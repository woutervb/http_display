#!/usr/bin/env python3

from os.path import exists
from os.path import join
import hashlib

from PIL import Image

from inky.auto import auto
from inky.inky_uc8159 import CLEAN
import urllib.request


class Inky:

    saturation = 0.5

    def __init__(self):
        self.inky = auto(ask_user=True, verbose=False)
                         
    def clean(self):
        for y in range(self.inky.height - 1):
            for x in range(self.inky.width - 1):
                self.inky.set_pixel(x, y, CLEAN)
        self.inky.show() 

    def show_image(self, path_to_image):
        image = Image.open(path_to_image).resize(self.inky.resolution)
        self.inky.set_image(image, saturation=self.saturation)
        self.inky.show() 

def main():
    cartoon_name = "/dev/shm/inky.png"
    md5_name = f"{cartoon_name}.md5"
    try:                 
        # Make an HTTP request to The Guardian website's cartoons section
        url = 'http://10.255.255.2/inky.png'
                         
        urllib.request.urlretrieve(url, cartoon_name)
        md5 = hashlib.md5(open(cartoon_name,'rb').read()).hexdigest()
                         
        draw = False
        if not exists(md5_name):
            # Missing md5, we have to draw
            draw = True  
        else:
            old_md5 = open(md5_name, "r").read()
            draw = old_md5 != md5
                         
        if draw:
            with open(md5_name, "w") as fh:
                fh.write(md5)
            inky = Inky()
            #inky.clean()
            inky.show_image(cartoon_name)
                         
    except Exception as exc:
        print(exc)       

if __name__ == "__main__":
    main()