import os
from PIL import Image

def scale_to_size(im1, width):

    wpercent = float(width)/im1.size[0]
    hsize = int(im1.size[1]*wpercent)
    return im1.resize((width, hsize), Image.ANTIALIAS)

def resize_image(image):
  if image.size == (128, 128):
    print("Image is at display resolution")
    return image
  elif image.size[0] == 100:
    print("Image is thumbnail")
    return image
  else:
    print("Image needs resize")
    return scale_to_size(image, 100)

def matte_image(image):
  if image.size == (128, 128):
    print("Image is matted")
    return image
  else:
    print("Image needs matte")
    matte = Image.new('RGB', (128,128), (0,0,0,1))

    # Verticaly center the image in the display region
    # upperLeft - (imageHeight - bbHeight) / 2
    y = 50-(image.size[1]-65)/2
    matte.paste(image, (28,y))

    return matte

def convert_image(sourcePath):
  try:
    im = Image.open(sourcePath)

    fileName = os.path.splitext(os.path.basename(sourcePath))[0]
    print(fileName)

    # Resize and matte the image
    im = resize_image(im)
    im = matte_image(im)

    # Replace spaces and save to `images`
    fileName = fileName.replace(" ", "-")
    newPath = "../images/{}.bmp".format(fileName)

    im.save(newPath)

  except Exception as e:
    print(e)


def convertImagesIn(dir):
  for i in os.listdir(dir):

    convert_image(os.path.join(dir, i))


convertImagesIn("../images_source")