"""Run every function in toolkit.py on sample images and run the experiments
from section 1.6.

Usage:
    python demo.py                      # uses the generated sample images
    python demo.py photo.jpg            # uses your own photo for Parts 1 and 2
    python demo.py photo.jpg cartoon.png

Input and output images are written to the examples/ folder.
"""

import os
import sys

from helpers import load_image, save_image, blank_image
from toolkit import (
    grayscale, invert, flip_horizontal, flip_vertical, rotate_90, blur,
    pixelate, unique_colors, brightness_histogram, print_histogram,
    paint_bucket,
)

OUT = "examples"


# ---------------------------------------------------------------------------
# Sample images, drawn pixel by pixel (no drawing library needed)
# ---------------------------------------------------------------------------

def fill_rect(pixels, top, left, bottom, right, color):
    for r in range(max(top, 0), min(bottom, len(pixels))):
        for c in range(max(left, 0), min(right, len(pixels[0]))):
            pixels[r][c] = color


def fill_circle(pixels, cy, cx, radius, color):
    for r in range(len(pixels)):
        for c in range(len(pixels[0])):
            if (r - cy) ** 2 + (c - cx) ** 2 <= radius ** 2:
                pixels[r][c] = color


def make_photo(width=160, height=120):
    """A colorful image with smooth gradients, shapes and fine detail."""
    pixels = []
    for r in range(height):
        row = []
        for c in range(width):
            red = 255 * c // (width - 1)
            green = 255 * r // (height - 1)
            blue = 255 - (red + green) // 2
            row.append((red, green, blue))
        pixels.append(row)
    fill_circle(pixels, 40, 45, 25, (250, 220, 40))
    fill_rect(pixels, 65, 90, 105, 145, (30, 30, 30))
    fill_rect(pixels, 75, 100, 95, 135, (230, 230, 230))
    # Thin stripes show off blur and pixelate
    for c in range(10, 70, 4):
        fill_rect(pixels, 80, c, 110, c + 2, (255, 255, 255))
    return pixels


def make_cartoon(width=160, height=120):
    """A cartoon scene with large flat areas for the paint bucket."""
    pixels = blank_image(width, height, (120, 190, 240))       # sky
    fill_circle(pixels, 25, 130, 15, (255, 215, 0))            # sun
    fill_rect(pixels, 85, 0, height, width, (70, 160, 60))     # grass
    fill_rect(pixels, 50, 30, 95, 90, (200, 60, 50))           # house
    for i in range(20):                                        # roof
        fill_rect(pixels, 30 + i, 60 - i - 10, 31 + i, 60 + i + 10, (110, 60, 30))
    fill_rect(pixels, 70, 52, 95, 68, (90, 50, 20))            # door
    fill_rect(pixels, 58, 36, 68, 48, (250, 250, 210))         # window
    fill_rect(pixels, 58, 72, 68, 84, (250, 250, 210))         # window
    return pixels


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def path(name):
    return os.path.join(OUT, name)


def part1(img):
    print("=== Part 1: Photo filters ===")
    save_image(grayscale(img), path("1_1_grayscale.png"))
    save_image(invert(img), path("1_2_invert.png"))
    save_image(flip_horizontal(img), path("1_3_flip_horizontal.png"))
    save_image(flip_vertical(img), path("1_3_flip_vertical.png"))
    rotated = rotate_90(img)
    save_image(rotated, path("1_3_rotate_90.png"))
    print(f"rotate_90: {len(img)} x {len(img[0])} (rows x cols) -> "
          f"{len(rotated)} x {len(rotated[0])}")
    save_image(blur(img), path("1_4_blur.png"))
    for block in (4, 8, 16):
        save_image(pixelate(img, block), path(f"1_5_pixelate_{block}.png"))
    print("Saved filter outputs to", OUT)


def experiments(img):
    print("\n=== 1.6 Experiments ===")

    # Blur 1, 5 and 20 times
    blurred = img
    for times in range(1, 21):
        blurred = blur(blurred)
        if times in (1, 5, 20):
            save_image(blurred, path(f"1_6_blur_x{times}.png"))
            colors = unique_colors(blurred)
            print(f"blur x{times:2d}: {len(colors):5d} unique colors, "
                  f"top-left {blurred[0][0]}, bottom-right {blurred[-1][-1]}")
    print(f"original: {len(unique_colors(img)):5d} unique colors")

    # Involution / idempotence
    print("invert(invert(img)) == img:", invert(invert(img)) == img)
    gray = grayscale(img)
    print("grayscale(grayscale(img)) == grayscale(img):", grayscale(gray) == gray)
    every_gray = [[(v, v, v) for v in range(256)]]
    print("  ...and for every gray level 0-255:", grayscale(every_gray) == every_gray)

    # Rotations and flips
    four = rotate_90(rotate_90(rotate_90(rotate_90(img))))
    print("rotate_90 x4 == img:", four == img)
    both_flips = flip_vertical(flip_horizontal(img))
    two_rotations = rotate_90(rotate_90(img))
    save_image(both_flips, path("1_6_flip_h_then_v.png"))
    save_image(two_rotations, path("1_6_rotate_90_x2.png"))
    print("flip_horizontal then flip_vertical == rotate_90 x2:",
          both_flips == two_rotations)
    print("flip_horizontal then flip_vertical == img:", both_flips == img)


def part2(img):
    print("\n=== Part 2: Color ===")
    print("unique colors:", len(unique_colors(img)))
    tiny = [[(255, 0, 0), (0, 255, 0), (255, 0, 0)],
            [(0, 0, 0), (128, 128, 128), (255, 255, 255)]]
    print("unique_colors(tiny 2x3 image):", sorted(unique_colors(tiny)))
    try:
        {[255, 0, 0]}
    except TypeError as error:
        print("Putting a list in a set raises:", repr(error))
    hist = brightness_histogram(img)
    print("brightness_histogram:", hist)
    print_histogram(hist)


def part3(cartoon):
    print("\n=== Part 3: Paint bucket ===")
    sky = paint_bucket(cartoon, 5, 5, (255, 0, 255), tolerance=20)
    save_image(sky, path("3_paint_bucket_sky.png"))
    house = paint_bucket(sky, 80, 35, (0, 200, 255), tolerance=20)
    save_image(house, path("3_paint_bucket_house.png"))
    grass = paint_bucket(house, 110, 150, (255, 140, 0), tolerance=20)
    save_image(grass, path("3_paint_bucket_grass.png"))
    print("original unchanged:", cartoon[5][5] == (120, 190, 240))
    print("sky pixel after fill:", sky[5][5], "| sun pixel untouched:", sky[25][130])


def main():
    os.makedirs(OUT, exist_ok=True)
    if len(sys.argv) > 1:
        img = load_image(sys.argv[1])
    else:
        img = make_photo()
    if len(sys.argv) > 2:
        cartoon = load_image(sys.argv[2], max_size=120)
    else:
        cartoon = make_cartoon()
    save_image(img, path("0_input_photo.png"))
    save_image(cartoon, path("0_input_cartoon.png"))

    part1(img)
    experiments(img)
    part2(img)
    part3(cartoon)


if __name__ == "__main__":
    main()
