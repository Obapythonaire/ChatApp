from PIL import Image
from django.core.exceptions import ValidationError
import os


def validate_icon_image_size(image):
    """Validate that icon images don't exceed 70x70 pixels"""
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                   f"The maximum allowed dimensions for the image are 70x70 - size you uploaded is {img.width}x{img.height}")


def validate_banner_image_size(image):
    """Validate that banner images don't exceed 1280x720 pixels"""
    if image:
        with Image.open(image) as img:
            if img.width > 1280 or img.height > 720:
                raise ValidationError(
                   f"The maximum allowed dimensions for the image are 1280x720 - size you uploaded is {img.width}x{img.height}")


def validate_image_file_extension(value):
    """Validate that uploaded files have allowed image extensions"""
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f"Unsupported file extension {ext}")