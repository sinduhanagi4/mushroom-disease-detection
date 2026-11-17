
import os
import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from pathlib import Path

# --------------------------------------------------
# 1. PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MODEL_PATH = Path(__file__).parent / "mushroom_disease_mobilenetv2.keras"

# --------------------------------------------------
# 2. LANGUAGE SELECTION
# --------------------------------------------------

if "language" not in st.session_state:
    st.session_state.language = "English"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f0fdf4, #ecfdf5);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .hero {
        background: linear-gradient(120deg, #064e3b, #047857, #10b981);
        padding: 42px 35px;
        border-radius: 24px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        font-weight: 800;
    }

    .hero p {
        color: #ecfdf5;
        font-size: 16px;
    }

    .small-badge {
        background: rgba(255,255,255,0.18);
        display: inline-block;
        padding: 7px 15px;
        border-radius: 30px;
        font-size: 13px;
        margin-bottom: 12px;
    }

    .info-card {
        background: white;
        border: 1px solid #d1fae5;
        border-radius: 17px;
        padding: 20px;
        min-height: 135px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .info-card h3 {
        color: #065f46;
        font-size: 18px;
    }

    .info-card p {
        color: #475569;
        font-size: 14px;
    }

    .section-title {
        color: #065f46;
        font-size: 25px;
        font-weight: 700;
        margin-top: 25px;
    }

    .advice-card {
        background: #ecfdf5;
        border-left: 5px solid #059669;
        padding: 18px;
        border-radius: 10px;
        margin-top: 12px;
    }

    footer {
        text-align: center;
        color: #64748b;
        padding: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Language selector at the top
language_options = ["English", "ಕನ್ನಡ"]

selected_language = st.radio(
    "🌐 Select Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    language_options,
    horizontal=True,
    index=0 if st.session_state.language == "English" else 1
)

st.session_state.language = (
    "English" if selected_language == "English" else "Kannada"
)

EN = st.session_state.language == "English"

# --------------------------------------------------
# 3. TEXT TRANSLATIONS
# --------------------------------------------------

if EN:
    page_title = "Mushroom AI Assistant"
    subtitle = "Smart Mushroom Disease Detection & Farmer Support"
    dashboard_title = "🌿 Smart Farming Dashboard"
    upload_title = "🔬 AI Mushroom Disease Detection"
    upload_help = "Upload a clear mushroom image to identify its condition."
    upload_label = "Choose a mushroom image"
    predict_button = "🔍 Predict Mushroom Disease"
    chatbot_title = "🤖 Farmer Assistant"
    chatbot_help = "Ask a question about mushroom health or cultivation."
    how_title = "🌱 How It Works"
    footer_text = "AI Based Mushroom Disease Detection | Farmer Support System"
    welcome = "Welcome! Upload a mushroom image to begin disease detection."
else:
    page_title = "ಮಶ್ರೂಮ್ AI ಸಹಾಯಕ"
    subtitle = "ಸ್ಮಾರ್ಟ್ ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ ಮತ್ತು ರೈತರಿಗೆ ಸಹಾಯ"
    dashboard_title = "🌿 ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್"
    upload_title = "🔬 AI ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ"
    upload_help = "ಮಶ್ರೂಮ್ ಚಿತ್ರದ ಮೂಲಕ ಅದರ ಸ್ಥಿತಿಯನ್ನು ಗುರುತಿಸಿ."
    upload_label = "ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ"
    predict_button = "🔍 ಮಶ್ರೂಮ್ ರೋಗವನ್ನು ಪತ್ತೆಹಚ್ಚಿ"
    chatbot_title = "🤖 ರೈತ ಸಹಾಯಕ"
    chatbot_help = "ಮಶ್ರೂಮ್ ಆರೋಗ್ಯ ಅಥವಾ ಕೃಷಿಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ."
    how_title = "🌱 ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ"
    footer_text = "AI ಆಧಾರಿತ ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ"
    welcome = "ಸ್ವಾಗತ! ರೋಗ ಪತ್ತೆ ಮಾಡಲು ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."

# --------------------------------------------------
# 4. HERO SECTION
# --------------------------------------------------

st.markdown(
    f"""
    <div class="hero">
        <div class="small-badge">
            🌱 AI Powered Agriculture • Smart Farming
        </div>
        <h1>🍄 {page_title}</h1>
        <p>{subtitle}</p>
        <p>
            Identify common mushroom diseases using deep learning
            and receive farmer-friendly guidance.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(welcome)

# --------------------------------------------------
# 5. DASHBOARD
# --------------------------------------------------

st.markdown(
    f'<div class="section-title">{dashboard_title}</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <h3>🔬 Disease Detection</h3>
            <p>Identify mushroom diseases from uploaded images.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <h3>🌱 Farmer Guidance</h3>
            <p>Get basic information and suggested precautions.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <h3>🌐 Two Languages</h3>
            <p>Use the application in English or Kannada.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="info-card">
            <h3>🤖 Farmer Assistant</h3>
            <p>Ask common questions about mushroom cultivation.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# 6. DISEASE CLASSES AND FARMER ADVICE
# --------------------------------------------------

class_names = [
    "Healthy",
    "Bacterial Blotch",
    "Dry Bubble",
    "Cobweb Disease",
    "Wet Bubble"
]

kannada_names = {
    "Healthy": "ಆರೋಗ್ಯಕರ",
    "Bacterial Blotch": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್",
    "Dry Bubble": "ಡ್ರೈ ಬಬಲ್",
    "Cobweb Disease": "ಕಾಬ್‌ವೆಬ್ ರೋಗ",
    "Wet Bubble": "ವೆಟ್ ಬಬಲ್"
}

advice_english = {
    "Healthy": [
        "The mushroom is classified as healthy by the model.",
        "Continue maintaining clean growing conditions.",
        "Monitor the crop regularly for any unusual changes."
    ],
    "Bacterial Blotch": [
        "Avoid excess moisture on mushroom caps.",
        "Maintain suitable ventilation in the growing room.",
        "Keep equipment and surfaces clean.",
        "Remove affected mushrooms carefully and seek expert advice."
    ],
    "Dry Bubble": [
        "Remove affected mushrooms carefully.",
        "Clean tools and growing-room surfaces.",
        "Avoid spreading contaminated material.",
        "Consult a mushroom cultivation expert for treatment advice."
    ],
    "Cobweb Disease": [
        "Remove affected material carefully.",
        "Improve air circulation where appropriate.",
        "Maintain cleanliness in the growing area.",
        "Seek advice from an agricultural expert."
    ],
    "Wet Bubble": [
        "Remove affected mushrooms and contaminated material carefully.",
        "Clean and disinfect tools and surfaces appropriately.",
        "Avoid moving contaminated material around the growing room.",
        "Consult an agricultural expert for further guidance."
    ]
}

advice_kannada = {
    "Healthy": [
        "ಮಶ್ರೂಮ್ ಆರೋಗ್ಯಕರವಾಗಿದೆ ಎಂದು ಮಾದರಿ ಗುರುತಿಸಿದೆ.",
        "ಬೆಳೆಸುವ ಸ್ಥಳವನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.",
        "ಬೆಳೆಯನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
    ],
    "Bacterial Blotch": [
        "ಮಶ್ರೂಮ್ ಮೇಲ್ಭಾಗದಲ್ಲಿ ಹೆಚ್ಚಿನ ತೇವಾಂಶ ಇರದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.",
        "ಬೆಳೆಸುವ ಕೋಣೆಯಲ್ಲಿ ಸೂಕ್ತ ಗಾಳಿಯ ಸಂಚಾರ ಇರಲಿ.",
        "ಉಪಕರಣಗಳು ಮತ್ತು ಮೇಲ್ಮೈಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.",
        "ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
    ],
    "Dry Bubble": [
        "ಬಾಧಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ.",
        "ಉಪಕರಣಗಳು ಮತ್ತು ಕೋಣೆಯನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.",
        "ಸೋಂಕಿತ ವಸ್ತು ಹರಡದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.",
        "ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
    ],
    "Cobweb Disease": [
        "ಬಾಧಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ.",
        "ಸೂಕ್ತ ಗಾಳಿಯ ಸಂಚಾರವನ್ನು ಕಾಪಾಡಿ.",
        "ಬೆಳೆಸುವ ಸ್ಥಳವನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.",
        "ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
    ],
    "Wet Bubble": [
        "ಬಾಧಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ.",
        "ಉಪಕರಣಗಳು ಮತ್ತು ಮೇಲ್ಮೈಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ.",
        "ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ಬೇರೆಡೆಗೆ ಹರಡಿಸಬೇಡಿ.",
        "ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
    ]
}

# --------------------------------------------------
# 7. LAZY MODEL LOADING
# --------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_mushroom_model(model_path):
    # TensorFlow is imported only when prediction is requested.
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

    import tensorflow as tf

    try:
        tf.config.threading.set_intra_op_parallelism_threads(2)
        tf.config.threading.set_inter_op_parallelism_threads(2)
    except Exception:
        pass

    model = tf.keras.models.load_model(model_path, compile=False)
    return model

# --------------------------------------------------
# 8. IMAGE UPLOAD AND PREDICTION
# --------------------------------------------------

st.markdown(
    f'<div class="section-title">{upload_title}</div>',
    unsafe_allow_html=True
)

st.write(upload_help)

uploaded_file = st.file_uploader(
    upload_label,
    type=["jpg", "jpeg", "png"],
    key="mushroom_image"
)

if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file)
        image = ImageOps.exif_transpose(image).convert("RGB")

        left, right = st.columns(2)

        with left:
            st.image(
                image,
                caption="Uploaded Mushroom Image",
                use_container_width=True
            )

        with right:
            st.write("### Image Information")
            st.write("Image format:", uploaded_file.type)
            st.write("Image size:", image.size)

        if st.button(predict_button, type="primary"):

            if not MODEL_PATH.exists():
                st.error(
                    "Model file not found. Please check that "
                    "mushroom_disease_mobilenetv2.keras is in your GitHub repository."
                )

            else:
                try:
                    with st.spinner(
                        "Loading the AI model and analysing the image..."
                    ):
                        model = load_mushroom_model(str(MODEL_PATH))

                        resized_image = image.resize((224, 224))

                        image_array = np.array(
                            resized_image,
                            dtype=np.float32
                        )

                        image_array = image_array / 255.0
                        image_array = np.expand_dims(image_array, axis=0)

                        predictions = model.predict(
                            image_array,
                            verbose=0
                        )

                        predicted_index = int(
                            np.argmax(predictions[0])
                        )

                        confidence = float(
                            predictions[0][predicted_index]
                        ) * 100

                        predicted_class = class_names[predicted_index]

                    st.success("Prediction completed successfully!")

                    st.markdown("### 🍄 Prediction Result")

                    if EN:
                        st.subheader(
                            f"Detected Category: {predicted_class}"
                        )
                    else:
                        st.subheader(
                            f"ಪತ್ತೆಯಾದ ವರ್ಗ: "
                            f"{kannada_names[predicted_class]}"
                        )

                    st.metric(
                        "Model Confidence" if EN else "ಮಾದರಿಯ ವಿಶ್ವಾಸ ಮಟ್ಟ",
                        f"{confidence:.2f}%"
                    )

                    st.progress(
                        min(max(confidence / 100, 0.0), 1.0)
                    )

                    st.markdown("### 🌱 Farmer Advice")

                    advice_list = (
                        advice_english[predicted_class]
                        if EN
                        else advice_kannada[predicted_class]
                    )

                    st.markdown(
                        '<div class="advice-card">',
                        unsafe_allow_html=True
                    )

                    for advice in advice_list:
                        st.write("• " + advice)

                    st.markdown("</div>", unsafe_allow_html=True)

                    st.caption(
                        "This is an AI prediction, not a laboratory diagnosis. "
                        "Consult an agricultural expert before taking treatment decisions."
                        if EN else
                        "ಇದು AI ಆಧಾರಿತ ಅಂದಾಜು ಮಾತ್ರ. ಚಿಕಿತ್ಸಾ ನಿರ್ಧಾರಕ್ಕೆ ಮೊದಲು ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
                    )

                except Exception as error:
                    st.error(
                        "Prediction failed. Please check the model file "
                        "and application logs."
                    )
                    st.exception(error)

    except Exception:
        st.error(
            "Unable to read this image. Please upload a valid JPG or PNG image."
        )

# --------------------------------------------------
# 9. SUPPORTED DISEASES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🍄 Supported Mushroom Categories</div>',
    unsafe_allow_html=True
)

disease_columns = st.columns(5)

for index, disease in enumerate(class_names):
    with disease_columns[index]:
        display_name = (
            disease if EN else kannada_names[disease]
        )
        st.markdown(
            f"""
            <div class="info-card">
                <h3>{index + 1}. {display_name}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# 10. HOW IT WORKS
# --------------------------------------------------

st.markdown(
    f'<div class="section-title">{how_title}</div>',
    unsafe_allow_html=True
)

step1, step2, step3, step4 = st.columns(4)

if EN:
    steps = [
        ("📷 Step 1", "Upload a mushroom image."),
        ("🖼️ Step 2", "Image is resized to 224 × 224 pixels."),
        ("🧠 Step 3", "MobileNetV2 analyses image features."),
        ("📊 Step 4", "The predicted category is displayed.")
    ]
else:
    steps = [
        ("📷 ಹಂತ 1", "ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."),
        ("🖼️ ಹಂತ 2", "ಚಿತ್ರವನ್ನು 224 × 224 ಗಾತ್ರಕ್ಕೆ ಬದಲಾಯಿಸಲಾಗುತ್ತದೆ."),
        ("🧠 ಹಂತ 3", "MobileNetV2 ಚಿತ್ರದ ಲಕ್ಷಣಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ."),
        ("📊 ಹಂತ 4", "ರೋಗದ ವರ್ಗವನ್ನು ತೋರಿಸಲಾಗುತ್ತದೆ.")
    ]

for column, step in zip([step1, step2, step3, step4], steps):
    with column:
        st.markdown(
            f"""
            <div class="info-card">
                <h3>{step[0]}</h3>
                <p>{step[1]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# --------------------------------------------------
# 11. RULE-BASED FARMER ASSISTANT
# --------------------------------------------------

st.markdown(
    f'<div class="section-title">{chatbot_title}</div>',
    unsafe_allow_html=True
)

st.write(chatbot_help)

def farmer_answer(question, english=True):
    q = question.lower()

    if any(word in q for word in ["hello", "hi", "ನಮಸ್ಕಾರ"]):
        return (
            "Hello! How can I help you with mushroom cultivation?"
            if english else
            "ನಮಸ್ಕಾರ! ಮಶ್ರೂಮ್ ಕೃಷಿಯಲ್ಲಿ ನಾನು ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?"
        )

    if any(word in q for word in ["healthy", "ಆರೋಗ್ಯ"]):
        return (
            "Healthy mushrooms should be grown in clean conditions. "
            "Monitor them regularly."
            if english else
            "ಆರೋಗ್ಯಕರ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಸ್ವಚ್ಛ ಪರಿಸರದಲ್ಲಿ ಬೆಳೆಸಿ. ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
        )

    if any(word in q for word in ["blotch", "ಬ್ಲಾಚ್"]):
        return (
            "For bacterial blotch, avoid excess moisture, maintain ventilation "
            "and clean the growing area."
            if english else
            "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್ ಸಮಸ್ಯೆಗೆ ಹೆಚ್ಚಿನ ತೇವಾಂಶ ತಪ್ಪಿಸಿ ಮತ್ತು ಸ್ಥಳವನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ."
        )

    if any(word in q for word in ["dry bubble", "ಡ್ರೈ ಬಬಲ್"]):
        return (
            "Remove affected mushrooms carefully, clean tools and consult "
            "a mushroom cultivation expert."
            if english else
            "ಬಾಧಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ, ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ."
        )

    if any(word in q for word in ["cobweb", "ಕಾಬ್"]):
        return (
            "Remove affected material carefully, maintain cleanliness "
            "and seek expert advice."
            if english else
            "ಬಾಧಿತ ವಸ್ತುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ, ಸ್ವಚ್ಛತೆ ಕಾಪಾಡಿ ಮತ್ತು ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
        )

    if any(word in q for word in ["wet bubble", "ವೆಟ್ ಬಬಲ್"]):
        return (
            "Remove affected material carefully and disinfect tools and surfaces "
            "appropriately. Consult an expert."
            if english else
            "ಬಾಧಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ."
        )

    if any(word in q for word in ["water", "moisture", "ತೇವಾಂಶ", "ನೀರು"]):
        return (
            "Maintain suitable humidity and avoid excess water on mushroom caps. "
            "Follow the recommended conditions for your mushroom variety."
            if english else
            "ಸೂಕ್ತ ತೇವಾಂಶ ಕಾಪಾಡಿ. ಮಶ್ರೂಮ್ ಮೇಲ್ಭಾಗದಲ್ಲಿ ಹೆಚ್ಚಿನ ನೀರು ಇರದಂತೆ ನೋಡಿಕೊಳ್ಳಿ."
        )

    if any(word in q for word in ["temperature", "ತಾಪಮಾನ"]):
        return (
            "The suitable temperature depends on the mushroom variety and "
            "growing stage. Follow a reliable cultivation guide."
            if english else
            "ಸೂಕ್ತ ತಾಪಮಾನವು ಮಶ್ರೂಮ್ ತಳಿ ಮತ್ತು ಬೆಳವಣಿಗೆಯ ಹಂತವನ್ನು ಅವಲಂಬಿಸಿರುತ್ತದೆ."
        )

    if any(word in q for word in ["disease", "ರೋಗ"]):
        return (
            "Upload a clear mushroom image in the Disease Detection section. "
            "The model can classify five categories."
            if english else
            "ರೋಗ ಪತ್ತೆ ವಿಭಾಗದಲ್ಲಿ ಸ್ಪಷ್ಟವಾದ ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
        )

    return (
        "I can provide basic guidance about mushroom health, diseases, "
        "cleanliness and cultivation. Please ask a specific question."
        if english else
        "ಮಶ್ರೂಮ್ ಆರೋಗ್ಯ, ರೋಗಗಳು, ಸ್ವಚ್ಛತೆ ಮತ್ತು ಕೃಷಿಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ."
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_question = st.chat_input(
    "Ask your mushroom farming question..."
    if EN else
    "ಮಶ್ರೂಮ್ ಕೃಷಿಯ ಬಗ್ಗೆ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
)

if user_question:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_question}
    )

    answer = farmer_answer(user_question, EN)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()

# --------------------------------------------------
# 12. OPTIONAL VOICE ASSISTANT
# --------------------------------------------------

st.markdown("### 🎤 Voice Farmer Assistant")

try:
    from streamlit_mic_recorder import speech_to_text
    from gtts import gTTS
    from io import BytesIO

    voice_language = "en" if EN else "kn"

    spoken_question = speech_to_text(
        language="en-US" if EN else "kn-IN",
        just_once=True,
        key="voice_input"
    )

    if spoken_question:
        st.write("You said:", spoken_question)

        spoken_answer = farmer_answer(spoken_question, EN)

        st.write("Assistant:", spoken_answer)

        audio_buffer = BytesIO()

        tts = gTTS(
            text=spoken_answer,
            lang=voice_language
        )

        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        st.audio(
            audio_buffer,
            format="audio/mp3"
        )

except ImportError:
    st.info(
        "Voice assistant packages are not installed. "
        "You can still use the text Farmer Assistant."
    )

except Exception:
    st.info(
        "Voice input is not available in this browser. "
        "Please use the text Farmer Assistant."
    )

# --------------------------------------------------
# 13. FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    f"""
    <footer>
        <h4>🍄 Mushroom AI Assistant</h4>
        <p>{footer_text}</p>
        <p>Developed using Python, TensorFlow, MobileNetV2 and Streamlit.</p>
    </footer>
    """,
    unsafe_allow_html=True
)
