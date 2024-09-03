# Health Management APP
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load all the environment variables
load_dotenv()

# Configure the API key for google.generativeai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_image, prompt):
    # Update the model to the newer version
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app
input_prompt = """
You are an expert pharmaceutical/Chemist where you need to see the tablets from the image 
and also provide the details of every drug/tablet item with the below format:

1. Examine the image carefully and identify the tablets depicted.
2. Describe the uses and functionalities of each tablet shown in the image.
3. Provide information on the intended purposes, features, and typical applications of the tablets.
4. If possible, include any notable specifications or distinguishing characteristics of each tablet.
5. Ensure clarity and conciseness in your descriptions, focusing on key details and distinguishing factors.
----
"""
# Set the page configuration for Streamlit
st.set_page_config(page_title="AI Chemist App")

# App header
st.header("AI Chemist App")

# Input prompt and file uploader
user_input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Tell me")

# If submit button is clicked
if submit and uploaded_file is not None:
    try:
        image_data = input_image_setup(uploaded_file)
        prompt = input_prompt + user_input  # Combine the base prompt with the user input
        response = get_gemini_response(image_data, prompt)  # Call with the updated model
        st.subheader("The Response is")
        st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    if not uploaded_file:
        st.warning("Please upload an image to proceed.")
