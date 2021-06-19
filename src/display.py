import os
import colorsys
import ST7735
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fonts.ttf import RobotoMedium as UserFont
import pytz
from pytz import timezone
from astral.geocoder import database, lookup
from astral.sun import sun
from datetime import datetime, timedelta

import settings

# Initialise the LCD
disp = ST7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

disp.begin()

WIDTH = disp.width
HEIGHT = disp.height

# Fonts
font_sm = ImageFont.truetype(UserFont, 12)
font_lg = ImageFont.truetype(UserFont, 14)

# Margins
margin = 3

#### Drawing Methods ======================
def calculate_y_pos(x, centre):
    """Calculates the y-coordinate on a parabolic curve, given x."""
    centre = 80
    y = 1 / centre * (x - centre) ** 2

    return int(y)

def circle_coordinates(x, y, radius):
    """Calculates the bounds of a circle, given centre and radius."""

    x1 = x - radius  # Left
    x2 = x + radius  # Right
    y1 = y - radius  # Bottom
    y2 = y + radius  # Top

    return (x1, y1, x2, y2)

def overlay_text(img, position, text, font, align_right=False, rectangle=False):
    draw = ImageDraw.Draw(img)
    w, h = font.getsize(text)
    if align_right:
        x, y = position
        x -= w
        position = (x, y)
    if rectangle:
        x += 1
        y += 1
        position = (x, y)
        border = 1
        rect = (x - border, y, x + w, y + h + border)
        rect_img = Image.new('RGBA', (WIDTH, HEIGHT), color=(0, 0, 0, 0))
        rect_draw = ImageDraw.Draw(rect_img)
        rect_draw.rectangle(rect, (255, 255, 255))
        rect_draw.text(position, text, font=font, fill=(0, 0, 0, 0))
        img = Image.alpha_composite(img, rect_img)
    else:
        draw.text(position, text, font=font, fill=(255, 255, 255))
    return img
#### ======================================

#### Background ===========================
# background constants
blur = 50
opacity = 125

mid_hue = 0
day_hue = 25

sun_radius = 50

def map_colour(x, centre, start_hue, end_hue, day):
    """Given an x coordinate and a centre point, a start and end hue (in degrees),
       and a Boolean for day or night (day is True, night False), calculate a colour
       hue representing the 'colour' of that time of day."""

    start_hue = start_hue / 360  # Rescale to between 0 and 1
    end_hue = end_hue / 360

    sat = 1.0

    # Dim the brightness as you move from the centre to the edges
    val = 1 - (abs(centre - x) / (2 * centre))

    # Ramp up towards centre, then back down
    if x > centre:
        x = (2 * centre) - x

    # Calculate the hue
    hue = start_hue + ((x / centre) * (end_hue - start_hue))

    # At night, move towards purple/blue hues and reverse dimming
    if not day:
        hue = 1 - hue
        val = 1 - val

    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, sat, val)]

    return (r, g, b)

def x_from_sun_moon_time(progress, period, x_range):
    """Recalculate/rescale an amount of progress through a time period."""

    x = int((progress / period) * x_range)

    return x

def sun_moon_time(city_name, time_zone):
    """Calculate the progress through the current sun/moon period (i.e day or
       night) from the last sunrise or sunset, given a datetime object 't'."""

    city = lookup(city_name, database())

    # Datetime objects for yesterday, today, tomorrow
    utc = pytz.utc
    utc_dt = datetime.now(tz=utc)
    local_dt = utc_dt.astimezone(pytz.timezone(time_zone))
    today = local_dt.date()
    yesterday = today - timedelta(1)
    tomorrow = today + timedelta(1)

    # Sun objects for yesterday, today, tomorrow
    sun_yesterday = sun(city.observer, date=yesterday)
    sun_today = sun(city.observer, date=today)
    sun_tomorrow = sun(city.observer, date=tomorrow)

    # Work out sunset yesterday, sunrise/sunset today, and sunrise tomorrow
    sunset_yesterday = sun_yesterday["sunset"]
    sunrise_today = sun_today["sunrise"]
    sunset_today = sun_today["sunset"]
    sunrise_tomorrow = sun_tomorrow["sunrise"]

    # Work out lengths of day or night period and progress through period
    if sunrise_today < local_dt < sunset_today:
        day = True
        period = sunset_today - sunrise_today
        # mid = sunrise_today + (period / 2)
        progress = local_dt - sunrise_today
    
    elif local_dt > sunset_today:
        day = False
        period = sunrise_tomorrow - sunset_today
        # mid = sunset_today + (period / 2)
        progress = local_dt - sunset_today

    else:
        day = False
        period = sunrise_today - sunset_yesterday
        # mid = sunset_yesterday + (period / 2)
        progress = local_dt - sunset_yesterday

    # Convert time deltas to seconds
    progress = progress.total_seconds()
    period = period.total_seconds()

    return (progress, period, day, local_dt)

