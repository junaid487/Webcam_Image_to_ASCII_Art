import cv2 as cv
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import random
import time

ASCII_WIDTH = 140
ASCII_HEIGHT = 100

font = ImageFont.truetype("consola.ttf", size=9)
debug_font = ImageFont.truetype("arial.ttf", size=25)
rain_font = ImageFont.truetype("consola.ttf", size=12)

left, top, right, bottom = font.getbbox("A")

char_width = right - left
char_height = bottom - top

canvas_width = ASCII_WIDTH * char_width
canvas_height = ASCII_HEIGHT * char_height

char_set = [
    " .:-=+*#%@",
    " .:=+xX$&@",
    " .oO0@",
    " .,:;tLCG08@",
    " .-+O#@",
    " .:=*#%@",
    " `.-:+xX$&@",
    " .,-~+*#%@",
]

ascii_chars = char_set[0]
rain_chars = "0123456789"
next_set = 1

color = "white"
sigma_x = 0.0
show_rain = False


def create_stream():
    length = random.randint(12, 20)

    return {
        "x": random.randint(20, canvas_width - 20),
        "y": random.randint(-(length * char_height), canvas_height // 2),
        "length": length,
        "speed": random.randint(3, 7)
    }


streams = []
max_streams = 50

def gray_image(frame):
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    if frame.mean() < 150:
        gray_img = cv.equalizeHist(gray_img)
            
    gray_img = cv.resize(gray_img, (ASCII_WIDTH, ASCII_HEIGHT))

    return gray_img


def create_canvas():
    canvas = Image.new("RGB", (canvas_width, canvas_height), "black")
    draw = ImageDraw.Draw(canvas)
    return canvas, draw


def draw_ascii(text, draw, color, fps, char_set_num):
    y = 0

    for row in text.splitlines():
        draw.text((0, y), row, fill=color, font=font)
        y += char_height

    blur_text = f"Blur: {int(sigma_x * 5)}"
    draw.text((10, 10), blur_text, fill="yellow", font=debug_font)

    stream_count = f"Streams: {len(streams)}"
    draw.text((10, 50), stream_count, fill="yellow", font=debug_font)

    fps_display = f"FPS: {fps}"
    draw.text((10, 90), fps_display, fill="yellow", font=debug_font)

    char_set_count = f"Char Set: {char_set_num}"
    draw.text((10, 130), char_set_count, fill="yellow", font=debug_font)


def draw_matrix_rain(draw):
    if not show_rain:
        return
    
    for stream in streams:        
        stream["y"] += stream["speed"]

        if stream["y"] > canvas_height + (stream["length"] * char_height):
            stream.update(create_stream())

        for i in range(stream["length"]):
            char = random.choice(rain_chars)

            if i == 0:
                draw.text(
                    (stream["x"], stream["y"] - (i * (char_height + 2))),
                    char,
                    fill="white",
                    font= rain_font
                )
            else:
                green_value = max(50, 255 - i * 10)

                draw.text(
                    (stream["x"], stream["y"] - (i * (char_height + 2))),
                    char,
                    fill=(0, green_value, 0),
                    font=rain_font
                )


def generate_ascii(img):
    rows = []

    for row in range(img.shape[0]):
        line = []

        for col in range(img.shape[1]):
            pixel = int(img[row, col])
            line.append(ascii_chars[pixel * len(ascii_chars) // 256])

        rows.append("".join(line))

    return "\n".join(rows)


def blur_image(img, key):
    global sigma_x

    if key == ord("p"):
        sigma_x += 0.2
        sigma_x = min(2, sigma_x)

    if key == ord("o"):
        sigma_x -= 0.2
        sigma_x = max(0, sigma_x)

    if key == ord("r"):
        sigma_x = 0

    if sigma_x <= 0:
        return img

    return cv.GaussianBlur(img, (0, 0), sigma_x)


def display_image(canvas, key):
    ascii_img = cv.cvtColor(np.array(canvas), cv.COLOR_RGB2BGR)
    ascii_img = blur_image(ascii_img, key)
    cv.imshow("ASCII Webcam", ascii_img)


start = time.perf_counter()
current_fps = 0
frame_count = 0
def calc_FPS():
    global frame_count, start, current_fps

    frame_count += 1

    end = time.perf_counter()
    elapsed = end - start

    if elapsed >= 1:
        current_fps = int(frame_count / elapsed)

        frame_count = 0
        start = end

    return current_fps


cv.namedWindow("ASCII Webcam", cv.WINDOW_NORMAL)

cv.setWindowProperty(
    "ASCII Webcam",
    cv.WND_PROP_FULLSCREEN,
    cv.WINDOW_FULLSCREEN
)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")


while True:
    ret, frame = cap.read()

    if not ret:
        print("Something went wrong")
        break

    gray_img = gray_image(frame)
    ascii_text = generate_ascii(gray_img)

    canvas, draw = create_canvas()

    fps = calc_FPS()

    key = cv.waitKey(1) & 0xFF

    if key in (ord("m"), ord("M")):
        if color == "white":
            color = "green"
            show_rain = True
        else:
            color = "white"
            show_rain = False

    if key in (ord("q"), ord("Q")):
        break

    if key == ord('['):
        max_streams -= 1
        max_streams = max(10, max_streams)

        if len(streams) > max_streams:
            streams.pop()

    elif key == ord(']'):
        max_streams += 1
        max_streams = min(100, max_streams)

    if key == ord('n'):
        show_rain = not show_rain

    if key == ord(' '):        
        if next_set < len(char_set):
            next_set += 1
        else:
            next_set = 1

        ascii_chars = char_set[next_set - 1]
        

    while len(streams) < max_streams:
        streams.append(create_stream())

    draw_ascii(ascii_text, draw, color, fps, next_set)
    draw_matrix_rain(draw)
    display_image(canvas, key)

cap.release()
cv.destroyAllWindows()