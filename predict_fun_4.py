from PIL import Image
import numpy as np
import pickle
from tensorflow.keras.models import load_model

model = load_model(r'C:\xampp\htdocs\mahmoud\cnn_model.h5')
# Load the class names
with open(r'C:\xampp\htdocs\mahmoud\class_indices.pkl', 'rb') as f:
    class_indices = pickle.load(f)

# Get the class names
class_names = list(class_indices.keys())

def predict_from_image_object(img: Image):
    # Resize the image to match the model's input shape
    img = img.resize((150, 150))
    # Convert the image to a numpy array
    img_array = np.array(img)

    # Normalize the image
    img_array = img_array / 255

    # Add a dimension to the image to match the model's input shape
    img_array = np.expand_dims(img_array, axis=0)

    # Use the model to make a prediction
    predictions = model.predict(img_array)

    # Get the index of the class with the highest probability
    class_index = np.argmax(predictions)

    # Get the class name
    class_name = class_names[class_index]

    return class_name