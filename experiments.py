from filters import grayscale, invert
from helpers import load_image, save_image
from pathlib import Path

# Change this to "dog.png" to test the other photo.
photo_name = "cat.png"

# Find the photos folder next to this file.
image_path = Path(__file__).parent / "photos" / photo_name
photo = load_image(image_path)

# Keep a copy to check that the original stays unchanged.
original_photo = [row[:] for row in photo]

# Apply each filter once, then apply it again to its result.
inverted_photo = invert(photo)
gray_photo = grayscale(photo)

inverted_twice = invert(inverted_photo)
gray_twice = grayscale(gray_photo)

####### TESTS ##########
# assert photo == original_photo, "A filter changed the original photo"
# # Inverting twice restores each color: 255 - (255 - value) = value.
# assert inverted_twice == photo, "Inverting the photo twice failed"
# # Gray pixels already have equal channels, so grayscale leaves them gray.
# assert gray_twice == gray_photo, "Grayscale twice changed the photo"
# # Check that both filters keep the same image size.
# assert all(len(row) == len(photo[0]) for row in inverted_photo)
# assert all(len(row) == len(photo[0]) for row in gray_photo)
# assert len(inverted_photo) == len(gray_photo) == len(photo)
# # Every grayscale pixel should have equal red, green, and blue values.
# assert all(r == g == b for row in gray_photo for r, g, b in row)
#######################

# Save the results in a separate folder to compare them visually.
output_dir = image_path.parent / (image_path.stem + "_results")
output_dir.mkdir(exist_ok=True)
save_image(photo, output_dir / "original.png")
save_image(inverted_photo, output_dir / "inverted.png")
save_image(gray_photo, output_dir / "grayscale.png")
save_image(inverted_twice, output_dir / "inverted_twice.png")
save_image(gray_twice, output_dir / "grayscale_twice.png")

# print("All photo tests passed!")
print("Images saved to:", output_dir.resolve())
