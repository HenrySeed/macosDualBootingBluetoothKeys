import plistlib

"""
    Converts a given string representing a hex number between little endian and big endian
    eg:  beace6  => e6acbe
        be ac e6 // split by 2-char hex code
        e6 ac be // reverse
        e6acbe // rejoin
"""
def littleEndian_to_bigEndian(string):
    hex_vals = []
    index = 0
    buffer = ""
    while index < len(string):
        buffer += string[index]
        if index % 2 != 0:
            hex_vals.append(buffer)
            buffer = ""
        index += 1

    hex_vals.reverse()
    return "".join(hex_vals)

"""
    Splits a 24-char hex code into 4 sections of 8 chars each, seperated by a space
"""
def split_hex(hex_str):
    return " ".join([hex_str[0:8], hex_str[8:16], hex_str[16:24], hex_str[24:32]])

"""
    Prints the interface object
"""
def print_interface(interface):
    print(interface[0])
    for device in interface[1]:
        print("    {}: {}".format(device[0], device[1]))


"""
    Returns the loaded plist object as a dict from:
    /private/var/root/Library/Preferences/com.apple.Bluetoothd.plist
"""
def get_plist():
    f = open("/private/var/root/Library/Preferences/com.apple.Bluetoothd.plist", "rb")
    return plistlib.load(f)


"""
    Takes a plist dict and returns all the bluetooth interfaces it finds, 
    along with the converted keys for windows
"""
def get_interfaces(plist):
    mac_interfaces = []
    win_interfaces = []

    for interface_key, interface_val in plist["LinkKeys"].items():
        interface_ID = interface_key
        mac_interface = []
        win_interface = []

        for device_key, device_val in interface_val.items():
            val_decoded = device_val.hex()
            mac_interface.append([device_key, split_hex(val_decoded)])
            win_interface.append([device_key, split_hex(littleEndian_to_bigEndian(val_decoded))])

        mac_interfaces.append([interface_ID, mac_interface])
        win_interfaces.append([interface_ID, win_interface])

    return [mac_interfaces, win_interfaces]


def main():
    plist = get_plist()
    mac_interfaces, win_interfaces = get_interfaces(plist)

    print("""\n\n                 ___  ___   ___ _     _  __            
  _ __  __ _ __ / _ \/ __| | _ ) |_  | |/ /___ _  _ ___
 | '  \/ _` / _| (_) \__ \ | _ \  _| | ' </ -_) || (_-<
 |_|_|_\__,_\__|\___/|___/ |___/\__| |_|\_\___|\_, /__/
                                               |__/    
    ~ Henry Seed (2020)""")

    print("\n\n")
    print("You should copy this output to a cloud storage / different \ncomputer so you can access it once you've dualbooted.")
    print("\nOnce in Windows, open PowerShell as admin and run the following command:\n    psexec -s -i regedit")

    print("\nNavigate to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\BTHPORT\Parameters\Keys\$INTERFACE_ID  \n\n(Replace the $INTERFACE_ID with the interface you are using below)")

    print("\nFor each device you want to use in macOS and Windows, open that \nfield and write the data from the device under the Windows section below:")


    print("\n")
    print("Recognised {} Bluetooth interface(s):".format(len(mac_interfaces)))
    for adapter in mac_interfaces:
        print("    - $INTERFACE_ID: " + adapter[0])

    print("\n")
    print("macOS =========================")
    for interface in mac_interfaces:
        print_interface(interface)

    print("\n")
    print("Windows =======================")
    for interface in win_interfaces:
        print_interface(interface)

    print("\nCredit for the conversion used goes to Camoguy from the insanelyMac Forum\nhttps://www.insanelymac.com/forum/topic/268837-dual-boot-bluetooth-pairing-solved/")


if __name__ == '__main__':
    main()