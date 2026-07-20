

import os
import random
import shutil
import uuid

IMAGE_FOLDERS = {
    "Books": "books",
    "Notes": "notes",
    "Electronics": "electronics",
    "Furniture": "furniture",
    "Hostel Essentials": "hostel",
    "Sports": "sports",
    "Cycles": "cycle",
    "Stationery and Tools": "stationary",
    "Others": "others"
}

BASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "images"
)

UPLOAD_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "static",
        "uploads"
    )
)


def copy_random_image(category):

    folder = IMAGE_FOLDERS[category]

    image_folder = os.path.join(BASE_PATH, folder)

    images = [
        img for img in os.listdir(image_folder)
        if img.endswith(".jpg")
    ]

    selected = random.choice(images)

    extension = os.path.splitext(selected)[1]

    new_filename = f"{uuid.uuid4().hex}{extension}"

    shutil.copy(
        os.path.join(image_folder, selected),
        os.path.join(UPLOAD_FOLDER, new_filename)
    )

    return new_filename