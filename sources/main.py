import os
import time

from ST7735 import TFT,TFTColor
from machine import SPI,Pin


# hardware SPI, HSPI
# spi = SPI(1, baudrate=8000000, polarity=0, phase=0)
spi = SPI(1, baudrate=125200, polarity=0, phase=0)

tft=TFT(spi,0,0,2)
tft.init_7735(tft.GREENTAB128x128)
tft.rotation(2)
tft.fill(TFT.BLACK)

def load_image(path):
    f=open(path, 'rb')
    if f.read(2) == b'BM':  #header
        dummy = f.read(8) #file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                print("Image size:", width, "x", height)
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                w, h = width, height
    #            if w > 128: w = 128
    #            if h > 160: h = 160
                if w > 128: w = 128
                if h > 160: h = 160

                tft._setwindowloc((0,0),(w - 1,h - 1))
                for row in range(h):
                    if flip:
                        pos = offset + (height - 1 - row) * rowsize
                    else:
                        pos = offset + row * rowsize
                    if f.tell() != pos:
                        dummy = f.seek(pos)
                    for col in range(w):
                        bgr = f.read(3)
                        tft._pushcolor(TFTColor(bgr[2],bgr[1],bgr[0]))
            else:
                print("Depth is not 24-bit")
        else:
            print("Planes is not 1")
    else:
        print("Bad image")
# spi.deinit()

def list_images(path):
    image_paths = []
    for image in os.listdir(path):
        img_path = path + "/" + image
        image_paths.append(img_path)
    return image_paths

def slide_show(image_paths):
    current_image_filename = "current.txt"

    try:
        current_image_file = open(current_image_filename, "r")
        current_img = int(current_image_file.read())
        current_image_file.close()
    except Exception as e:
        print(e)
        current_img = 0

    while True:
        if current_img >= len(image_paths):
            current_img = 0

        img_path = image_paths[current_img]
        print("display " + img_path)
        load_image(img_path)

        current_img += 1
        try:
            current_image_file = open(current_image_filename, "w")
            current_image_file.write("{}".format(current_img))
            current_image_file.close()
        except Exception as e:
            print(e)
            print("Failed to write current image")

        time.sleep_ms(1000)


image_paths = list_images("images")

slide_show(image_paths)