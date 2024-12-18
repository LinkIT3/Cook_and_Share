from PIL import Image
import pillow_avif
from django.core.exceptions import ValidationError

MAX_PROFILE_PIC_SIZE_KB = 500
MAX_PROFILE_PIC_WIDTH = 500
MAX_PROFILE_PIC_HEIGTH = 500

MAX_DISH_PIC_SIZE_KB = 2000
MAX_DISH_PIC_WIDTH = 1000
MAX_DISH_PIC_HEIGTH = 1000


def validate_image_size(image, max_size_kb) -> None:
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"The image must not exceed {max_size_kb} KB")


def validate_image_extension(image) -> None:
    valid_format = [
        "AVIF", 
        "GIF", 
        "JPEG", 
        "JPG", 
        "PNG", 
        "WEBP"
    ]
    
    try:
        img = Image.open(image)
        img.verify()
    except (IOError, SyntaxError):
        raise ValidationError("The uploaded file is not a valid image")
    
    if img.format not in valid_format:
        raise ValidationError('Invalid extension. Allowed extensions are: ' + ', '.join(valid_format))


def validate_image_dimensions(image, max_width, max_height) -> None:
    
    with Image.open(image) as img:
        width, height = img.size
        
        if width > max_width or height > max_height:
            raise ValidationError(f"The maximum image resolution is {max_width}x{max_height}")


def validate_profile_image_size(image) -> None:
    validate_image_size(image, MAX_PROFILE_PIC_SIZE_KB)

def validate_profile_image_dimension(image) -> None:
    validate_image_dimensions(image, MAX_PROFILE_PIC_WIDTH, MAX_PROFILE_PIC_HEIGTH)

def validate_profile_image(image) -> None:
    try:
        validate_image_extension(image)
        validate_profile_image_size(image)
        validate_profile_image_dimension(image)
    except ValidationError as e:
        raise e


def validate_dish_image_size(image) -> None:
    validate_image_size(image, MAX_DISH_PIC_SIZE_KB)

def validate_dish_image_dimension(image) -> None:
    validate_image_dimensions(image, MAX_DISH_PIC_WIDTH, MAX_DISH_PIC_HEIGTH)

def validate_dish_image(image) -> None:
    try:
        validate_image_extension(image)
        validate_dish_image_size(image)
        validate_dish_image_dimension(image)
    except ValidationError as e:
        raise e