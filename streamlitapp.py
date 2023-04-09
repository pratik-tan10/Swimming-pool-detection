import streamlit as st
from streamlit_image_comparison import image_comparison
from PIL import Image
import torch
from yolov5 import detect
import numpy as np
from splitImage import crop_image
from stitchImages import stitch_images
import os
import shutil
import tempfile

from normalizeCenters import draw_bb


# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define Streamlit app

def app():
    st.title('YOLOv5 Object Detection')
    st.text('Upload an image and click "Detect" to run object detection')
    # Upload image
    uploaded_file = st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])
    file_save_container = st.empty()

    image_container = st.empty()
    status_container = st.empty()
    
    success = False
    DEMO = False
    image = None
    
    @st.cache_data
    def get_temp_dir():
        return tempfile.TemporaryDirectory().name
    tempdir = get_temp_dir()
    
    if uploaded_file is not None:
        
        # create a directory to save the uploaded files
        if os.path.exists(os.path.join(tempdir, 'uploads')):
            image_container.empty()
            shutil.rmtree(os.path.join(tempdir, 'uploads'))
        
        os.makedirs(os.path.join(tempdir, 'uploads'))
        
        # Delete contents of the upload folder     
        #for each in os.listdir(os.path.join(tempdir, 'uploads')):
        #    os.remove(os.path.join(os.path.join(tempdir, 'uploads', each)))
        
        # need to move further
        with open(os.path.join(tempdir, 'uploads', uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
            extension = uploaded_file.name.split(".")[-1]
            file_save_container.success("File saved")
            # Display original image
            image = Image.open(uploaded_file)
            
            image_container.image(image, caption='Original Image', use_column_width=True)
            if os.path.exists(os.path.join("image_with_bbox.{extension}")):
                os.remove(os.path.join("image_with_bbox.{extension}"))
                os.remove(os.path.join("stitched_image.{extension}"))
                
        
    # Demo Button
    # if (st.button('Show Demo')):
        # DEMO = True
        # image = Image.open('imgs/demo1.jpg')
        # image_container.empty()
        # image_container.image(image, caption='Original Image', use_column_width=True)
        
    print('From outside', type(image), image is None)
    # Run object detection on image
    if (not image is None) and st.button('Detect'):
        print("From st.button:", type(image))
        if os.path.exists(os.path.join(tempdir, "results")):
            shutil.rmtree(os.path.join(tempdir, "results"))
        file_save_container.empty()
        file_save_container.warning("Preprocessing . . .")
        
        status_container.empty()
        status_container.warning("Preprocessing . . .")
        
        # crop images
        crop_image(image, 640, extension = extension, output_path = tempdir)
        file_save_container.empty()
        file_save_container.warning("Running object detection")
        status_container.empty()
        status_container.warning("Running object detection")
        
        results = detect.run(source = os.path.join(tempdir, 'uploads', 'cropped'), weights = 'yolov5/weights/best.pt', view_img = True, save_txt = True, name = os.path.join(tempdir, "results"))
        #results = Image.open(f"yolov5/runs/detect/results/{uploaded_file.name}")
        # Display image with bounding boxes and labels
        #st.image(results, caption='Object Detection', use_column_width=True)
        
        image_container.empty()
        combined = stitch_images(os.path.join(tempdir, "results"), image, tempdir, extension = extension)
        #combined.save(f"stitched_image.{extension}")
        
        # Add swipe effect to compare original image with detection result
        # image_comparison(
        # img2 = image,
        # img1 = combined,
        # label2="Original",
        # label1="Swimming Pools",
        # )
        # status_container.empty()
        # status_container.success("Completed")
        
        file_contents = draw_bb(image, labels_directory = os.path.join(tempdir, "results", "labels"), output_folder = tempdir, extension = extension)

    #success = os.path.exists(os.path.join(tempdir, 'image_with_bbox.jpg')) \
    #and os.path.exists(os.path.join(tempdir, "stitched_image.jpg")) and os.path.exists(os.path.join(tempdir, 'All_boundingBoxes.txt'))
    
    try:
        # Add swipe effect to compare original image with detection result
        image_comparison(
        img2 = image,
        img1 = combined,
        label2="Original",
        label1="Swimming Pools",
        )
        status_container.empty()
        status_container.success("Completed")
    except:    
        try:
            
            img1 = [i for i in os.listdir(os.path.join(tempdir, 'uploads')) if i.contains(".")][0]
            extension = img1.split(".")[-1]
            img1 = os.path.join(tempdir, 'uploads', img1)
            img2 = os.path.join(tempdir, f"stitched_image.{extension}")
            print("from firsty try block", img1, img2)
            
            image_comparison(
            img2 = img1,
            img1 = img2,
            label2="Original",
            label1="Swimming Pools",
            )
            
            image_container.empty()
        except:
            pass
        
    #if success:
    print(tempdir)
    try:
        with open(os.path.join(tempdir, 'All_boundingBoxes.txt'), 'r') as fp:
            st.download_button(
            label="Download Bounding Box",
            data = fp,
            file_name="string.txt",
            mime="text/plain"
            )
        
        with open(os.path.join(tempdir, f"image_with_bbox.{extension}"), "rb") as fp:
            btn = st.download_button(
                label="Download IMAGE with Boundingbox only",
                data=fp,
                file_name=f"image_with_bbox.{extension}",
                mime=f"image/{extension}"
            )
            
        with open(os.path.join(tempdir, f"stitched_image.{extension}"), "rb") as fp:
            btn2 = st.download_button(
                label="Download IMAGE with Boundingbox and labels",
                data=fp,
                file_name=f"stitched_image.{extension}",
                mime=f"image/{extension}"
            )
    except:
        pass
    

# Run Streamlit app
if __name__ == '__main__':
    app()