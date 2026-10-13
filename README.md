# Image-Toolkit

A small image-processing toolkit written from scratch in pure Python for
**COP 3410 – Computational Thinking, Assignment 3: Organizing Information and Recursion**.

Every image is treated as a grid of numbers, so each filter is an exercise in
data structures (lists, tuples, dictionaries, sets) and recursion. No computer
vision libraries such as OpenCV (`cv2`) are used; Pillow is only used to read
and write image files.

## Authors / Contributors

- Andres Zubizarreta
- Jacobo Pacheco
- Samantha Timmins
- Nicolas Cava
- Isam Salem

## How images are represented

An image is a **list of rows**, where each row is a **list of pixels**, and each
pixel is a **tuple** `(r, g, b)` with values from 0 to 255.

```python
pixels = [
    [(255, 0, 0), (0, 255, 0)],        # row 0
    [(0, 0, 255), (255, 255, 255)],    # row 1
]
```

Pixels are always indexed as `pixels[row][col]`, which is `pixels[y][x]`.

## Project structure

| File | Purpose |
| --- | --- |
| `helpers.py` | Provided helper functions for loading, saving and creating images |
| `README.md` | This file |

### Helper functions (`helpers.py`)

- `load_image(path, max_size=200)`: opens an image and returns it as a list of rows of `(r, g, b)` tuples, shrunk so its longest side is at most `max_size` pixels.
- `load_square(path, size=128)`: opens an image cropped and resized to `size × size` (use a power of 2).
- `save_image(pixels, path)`: saves a list of rows of `(r, g, b)` tuples as an image file.
- `blank_image(width, height, color=(255, 255, 255))`: returns a new image filled with one color.

## Part 1: Photo filters

Every filter takes an image and returns a **new** image. The input image is never modified in place.

| Function | Description |
| --- | --- |
| `grayscale(pixels)` | Each pixel becomes `(v, v, v)` where `v = round(0.299R + 0.587G + 0.114B)` |
| `invert(pixels)` | Each pixel becomes `(255 - r, 255 - g, 255 - b)`, like a photo negative |
| `flip_horizontal(pixels)` | Mirrors the image left to right (implemented with list slicing) |
| `flip_vertical(pixels)` | Mirrors the image top to bottom (implemented with a loop) |
| `rotate_90(pixels)` | Rotates the image 90° clockwise; the output has `width` rows and `height` columns |
| `blur(pixels)` | 3 × 3 box blur; each pixel is the average of itself and its existing neighbors (edge pixels average fewer neighbors) |
| `pixelate(pixels, block)` | Splits the image into `block × block` squares and paints each with its average color (tested with `block = 4, 8, 16`) |

### Experiments (1.6)

- Apply `blur` 1, 5 and 20 times and observe why the image never becomes one solid color.
- Test whether `invert(invert(img)) == img` and `grayscale(grayscale(img)) == grayscale(img)` always hold.
- Compare `rotate_90` applied four times, `flip_horizontal` followed by `flip_vertical`, and `rotate_90` applied twice.

## Part 2: Understanding color

Because pixels are tuples, they are hashable and can be used as dictionary keys and set members.

| Function | Description |
| --- | --- |
| `unique_colors(pixels)` | Returns a set of all distinct colors in the image |
| `brightness_histogram(pixels, bins=16)` | Returns a dictionary mapping each bin number to a count, using the grayscale value `v` placed in bin `v * bins // 256` |
| `print_histogram(hist)` | Draws the histogram as a text bar chart |

## Part 3: Paint bucket (recursive flood fill)

A recursive paint bucket that fills a connected area of similar color, like the
bucket tool in drawing apps.

- The image is copied first so the original is not modified.
- Two colors are "within tolerance" if each channel differs by at most `tolerance`.
- Visited positions are tracked in a **set** of `(row, col)` tuples for constant-time membership checks.
- Every recursive function marks its **base case** (when to stop) and **recursive case** (how the problem shrinks) in comments.

Note: filling a large region recursively can exceed Python's default recursion
limit (about 1000 calls). Keep test images small (the helpers shrink images to
200 pixels by default) or raise the limit with `sys.setrecursionlimit(...)`.

## Getting started

### Requirements

- Python 3.8+
- [Pillow](https://pypi.org/project/pillow/) (for reading and writing image files only)

```bash
pip install pillow
```

### Google Colab

The assignment recommends Google Colab. Upload `helpers.py` (or mount Google
Drive) and import it in a notebook cell:

```python
from google.colab import drive
drive.mount('/content/drive')

import sys
sys.path.append('/content/drive/MyDrive/Image-Toolkit')
from helpers import load_image, save_image
```

### Example usage

```python
from helpers import load_image, save_image

img = load_image("photo.jpg")
save_image(grayscale(img), "photo_gray.png")
save_image(pixelate(img, 8), "photo_pixelated.png")
```

Any personal photo or freely available image can be used for testing. A
cartoon-style image with large flat areas works best for the paint bucket.

## Submission

The final submission is a single PDF containing:

- Written answers to every question in the assignment (including why a pixel is a tuple but a row is a list, and which flip implementation was clearer).
- The exported code.
- For each function, an example input image and the corresponding output image.
