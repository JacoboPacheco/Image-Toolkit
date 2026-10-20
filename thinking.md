# Nico's Part and Thoughts:

My part:
    - 1.1 Grayscale
    - 1.2 Invert
    - 1.6 Experiments: invert twice / grayscale twice question

Q: Is invert(invert(img)) == img always true?
A: Yes, when you invert the image a second time, it restores the original image
    255 - (255 - value) = value

Q: Is grayscale(grayscale(img)) == grayscale(img)?
A: Yes, after the first grayscale, each pixel has equal red, green, and blue values.
    The weights add up to 1, so applying grayscale again keeps the same values.
