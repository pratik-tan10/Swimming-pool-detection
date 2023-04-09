from PIL import Image
import os


def crop_image(img, crop_size, extension = "jpg", output_path = ""):
    # create a directory to save the uploaded files
    if not os.path.exists(os.path.join(output_path, 'uploads', 'cropped')):
        os.makedirs(os.path.join(output_path, 'uploads', 'cropped'))
    
    width, height = img.size
    for i in range(0, width, crop_size):
        for j in range(0, height, crop_size):
            box = (i, j, i + crop_size, j + crop_size)
            cropped_img = img.crop(box)
            filename = f"{i}_{j}.{extension}" # naming convention
            cropped_img.save(os.path.join(output_path, "uploads", "cropped", filename))

# Example usage
#crop_image(img, 640)
