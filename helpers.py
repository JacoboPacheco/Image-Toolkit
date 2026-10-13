from PIL import Image

def load_image(path, max_size=200):
    """Open an image and return it as a list of rows of (r, g, b) tuples.
    The image is shrunk so its longest side is at most max_size pixels."""
    img = Image.open(path).convert("RGB")
    img.thumbnail((max_size, max_size))
    w, h = img.size
    data = list(img.getdata())
    return [data[r * w:(r + 1) * w] for r in range(h)]

def load_square(path, size=128):
    """Open an image cropped and resized to size x size (use a power of 2)."""
    img = Image.open(path).convert("RGB")
    side = min(img.size)
    img = img.crop((0, 0, side, side)).resize((size, size))
    data = list(img.getdata())
    return [data[r * size:(r + 1) * size] for r in range(size)]

def save_image(pixels, path):
    """Save a list of rows of (r, g, b) tuples as an image file."""
    h, w = len(pixels), len(pixels[0])
    img = Image.new("RGB", (w, h))
    img.putdata([tuple(p) for row in pixels for p in row])
    img.save(path)

def blank_image(width, height, color=(255, 255, 255)):
    """Return a new image filled with one color."""
    return [[color for _ in range(width)] for _ in range(height)]