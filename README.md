# HTTP_DISPLAY

This is a simple program that will retrieve an image from an http server and will display it on a Pimoroni ePaper display of the inky series.


# Hardware used for development / testing

The code is developed and tested on:

* [RaspberryPi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/)
* [Raspberry Pi OS](https://www.raspberrypi.com/software/)
* [Pimoroni Inky Impression 4"](https://shop.pimoroni.com/products/inky-impression-4)


# Working

After installing the program and the systemd service + timer, the program will retrieve every 5 minutes a picture from a http server.

It then will compare if the picture is the same as already displayed. If it is, it will stop processing.

If the picture is different, then it will update the picture on the ePaper display, and update the file that is used to determine the differences.

## Detecting picture differences

This is done using the md5 hashing algorithm. Since we are only interested in determining any difference between the current picture and a newly downloaded one, this is a perfectly fine way to do it.

Using md5 might sound 'insecure', but since we are only interested in a cheap way to determine differences, it isn't bad. As a hash collision will only cause the picture not to be updated.


# Configuration
The tool uses an environment variable set in the systemd service file, to determine which url should be used to download the picture. It's up to the user, to i.e. update the picture on the server side with new content, which then will be picked up automatically.


# Install

On the raspberry os, it's important that the I2C and SPI interfaces are enabled on the raspberry pi. These can be enabled via:

    sudo raspi-config

## Python code

Python can be directly installed from this github repo via the following command:

    sudo pip install https://github.com/woutervb/http_display.git

## Systemd files

Easiest (and safest) thing to do, is install the systemd files under a user account i.e. via the following commands:

    mkdir -p ~/.config/systemd/user
    cd ~/.config/systemd/user
    wget https://raw.githubusercontent.com/woutervb/http_display/main/http_display.timer
    wget https://raw.githubusercontent.com/woutervb/http_display/main/http_display.service

    # Edit the service file, so that the url is valid
    # vi http_display.service

    # enable the timer & service
    systemctl --user enable http_display.timer
    systemctl --user enable --now http_display.service

    # Ensure that user sessions are started on boot
    loginctl enable-linger $USER

