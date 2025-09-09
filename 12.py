import streamlit as st
from PIL import Image
import google.generativeai as genai
import io


API_KEY = "AIzaSyBnV45TBfOt3nNLIfTG-BWIdQIWec6Tn18"
genai.configure(api_key=API_KEY)


st.set_page_config(page_title="🌱 Plant Detector ", page_icon="🧟", layout="centered")
st.title("🌱 Plant Disease Detection ")
st.write("Upload a leaf/crop image, and we will identify the plant type and give a short description.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        [
            {"mime_type": "image/png", "data": img_bytes},
            """You are a plant identification assistant. 
            Identify the plant and disease (if any) from the image. 
            Respond in JSON format like this:
            {
              "Plant": "Plant Name",
              "Description": "One short line about the plant",
              "Disease": "Disease Name or 'Healthy'",
              "Treatment": "One short treatment (if diseased)"
            }"""
        ]
    )

    st.subheader("🔍Prediction")

    st.write(response.text)
else:
    st.info("👆 Upload an image to get started.")
