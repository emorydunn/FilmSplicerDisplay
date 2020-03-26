import os

path = "images"

for i in os.listdir(path):
  img_path = path + "/" + i
  os.remove(img_path)

os.rmdir(path)