from streamlit.testing.v1 import AppTest
import cv2
from PIL import Image
from PIL import ImageOps
import numpy as np
import os
from streamlit_app.pages.object_detection import process_image, annotate_image


def test_smoke_page_input():
    at = AppTest.from_file('../../streamlit_app/pages/object_detection.py')
    at.run()
    assert not at.exception


def assert_images_equal(img1, img2): #PIL images

    # Convert to same mode and size for comparison
    img2 = img2.convert(img1.mode)
    img2 = img2.resize(img1.size)

    sum_sq_diff = np.sum((np.asarray(img1).astype('float') - np.asarray(img2).astype('float')) ** 2)

    if sum_sq_diff == 0:
        # Images are exactly the same
        pass
    else:
        normalized_sum_sq_diff = sum_sq_diff / np.sqrt(sum_sq_diff)
        assert normalized_sum_sq_diff < 0.001


# def test_annotation_image_similarity():
#     image_input_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "images", "input_dog.jpeg"))
#     image = Image.open(image_input_path)
#     image = np.array(image)
#     detections = process_image(image)
#     processed_opencv_image = annotate_image(image, detections)
#     cv2.imwrite("processed_opencv_image.jpeg", processed_opencv_image)
#     processed_pil_image = Image.fromarray(cv2.cvtColor(processed_opencv_image, cv2.COLOR_BGR2RGB));
#     processed_pil_image.save("process_pil_image.jpeg")
#
#     image_output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "images", "output_annotation_dog.jpeg"))
#     test_output_annotation_image = Image.open(image_output_path)
#     assert_images_equal(processed_pil_image, test_output_annotation_image)
