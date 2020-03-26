# FilmSplicerDisplay

A simple slideshow viewer for an ESP8266 and 1.44" TFT display. 

The workflow is optimized to display images in a Keystone Manufactering film splicer. Each image is shown for 1 second before beginning to display the next image. The slideshow position is saved in `current.txt` and will resume where it left off after a reboot. 

## Usage

1. Precompile [`st7735`][st7735] using [mpy-cross][]
2. Set your WiFi SSID and password in `boot.py`
3. Use a tool like [ampy][] to copy the contents of the `sources` directory to the root of the ESP board. 
4. Copy the images you wish to display into `images_source`
5. Run `utilities/convert_images.py` to resize, matte, and convert the images to bitmaps
6. Copy the `images` directory to the board. 

### convert_images.py

This is a simple script to prepare images for display. It does three things:

1. Resize an image to 100 px on the long edge
    - If the image is already 128 x 128, it won't be resized
2. Add a black matte to the image, positioning it in place for display
3. Save the image as bitmap

If you wish to use custom images, but still use the bitmap conversion, save your image at 128 x 128 pixels. 

### remove_images.py

This will delete all images and the `images` folder _on the board_ to make it easy to copy new images over. 

`ampy run remove_images.py`

[ampy]: https://github.com/scientifichackers/ampy
[st7735]: https://github.com/cheungbx/st7735-esp8266-micropython
[mpy-cross]: https://pypi.org/project/mpy-cross/