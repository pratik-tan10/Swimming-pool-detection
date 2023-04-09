import os
from PIL import Image, ImageDraw

def normalize_centers(directory, img_size, verbose = False, output_folder = ''):
    #os.chdir(directory)
    raw_centers = [i for i in os.listdir(directory) if i.endswith('.txt')]
    X0, Y0 = img_size
    All_bbs = []
    for each in raw_centers:
        # Get the coordinate of top-left from file name
        X, Y = list(map(int, each.replace('.txt', '').split('_')))
        
        # Open the text file
        with open(os.path.join(directory, each), 'r') as f:
            lines = f.read().strip().split('\n')
            for line in lines:
                # get the feature id, x, y center, widht and height
                o, x,y,w,h = list(map(float, line.strip().split(" ")))
                
                # convert the x, y centers to absolute pixel location based on main image
                All_bbs.append([int(o), (X+x*640)/X0, (Y + y*640)/Y0,w*640/X0,h*640/Y0])
    
    with open(os.path.join(output_folder, 'All_boundingBoxes.txt'), 'w') as file:
        file.writelines([" ".join([str(nums)[:6] for nums in bb])+'\n' for bb in All_bbs])
    
    if verbose: print(f"file saved at {os.path.join(os.getcwd(), 'All_boundingBoxes.txt')}")
    text = "".join([" ".join([str(nums)[:6] for nums in bb])+'\n' for bb in All_bbs])
    return(All_bbs, text)

def draw_bb(main_image, labels_directory = r"yolov5\runs\detect\results\labels", verbose = False, name = 'image_with_bbox', output_folder = "", extension = ".jpg"):

    #main_image = Image.open("LargeImage.jpg")

    # Create a PIL ImageDraw object
    draw = ImageDraw.Draw(main_image)

    img_size = main_image.size
    BBs, text = normalize_centers(labels_directory, img_size, output_folder = output_folder)

    # Get the image dimensions
    image_width, image_height = main_image.size

    for _, x_center_norm, y_center_norm, width_norm, height_norm in BBs:
        # Calculate the pixel coordinates of the bounding box
        x_center = int(x_center_norm * image_width)
        y_center = int(y_center_norm * image_height)
        width = int(width_norm * image_width)
        height = int(height_norm * image_height)
        x_min = x_center - width // 2
        y_min = y_center - height // 2
        x_max = x_center + width // 2
        y_max = y_center + height // 2

        # Draw the bounding box on the image
        draw.rectangle([x_min, y_min, x_max, y_max], outline='red', width = 10)

    # Save the modified image
    main_image.save(os.path.join(output_folder, f"{name}.{extension}"))
    if verbose: print("Image saved at", os.path.join(os.getcwd(), 'image_with_bbox.jpg'))
    return text
	