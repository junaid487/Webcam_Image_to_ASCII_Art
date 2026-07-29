import cv2 as cv
import numpy as np
from PIL import Image, ImageFont, ImageDraw

ASCII_WIDTH = 100
ASCII_HEIGHT = 80
WINDOW_NAME = "ASCII Webcam"

font = ImageFont.truetype("consola.ttf", size= 9)

left, top, right, bottom = font.getbbox("A")

char_width = right - left
char_height = bottom - top

canvas_width = ASCII_WIDTH * char_width
canvas_height = ASCII_HEIGHT * char_height

ascii_chars = " .:-=+*#%@"

cv.namedWindow("WINDOW_NAME", cv.WINDOW_NORMAL)
cv.setWindowProperty("WINDOW_NAME", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

cap = cv.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Something went wrong")
        break

    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # gray_img = cv.equalizeHist(gray_img)                          # good in low light
    gray_img = cv.resize(gray_img, (ASCII_WIDTH, ASCII_HEIGHT))

    canvas = Image.new('L', (canvas_width, canvas_height), 'black')
    draw = ImageDraw.Draw(canvas)

    for i in range(gray_img.shape[0]):
        row = ""

        for j in range(gray_img.shape[1]):
            pixel = int(gray_img[i, j])
            row += ascii_chars[len(ascii_chars) * pixel // 256]

        draw.text((0, i * char_height), row, fill= 255, font=font)

    ascii_img = np.array(canvas)

    cv.imshow("WINDOW_NAME", ascii_img)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()