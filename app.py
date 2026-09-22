
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# -----------------------------
# Load trained model
# -----------------------------
model = tf.keras.models.load_model("mushroom_disease_mobilenetv2.keras")

class_names = [
    "Healthy",
    "Bacterial Blotch",
    "Dry Bubble",
    "Cobweb",
    "Wet Bubble"
]

# -----------------------------
# Disease information
# -----------------------------
disease_info = {

    "Healthy": {
        "en": "The mushroom appears healthy according to the AI model.",
        "kn": "AI ಮಾದರಿಯ ಪ್ರಕಾರ ಅಣಬೆ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತದೆ."
    },

    "Bacterial Blotch": {
        "en": "Bacterial Blotch is a disease that can cause brown or yellowish spots on mushrooms.",
        "kn": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್ ಅಣಬೆಗಳ ಮೇಲೆ ಕಂದು ಅಥವಾ ಹಳದಿ ಬಣ್ಣದ ಕಲೆಗಳನ್ನು ಉಂಟುಮಾಡುವ ರೋಗವಾಗಿದೆ."
    },

    "Dry Bubble": {
        "en": "Dry Bubble is a fungal disease that can affect mushroom development and appearance.",
        "kn": "ಡ್ರೈ ಬಬಲ್ ಅಣಬೆಗಳ ಬೆಳವಣಿಗೆ ಮತ್ತು ರೂಪವನ್ನು ಪರಿಣಾಮಗೊಳಿಸಬಹುದಾದ ಶಿಲೀಂಧ್ರ ರೋಗವಾಗಿದೆ."
    },

    "Cobweb": {
        "en": "Cobweb is a fungal disease that may produce a web-like growth around mushrooms.",
        "kn": "ಕಾಬ್‌ವೆಬ್ ಅಣಬೆಗಳ ಸುತ್ತ ಜಾಲದಂತಿರುವ ಬೆಳವಣಿಗೆಯನ್ನು ಉಂಟುಮಾಡಬಹುದಾದ ಶಿಲೀಂಧ್ರ ರೋಗವಾಗಿದೆ."
    },

    "Wet Bubble": {
        "en": "Wet Bubble is a fungal disease that can affect mushroom growth and produce abnormal wet-looking symptoms.",
        "kn": "ವೆಟ್ ಬಬಲ್ ಅಣಬೆಗಳ ಬೆಳವಣಿಗೆಯನ್ನು ಪರಿಣಾಮಗೊಳಿಸಬಹುದಾದ ಶಿಲೀಂಧ್ರ ರೋಗವಾಗಿದ್ದು, ಅಸಹಜ ತೇವದಂತಹ ಲಕ್ಷಣಗಳನ್ನು ಉಂಟುಮಾಡಬಹುದು."
    }
}

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Mushroom Disease Detection",
    page_icon="🍄",
    layout="centered"
)

# -----------------------------
# Language selection
# -----------------------------
st.title("🍄 Mushroom Disease Detection")
st.subheader("ಅಣಬೆ ರೋಗ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ")

language = st.radio(
    "Choose Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    ["English", "ಕನ್ನಡ"],
    horizontal=True
)

# -----------------------------
# Introduction
# -----------------------------
if language == "English":
    st.write(
        "Upload a clear photograph of a mushroom. "
        "The AI model will classify the image into one of five classes."
    )
else:
    st.write(
        "ಅಣಬೆಯ ಸ್ಪಷ್ಟವಾದ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ. "
        "AI ಮಾದರಿಯು ಚಿತ್ರವನ್ನು ಐದು ವರ್ಗಗಳಲ್ಲಿ ಒಂದಾಗಿ ಗುರುತಿಸುತ್ತದೆ."
    )

# -----------------------------
# Image upload
# -----------------------------
if language == "English":
    upload_text = "📷 Upload Mushroom Image"
else:
    upload_text = "📷 ಅಣಬೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"

uploaded_file = st.file_uploader(
    upload_text,
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # -----------------------------
    # Display image
    # -----------------------------
    image = Image.open(uploaded_file).convert("RGB")

    if language == "English":
        st.image(
            image,
            caption="Uploaded Mushroom Image",
            use_container_width=True
        )
    else:
        st.image(
            image,
            caption="ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಅಣಬೆಯ ಚಿತ್ರ",
            use_container_width=True
        )

    # -----------------------------
    # Preprocessing
    # -----------------------------
    image_resized = image.resize((224, 224))
    image_array = np.array(image_resized) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # -----------------------------
    # Prediction
    # -----------------------------
    prediction = model.predict(image_array, verbose=0)

    predicted_class = np.argmax(prediction[0])
    predicted_name = class_names[predicted_class]
    confidence = prediction[0][predicted_class] * 100

    # -----------------------------
    # Result
    # -----------------------------
    if language == "English":
        st.header("🔍 Prediction Result")

        st.success(
            f"Predicted Class: {predicted_name}"
        )

        st.info(
            f"Model Confidence: {confidence:.2f}%"
        )

        st.subheader("📖 About the Result")

        st.write(
            disease_info[predicted_name]["en"]
        )

        st.warning(
            "⚠️ This is an AI-assisted prediction. "
            "Please consult an agricultural expert before taking treatment decisions."
        )

    else:
        st.header("🔍 ಫಲಿತಾಂಶ")

        st.success(
            f"ಗುರುತಿಸಲಾದ ವರ್ಗ: {predicted_name}"
        )

        st.info(
            f"AI ಮಾದರಿಯ ವಿಶ್ವಾಸ ಮಟ್ಟ: {confidence:.2f}%"
        )

        st.subheader("📖 ಫಲಿತಾಂಶದ ಮಾಹಿತಿ")

        st.write(
            disease_info[predicted_name]["kn"]
        )

        st.warning(
            "⚠️ ಇದು AI ಆಧಾರಿತ ಸಹಾಯಕ ಫಲಿತಾಂಶವಾಗಿದೆ. "
            "ಚಿಕಿತ್ಸೆ ಅಥವಾ ನಿಯಂತ್ರಣ ಕ್ರಮಗಳನ್ನು ಕೈಗೊಳ್ಳುವ ಮೊದಲು ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
        )

# -----------------------------
# Footer
# -----------------------------
st.divider()

if language == "English":
    st.caption(
        "🍄 AI-Based Mushroom Disease Detection | "
        "MobileNetV2 Deep Learning Model"
    )
else:
    st.caption(
        "🍄 AI ಆಧಾರಿತ ಅಣಬೆ ರೋಗ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ | "
        "MobileNetV2 ಡೀಪ್ ಲರ್ನಿಂಗ್ ಮಾದರಿ"
    )
