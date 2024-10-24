# UsbMiniLEDRing
I had a USB Light Ring with 16 WS2812B LEDs that I wanted to test as a USB HID device, so this is my test program. I ended up writing a colour picker and USB class for it to make it more encapsulated.

Click the coloured LED circle to change the colour in the colour picker below. Or you can CTRL + Click multiple LEDs to change them at once.

## Compiling

Use Python v3.10.11 and download the following packages:
- PyQt6
- PyUsb