def draw_background(progress, period, day):
    """Given an amount of progress through the day or night, draw the
       background colour and overlay a blurred sun/moon."""

    # x-coordinate for sun/moon
    x = x_from_sun_moon_time(progress, period, WIDTH)

    # If it's day, then move right to left
    if day:
        x = WIDTH - x

    # Calculate position on sun/moon's curve
    centre = WIDTH / 2
    y = calculate_y_pos(x, centre)

    # Background colour
    background = map_colour(x, 80, mid_hue, day_hue, day)

    # New image for background colour
    img = Image.new('RGBA', (WIDTH, HEIGHT), color=background)
    # draw = ImageDraw.Draw(img)

    # New image for sun/moon overlay
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), color=(0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    # Draw the sun/moon
    circle = circle_coordinates(x, y, sun_radius)
    overlay_draw.ellipse(circle, fill=(200, 200, 50, opacity))

    # Overlay the sun/moon on the background as an alpha matte
    composite = Image.alpha_composite(img, overlay).filter(ImageFilter.GaussianBlur(radius=blur))

    return composite
#### ======================================

def set_datetime(background,local_dt):
    date_string = local_dt.strftime("%d %b %y").lstrip('0')
    time_string = local_dt.strftime("%H:%M")
    img = overlay_text(background, (0 + margin, 0 + margin), time_string, font_lg)
    img = overlay_text(img, (WIDTH - margin, 0 + margin), date_string, font_lg, align_right=True)
    return img

def text(img,x,y,reading,reading_range):
    img = overlay_text(img, (x, y), reading, font_lg, align_right=True)
    spacing = font_lg.getsize(reading)[1] + 1
    img = overlay_text(img, (x, y + spacing), reading_range, font_sm, align_right=True, rectangle=True)
    return img

def update(amb,pol,statusHistory):
    path = os.path.dirname(os.path.realpath(__file__))
    progress, period, day, local_dt = sun_moon_time(settings.CITY_NAME, settings.TIME_ZONE)
    
    # get the rendered background design
    background = draw_background(progress,period,day)

    # add the time to the display drawing
    img = set_datetime(background,local_dt)

    # column 1 - top (temp)
    img = text(img,68,18,str(amb['temp']),'60-80')
    temp_icon = Image.open(f"{path}/icons/temperature.png")
    img.paste(temp_icon,(margin,18),mask=temp_icon)
    
    # column 1 - bottom (humidity)
    img = text(img,68,48,str(round(amb['humidity'])),'Good')
    humidity_icon = Image.open(f"{path}/icons/humidity-good.png")
    img.paste(humidity_icon,(margin,50),mask=humidity_icon)

    # column 2 - top (AQI)
    img = text(img,WIDTH-4*margin,18,str(pol['aqi']['aqi-val']),pol['aqi']['aqi'])
    aqi_icon = Image.open(f"{path}/icons/aqi.png").convert("RGBA")
    img.paste(aqi_icon,(80,16),mask=aqi_icon)

    # column 2 - bottom (pm 2.5/10)
    img = text(img,WIDTH-4*margin,48,str(pol['pm2.5']),'Good')
    pm25_icon = Image.open(f"{path}/icons/pm25.png").convert("RGBA")
    img.paste(pm25_icon,(80,46),mask=pm25_icon)

    # render the status indicators
    check_icon = Image.open(f"{path}/icons/circle-check.png").convert("RGBA")
    times_icon = Image.open(f"{path}/icons/circle-times.png").convert("RGBA")
    x_offset = 49
    y_offset = 0+margin+3
    for x in reversed(statusHistory):
        if x:
            img.paste(check_icon,(x_offset,y_offset),mask=check_icon)
        else:
            img.paste(times_icon,(x_offset,y_offset),mask=times_icon)
        
        x_offset = x_offset+8

    # render the image
    disp.display(img)