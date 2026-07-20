from PIL import Image
import os

INPUT_FOLDER = "collage"
OUTPUT_FOLDER = "images"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):

    if not file.endswith((".png", ".jpg", ".jpeg")):
        continue

    category = os.path.splitext(file)[0]

    category_folder = os.path.join(OUTPUT_FOLDER, category)

    os.makedirs(category_folder, exist_ok=True)

    img = Image.open(os.path.join(INPUT_FOLDER, file))

    width, height = img.size

    tile_w = width // 4
    tile_h = height // 2

    count = 1

    for row in range(2):
        for col in range(4):

            left = col * tile_w
            upper = row * tile_h
            right = left + tile_w
            lower = upper + tile_h

            crop = img.crop((left, upper, right, lower))

            # Convert RGBA to RGB
            crop = crop.convert("RGB")

            crop.save(
            os.path.join(
            category_folder,
            f"{category}_{count}.jpg"
             ),
             quality=95
             )

            count += 1

print("All images split successfully!")