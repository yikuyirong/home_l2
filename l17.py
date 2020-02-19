import os
from PIL import Image

def save_image(input_name, output_name):
    im = Image.open(input_name)
    if im.mode=="RGBA":
        im.load()  # required for png.split()
        background = Image.new("RGB", im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3])  # 3 is the alpha channel
        im = background
    im.save('{}.jpg'.format(output_name),'JPEG')

def main():

    file_dir = "/Users/yikuyirong/desktop/语文课本"

    for file in os.listdir(file_dir):
        save_image(os.path.join(file_dir,file),os.path.join(file_dir,file))



if __name__ == "__main__":
    main()