# 1.1 Grayscale
def grayscale(pixels):
    """Make a gray copy of the image without changing the original."""
    grayscale_rows = []
    for row in pixels:
        grayscale_row = []
        for pixel in row:
            # Calculate brightness and use it for all three colors.
            v = round(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
            grayscale_row.append((v, v, v))
        grayscale_rows.append(grayscale_row)
    return grayscale_rows


# 1.2 Invert
def invert(pixels):
    """Make a copy with opposite colors without changing the original."""
    invert_rows = []
    for row in pixels:
        invert_row = []
        for pixel in row:
            # Subtract each color value from 255.
            invert_row.append((255 - pixel[0], 255 - pixel[1], 255 - pixel[2]))
        invert_rows.append(invert_row)
    return invert_rows


