from PIL import Image
import os
import math

#main_image = Image.open("LargeImage.jpg")
#stitched_size = (math.ceil(main_image.size[0]/640.0), math.ceil(main_image.size[1]/640.0))
def stitch_images(input_dir, main_image, output_path = "", extension = "jpg"):
    files = [i for i in os.listdir(input_dir) if i.endswith(f'.{extension}')]
    print(len(files))

    #stitched_size = main_image.size
    stitched_image = Image.new("RGB", main_image.size)
    for i, image in enumerate(files):
        coords = list(map(int, image.replace(f'.{extension}', '').split('_')[:2]))
        with Image.open(os.path.join(input_dir, image)) as img:
            stitched_image.paste(img, (coords[0], coords[1]))
    
    box = (0, 0, main_image.size[0], main_image.size[1])
    stitched_image = stitched_image.crop(box)
    stitched_image.save(os.path.join(output_path, f"stitched_image.{extension}"))
    return stitched_image
    

# Example usage
#stitch_images("uploads", "stitched_image.jpg")
