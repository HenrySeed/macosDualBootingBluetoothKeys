# macos DualBooting Bluetooth Keys

A script automating the process defined [here](https://www.insanelymac.com/forum/topic/268837-dual-boot-bluetooth-pairing-solved/) with the fix for catalina from [here](https://www.tonymacx86.com/threads/cannot-find-the-bluetooth-pair-key.233103/)

It grabs the keys from `com.apple.Bluetoothd.plist` and converts them into big endian for windows regestry.

You can then copy this to GoogleDrive (or another cloud storage)

Reboot into Windows and paste these keys under the corrosponding Interface in `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\BTHPORT\Parameters\Keys\$INTERFACE_ID`
