"""Image-processing toolkit for COP 3410 Assignment 3.

An image is a list of rows, each row is a list of pixels, and each pixel is a
tuple (r, g, b). Always index as pixels[row][col], which is pixels[y][x].
Every filter returns a NEW image and never changes the input in place.
"""

import sys


# ---------------------------------------------------------------------------
# Part 1: Photo filters
# ---------------------------------------------------------------------------

def gray_value(pixel):
    """Return the weighted grayscale value v of one (r, g, b) pixel."""
    r, g, b = pixel
    return round(0.299 * r + 0.587 * g + 0.114 * b)


def grayscale(pixels):
    """1.1: Return a new image where every pixel is (v, v, v)."""
    result = []
    for row in pixels:
        new_row = []
        for pixel in row:
            v = gray_value(pixel)
            new_row.append((v, v, v))
        result.append(new_row)
    return result


def invert(pixels):
    """1.2: Return the photo negative: each pixel becomes (255-r, 255-g, 255-b)."""
    return [[(255 - r, 255 - g, 255 - b) for (r, g, b) in row] for row in pixels]


def flip_horizontal(pixels):
    """1.3: Mirror the image left to right, using list slicing."""
    return [row[::-1] for row in pixels]


def flip_vertical(pixels):
    """1.3: Mirror the image top to bottom, using a loop."""
    result = []
    for r in range(len(pixels) - 1, -1, -1):
        result.append(list(pixels[r]))
    return result


def rotate_90(pixels):
    """1.3: Rotate the image 90 degrees clockwise.

    The output has `width` rows and `height` columns. Pixel (row, col) of the
    input moves to (col, height - 1 - row) of the output, so output pixel
    (r, c) comes from input pixel (height - 1 - c, r).
    """
    height = len(pixels)
    width = len(pixels[0])
    result = []
    for r in range(width):
        new_row = []
        for c in range(height):
            new_row.append(pixels[height - 1 - c][r])
        result.append(new_row)
    return result


def average_color(colors):
    """Return the rounded average (r, g, b) of a non-empty list of pixels."""
    n = len(colors)
    total_r = total_g = total_b = 0
    for r, g, b in colors:
        total_r += r
        total_g += g
        total_b += b
    return (round(total_r / n), round(total_g / n), round(total_b / n))


def blur(pixels):
    """1.4: 3 x 3 box blur.

    Each new pixel is the average of itself and its up-to-8 neighbors. Edge
    and corner pixels only average the neighbors that exist.
    """
    height = len(pixels)
    width = len(pixels[0])
    result = []
    for r in range(height):
        new_row = []
        for c in range(width):
            box = []
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width:
                        box.append(pixels[nr][nc])
            new_row.append(average_color(box))
        result.append(new_row)
    return result


def pixelate(pixels, block):
    """1.5: Split the image into block x block squares and paint each square
    with its average color. Squares on the right/bottom edge may be smaller."""
    height = len(pixels)
    width = len(pixels[0])
    result = [list(row) for row in pixels]
    for top in range(0, height, block):
        for left in range(0, width, block):
            bottom = min(top + block, height)
            right = min(left + block, width)
            square = [pixels[r][c] for r in range(top, bottom) for c in range(left, right)]
            color = average_color(square)
            for r in range(top, bottom):
                for c in range(left, right):
                    result[r][c] = color
    return result


# ---------------------------------------------------------------------------
# Part 2: Understanding color
# ---------------------------------------------------------------------------

def unique_colors(pixels):
    """2.1: Return a set of all distinct colors in the image."""
    colors = set()
    for row in pixels:
        for pixel in row:
            colors.add(pixel)
    return colors


def brightness_histogram(pixels, bins=16):
    """2.2: Return a dictionary mapping each bin number to a pixel count.

    A pixel with grayscale value v goes in bin v * bins // 256. Every bin from
    0 to bins - 1 is present, even if its count is 0.
    """
    hist = {b: 0 for b in range(bins)}
    for row in pixels:
        for pixel in row:
            v = gray_value(pixel)
            hist[v * bins // 256] += 1
    return hist


def print_histogram(hist, max_width=50):
    """2.2: Draw the histogram as a text bar chart.

    Bars are scaled so the tallest bin is max_width characters wide, because a
    real photo has thousands of pixels per bin.
    """
    largest = max(hist.values()) if hist else 0
    for b in sorted(hist):
        count = hist[b]
        length = round(count * max_width / largest) if largest else 0
        print(f"bin {b:2d} | {'#' * length} {count}")


# ---------------------------------------------------------------------------
# Part 3: Paint bucket (recursive flood fill)
# ---------------------------------------------------------------------------

def within_tolerance(color, target, tolerance):
    """Two colors are similar if each channel differs by at most tolerance."""
    for a, b in zip(color, target):
        if abs(a - b) > tolerance:
            return False
    return True


def flood_fill(pixels, row, col, target, new_color, tolerance, visited):
    """Recolor every pixel connected to (row, col) whose color is within
    `tolerance` of `target`. Moves are up, down, left and right only.

    `visited` is a set of (row, col) tuples. A set is a better choice than a
    list because checking `(row, col) in visited` takes constant time on
    average with a set (it is a hash lookup), but a list has to be scanned
    from the start every time, which gets slower as more pixels are filled.
    """
    # Base cases: off the image? already visited? color too different?
    if row < 0 or row >= len(pixels) or col < 0 or col >= len(pixels[0]):
        return
    if (row, col) in visited:
        return
    if not within_tolerance(pixels[row][col], target, tolerance):
        return

    # Recursive case: recolor this pixel, mark it visited,
    #                 then call flood_fill on the 4 neighbors.
    # Each call marks one more pixel as visited, so the number of pixels
    # left to explore keeps shrinking until every branch hits a base case.
    pixels[row][col] = new_color
    visited.add((row, col))
    flood_fill(pixels, row - 1, col, target, new_color, tolerance, visited)  # up
    flood_fill(pixels, row + 1, col, target, new_color, tolerance, visited)  # down
    flood_fill(pixels, row, col - 1, target, new_color, tolerance, visited)  # left
    flood_fill(pixels, row, col + 1, target, new_color, tolerance, visited)  # right


def paint_bucket(pixels, row, col, new_color, tolerance=30):
    """Return a copy of the image with the area connected to (row, col) filled
    with new_color. The original image is not modified."""
    copy = [list(r) for r in pixels]
    target = pixels[row][col]
    # A large region can need one nested call per pixel, which is more than
    # Python's default limit of about 1000.
    needed = len(pixels) * len(pixels[0]) + 1000
    if sys.getrecursionlimit() < needed:
        sys.setrecursionlimit(needed)
    flood_fill(copy, row, col, target, new_color, tolerance, set())
    return copy
