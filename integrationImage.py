import sys
import base64
import cv2
import numpy as np
from PIL import Image
import json
import requests
import OneImageV3withResize as pre
import predict_fun_4 as pf4

def predict(filename):
    # Initialize prediction variable
    prediction = None

    # Read the image file
    image = cv2.imread(filename)

    textReader = pre.pipline()

    # Preprocess the image
    preprocessed_image_1 = pre.PreProcessing(image)
    preprocessed_image_2 = pre.fix180RotationDegree(textReader,preprocessed_image_1)

    # Check if the preprocessing function found a region of interest
    if preprocessed_image_2 is not None:
        # Convert the OpenCV image to a PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(preprocessed_image_2, cv2.COLOR_BGR2RGB))

        # Predict the currency
        prediction = pf4.predict_from_image_object(pil_image)
    else:
        prediction = 0

    prediction = json.dumps(prediction)

    """ # Send the prediction back to the API
    response = requests.post('http://localhost/mahmoud/function_2.py', json={'prediction': prediction})"""
    return prediction

if __name__ == "__main__":
    # Get the filename from the command line arguments
    filename = sys.argv[1]

    # Call the predict function
    prediction = predict(filename)

    # Convert the prediction to JSON and print it
    #prediction = json.dumps(prediction)
    print(prediction)