import os
from PIL import Image
from django.core.exceptions import ValidationError


def validate_image_size(image):
    max_size_kb = 500  
    
    if image.size > max_size_kb * 1024:
        raise ValidationError(f"The image must not exceed {max_size_kb} KB")


def validate_image_extension(image):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(image.name)[1]
    
    if ext.lower() not in valid_extensions:
        raise ValidationError('Invalid extension. Allowed extensions are: ' + ', '.join(valid_extensions))


def validate_image_dimensions(image):
    max_width = 500
    max_height = 500
    
    with Image.open(image) as img:
        width, height = img.size
        
        if width > max_width or height > max_height:
            raise ValidationError(f"The maximum image resolution is {max_width}x{max_height}")
