
from PIL import Image,ImageDraw,ImageFont

def main():

     image = Image.new("RGB",size=(2970,2100),color=(255,255,255))

     imagedraw = ImageDraw.Draw(image)

     imagefont = ImageFont. . .load_default()
     imagefont.

     imagedraw.text((10,10),text="Hello world",fill="black",)


     image.show()


if __name__ == '__main__':
    main()

