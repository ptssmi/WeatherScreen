import requests
import json

import time
import config

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 30

# Load default font.
font = ImageFont.truetype("arial.ttf", 17)

while True:
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={api}".format(lat=config.latitude, lon=config.longitude, part="hourly,minutely,alerts,daily", api=config.key)
    response = requests.get(url)
    data = response.json()

    temperature = round((data["current"]["temp"] - 273.15) * 9/5 + 32,2) #converts from kelvin to farenheit
    windspeed = round(data["current"]["wind_speed"] * 2.23694,2)         #converts from meters/sec to mph

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Diplays information on the screen
    draw.text((x, top),       str(temperature) + " °F" ,  font=font, fill=255)
    draw.text((x, top+16),     str(windspeed)+ " mph", font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(15*60)
