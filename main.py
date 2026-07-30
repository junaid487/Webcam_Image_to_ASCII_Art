import cv2 as cv
import numpy as np
from PIL import Image, ImageFont, ImageDraw


ASCII_WIDTH = 100
ASCII_HEIGHT = 80

font = ImageFont.truetype("consola.ttf", size= 9)

left, top, right, bottom = font.getbbox("A")

char_width = right - left
char_height = bottom - top

canvas_width = ASCII_WIDTH * char_width
canvas_height = ASCII_HEIGHT * char_height

ascii_chars = " .:-=+*#%@"
rain_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

color = 'white'


def gray_image(frame):
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_img = cv.equalizeHist(gray_img)
    gray_img = cv.resize(gray_img, (ASCII_WIDTH, ASCII_HEIGHT))
    return gray_img


def create_canvas():
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'black')
    draw = ImageDraw.Draw(canvas)
    return canvas, draw


def draw_ascii(text, draw, color):
    y = 0
    for row in text.splitlines():
        draw.text((0, y), row, fill=color, font=font)
        y += char_height


def draw_matrix_rain():
    # x = random pos
    # y = random pos
    # draw.text((x, y), text, fill= 'green maybe, font=font)
    pass


def generate_ascii(img):
    ascii_text = ""
    
    for row in range(img.shape[0]):
        for col in range(img.shape[1]):
            pixel = int(img[row, col])
            ascii_text += ascii_chars[len(ascii_chars) * pixel // 256]
        ascii_text += "\n"

    return ascii_text


def display_image(canvas):
    ascii_img = cv.cvtColor(np.array(canvas), cv.COLOR_RGB2BGR)
    cv.imshow("ASCII Webcam", ascii_img)
    

cv.namedWindow("ASCII Webcam", cv.WINDOW_NORMAL)
cv.setWindowProperty("ASCII Webcam", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

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

    key = cv.waitKey(1) & 0xFF

    if key in (ord('m'), ord('M')) :
        if color == 'white':
            color = 'green'
        else:
            color = 'white'

    if key in (ord('q'), ord('Q')):
        break

    draw_ascii(ascii_text, draw, color)
    display_image(canvas)


cap.release()
cv.destroyAllWindows()
