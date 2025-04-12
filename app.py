
import streamlit as st
import tempfile
import cv2
import numpy as np
import tensorflow as tf
from utils.video_processing import process_video
from utils.email_alert import send_email_alert
import os

# Load the trained model
model = tf.keras.models.load_model('best_violence_model.h5')

# Set page config
st.set_page_config(page_title="Violence Detection App", layout="wide")

# Custom CSS
with open('static/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Violence Detection in Video")
st.markdown("Upload a video to detect violence scenes.")

email = st.text_input("Enter your Email to get Alert on Violence Detection:")

uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])

if uploaded_file and email:
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    st.video(uploaded_file)

    st.write("Analyzing video, please wait...")
    violence_timestamps = process_video(video_path, model)

    if violence_timestamps:
        st.error("Violence Detected!")
        st.write("Violence found at these timestamps (in seconds):")
        st.write(violence_timestamps)

        # Send email
        send_email_alert(email, violence_timestamps)

        st.success(f"Alert email sent to {email}")
    else:
        st.success("No Violence Detected!")

