import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Mushroom Disease Detection",
    page_icon="🍄",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #f6fff8;
}

.hero {
    background: linear-gradient(135deg, #0f9d58, #34c759);
    padding: 40px;
    border-radius: 25px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.dashboard-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    min-height: 170px;
}

.result-card {
    background: linear-gradient(135deg, #e8f5e9, #ffffff);
    padding: 30px;
    border-radius: 25px;
    border-left: 8px solid #0f9d58;
    margin-top: 20px;
}

.advice-card {
    background: #fff8e1;
    padding: 25px;
    border-radius: 20px;
    border-left: 8px solid #ffb300;
    margin-top: 20px;
}

.section-title {
    color: #137333;
    font-size: 30px;
    font-weight: bold;
    margin-top: 30px;
    margin-bottom: 20px;
}

.disease-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
    text-align: center;
    min-height: 140px;
}

.footer {
    text-align: center;
    padding: 30px;
    color: #666;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LANGUAGE SELECTION
# ==================================================

language = st.radio(
    "Language",
    ["🇬🇧 English", "🇮🇳 ಕನ್ನಡ"],
    horizontal=True,
    label_visibility="collapsed"
)

is_kannada = language == "🇮🇳 ಕನ್ನಡ"

# ==================================================
# LOAD MODEL
# ==================================================

MODEL_PATH = "mushroom_disease_mobilenetv2.keras"

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

model = load_model()

# ==================================================
# CLASS NAMES
# ==================================================

class_names = [
    "Healthy",
    "Bacterial Blotch",
    "Dry Bubble",
    "Cobweb",
    "Wet Bubble"
]

# Kannada disease names

kannada_names = {
    "Healthy": "ಆರೋಗ್ಯಕರ",
    "Bacterial Blotch": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್",
    "Dry Bubble": "ಡ್ರೈ ಬಬಲ್",
    "Cobweb": "ಕಾಬ್‌ವೆಬ್",
    "Wet Bubble": "ವೆಟ್ ಬಬಲ್"
}

# ==================================================
# DISEASE-SPECIFIC FARMER ADVICE
# ==================================================

advice_english = {

    "Healthy": {
        "title": "🌱 Your mushroom appears healthy",
        "points": [
            "Continue maintaining good farm hygiene.",
            "Monitor mushrooms regularly for early signs of disease.",
            "Maintain suitable temperature, humidity and ventilation.",
            "Remove damaged or contaminated material promptly."
        ]
    },

    "Bacterial Blotch": {
        "title": "⚠️ Bacterial Blotch detected",
        "points": [
            "Remove visibly affected mushrooms carefully.",
            "Avoid excessive moisture on mushroom surfaces.",
            "Improve air circulation and ventilation.",
            "Keep growing areas and equipment clean.",
            "Monitor nearby mushrooms for similar symptoms."
        ]
    },

    "Dry Bubble": {
        "title": "⚠️ Dry Bubble detected",
        "points": [
            "Remove affected mushrooms and contaminated material carefully.",
            "Maintain good sanitation in the growing area.",
            "Improve ventilation and environmental management.",
            "Avoid spreading contaminated material to healthy areas.",
            "Seek advice from an agricultural expert if the problem increases."
        ]
    },

    "Cobweb": {
        "title": "⚠️ Cobweb detected",
        "points": [
            "Remove visibly affected mushrooms carefully.",
            "Maintain good hygiene around the growing area.",
            "Improve ventilation and air circulation.",
            "Avoid disturbing infected material unnecessarily.",
            "Monitor surrounding mushrooms for further symptoms."
        ]
    },

    "Wet Bubble": {
        "title": "⚠️ Wet Bubble detected",
        "points": [
            "Remove affected mushrooms carefully.",
            "Avoid spreading contaminated material.",
            "Maintain clean tools and growing areas.",
            "Control excessive moisture and improve ventilation.",
            "Monitor the crop regularly for additional symptoms."
        ]
    }
}

# ==================================================
# KANNADA DISEASE ADVICE
# ==================================================

advice_kannada = {

    "Healthy": {
        "title": "🌱 ನಿಮ್ಮ ಅಣಬೆ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತಿದೆ",
        "points": [
            "ಕೃಷಿ ಪ್ರದೇಶದಲ್ಲಿ ಉತ್ತಮ ಸ್ವಚ್ಛತೆಯನ್ನು ಮುಂದುವರಿಸಿ.",
            "ರೋಗದ ಲಕ್ಷಣಗಳನ್ನು ಆರಂಭದಲ್ಲೇ ಗುರುತಿಸಲು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ.",
            "ಸೂಕ್ತ ತಾಪಮಾನ, ತೇವಾಂಶ ಮತ್ತು ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
            "ಹಾನಿಗೊಳಗಾದ ಅಥವಾ ಕಲುಷಿತ ವಸ್ತುಗಳನ್ನು ತಕ್ಷಣ ತೆಗೆದುಹಾಕಿ."
        ]
    },

    "Bacterial Blotch": {
        "title": "⚠️ ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್ ಪತ್ತೆಯಾಗಿದೆ",
        "points": [
            "ಬಾಧಿತ ಅಣಬೆಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ.",
            "ಅಣಬೆಗಳ ಮೇಲ್ಮೈಯಲ್ಲಿ ಅತಿಯಾದ ತೇವಾಂಶ ಇರದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.",
            "ಗಾಳಿಯ ಹರಿವು ಮತ್ತು ವಾತಾಯನವನ್ನು ಉತ್ತಮಗೊಳಿಸಿ.",
            "ಬೆಳೆ ಪ್ರದೇಶ ಮತ್ತು ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.",
            "ಪಕ್ಕದಲ್ಲಿರುವ ಅಣಬೆಗಳಲ್ಲಿ ಇದೇ ರೀತಿಯ ಲಕ್ಷಣಗಳಿವೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ."
        ]
    },

    "Dry Bubble": {
        "title": "⚠️ ಡ್ರೈ ಬಬಲ್ ಪತ್ತೆಯಾಗಿದೆ",
        "points": [
            "ಬಾಧಿತ ಅಣಬೆಗಳು ಮತ್ತು ಕಲುಷಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ.",
            "ಬೆಳೆಯುವ ಪ್ರದೇಶದಲ್ಲಿ ಉತ್ತಮ ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
            "ವಾತಾಯನ ಮತ್ತು ಪರಿಸರ ನಿರ್ವಹಣೆಯನ್ನು ಉತ್ತಮಗೊಳಿಸಿ.",
            "ಕಲುಷಿತ ವಸ್ತುಗಳು ಆರೋಗ್ಯಕರ ಪ್ರದೇಶಗಳಿಗೆ ಹರಡದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.",
            "ಸಮಸ್ಯೆ ಹೆಚ್ಚಾದರೆ ಕೃಷಿ ತಜ್ಞರ ಸಲಹೆ ಪಡೆಯಿರಿ."
        ]
    },

    "Cobweb": {
        "title": "⚠️ ಕಾಬ್‌ವೆಬ್ ರೋಗ ಪತ್ತೆಯಾಗಿದೆ",
        "points": [
            "ಬಾಧಿತ ಅಣಬೆಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ.",
            "ಬೆಳೆಯುವ ಪ್ರದೇಶದಲ್ಲಿ ಉತ್ತಮ ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.",
            "ವಾತಾಯನ ಮತ್ತು ಗಾಳಿಯ ಹರಿವನ್ನು ಉತ್ತಮಗೊಳಿಸಿ.",
            "ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ಅನಗತ್ಯವಾಗಿ ಅಲುಗಾಡಿಸುವುದನ್ನು ತಪ್ಪಿಸಿ.",
            "ಸುತ್ತಮುತ್ತಲಿನ ಅಣಬೆಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
        ]
    },

    "Wet Bubble": {
        "title": "⚠️ ವೆಟ್ ಬಬಲ್ ರೋಗ ಪತ್ತೆಯಾಗಿದೆ",
        "points": [
            "ಬಾಧಿತ ಅಣಬೆಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ.",
            "ಕಲುಷಿತ ವಸ್ತುಗಳು ಇತರ ಪ್ರದೇಶಗಳಿಗೆ ಹರಡದಂತೆ ನೋಡಿಕೊಳ್ಳಿ.",
            "ಉಪಕರಣಗಳು ಮತ್ತು ಬೆಳೆಯುವ ಪ್ರದೇಶವನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.",
            "ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ನಿಯಂತ್ರಿಸಿ ಮತ್ತು ವಾತಾಯನವನ್ನು ಉತ್ತಮಗೊಳಿಸಿ.",
            "ಬೆಳೆಯನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
        ]
    }
}

# ==================================================
# HERO SECTION
# ==================================================

if is_kannada:

    hero_title = "🍄 ಅಣಬೆ ರೋಗ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ"
    hero_text = "AI ಮತ್ತು Deep Learning ಬಳಸಿ ಅಣಬೆಗಳ ರೋಗವನ್ನು ಗುರುತಿಸಿ"

else:

    hero_title = "🍄 Mushroom Disease Detection"
    hero_text = "Detect mushroom diseases using AI and Deep Learning"

st.markdown(
    f"""
    <div class="hero">
        <h1>{hero_title}</h1>
        <p>{hero_text}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# DASHBOARD
# ==================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">📊 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-title">📊 Dashboard</div>',
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)

# Dashboard Card 1

with col1:

    if is_kannada:

        st.markdown("""
        <div class="dashboard-card">
            <h2>🔬</h2>
            <h3>AI ರೋಗ ಪತ್ತೆ</h3>
            <p>ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ರೋಗವನ್ನು ಗುರುತಿಸಿ</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="dashboard-card">
            <h2>🔬</h2>
            <h3>AI Disease Detection</h3>
            <p>Upload an image to detect disease</p>
        </div>
        """, unsafe_allow_html=True)

# Dashboard Card 2

with col2:

    if is_kannada:

        st.markdown("""
        <div class="dashboard-card">
            <h2>🌱</h2>
            <h3>ರೈತ ಮಾರ್ಗದರ್ಶನ</h3>
            <p>ರೋಗದ ಆಧಾರದ ಮೇಲೆ ಸಲಹೆ ಪಡೆಯಿರಿ</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="dashboard-card">
            <h2>🌱</h2>
            <h3>Farmer Guidance</h3>
            <p>Get advice based on the prediction</p>
        </div>
        """, unsafe_allow_html=True)

# Dashboard Card 3

with col3:

    if is_kannada:

        st.markdown("""
        <div class="dashboard-card">
            <h2>🤖</h2>
            <h3>AI ಸಹಾಯಕ</h3>
            <p>ಅಣಬೆ ಕೃಷಿಯ ಬಗ್ಗೆ ಸಹಾಯ ಪಡೆಯಿರಿ</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="dashboard-card">
            <h2>🤖</h2>
            <h3>AI Assistant</h3>
            <p>Get help with mushroom farming</p>
        </div>
        """, unsafe_allow_html=True)

# Dashboard Card 4

with col4:

    if is_kannada:

        st.markdown("""
        <div class="dashboard-card">
            <h2>📊</h2>
            <h3>ರೋಗ ಮಾಹಿತಿ</h3>
            <p>ಸಾಮಾನ್ಯ ಅಣಬೆ ರೋಗಗಳ ಮಾಹಿತಿ</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="dashboard-card">
            <h2>📊</h2>
            <h3>Disease Insights</h3>
            <p>Learn about common mushroom diseases</p>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# HOMEPAGE FARMER ADVICE
# ==================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">🌱 ರೈತರಿಗೆ ಉಪಯುಕ್ತ ಸಲಹೆಗಳು</div>',
        unsafe_allow_html=True
    )

    st.write(
        "ಅಣಬೆ ಬೆಳೆಯಲ್ಲಿ ಉತ್ತಮ ಆರೋಗ್ಯ ಮತ್ತು ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಲು ಈ ಸಲಹೆಗಳನ್ನು ಅನುಸರಿಸಿ."
    )

else:

    st.markdown(
        '<div class="section-title">🌱 Farmer Advice</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Follow these simple practices to maintain healthy mushroom cultivation."
    )

advice_col1, advice_col2, advice_col3, advice_col4 = st.columns(4)

# Advice 1

with advice_col1:

    if is_kannada:

        st.markdown("""
        <div class="card">
            <h2>🧼</h2>
            <h3>ಸ್ವಚ್ಛತೆ</h3>
            <p>ಬೆಳೆಯುವ ಪ್ರದೇಶ ಮತ್ತು ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
            <h2>🧼</h2>
            <h3>Maintain Hygiene</h3>
            <p>Keep the growing area and equipment clean.</p>
        </div>
        """, unsafe_allow_html=True)

# Advice 2

with advice_col2:

    if is_kannada:

        st.markdown("""
        <div class="card">
            <h2>💧</h2>
            <h3>ತೇವಾಂಶ ನಿಯಂತ್ರಣ</h3>
            <p>ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ ಮತ್ತು ಪರಿಸರವನ್ನು ಗಮನಿಸಿ.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
            <h2>💧</h2>
            <h3>Control Moisture</h3>
            <p>Avoid excessive moisture and monitor the growing environment.</p>
        </div>
        """, unsafe_allow_html=True)

# Advice 3

with advice_col3:

    if is_kannada:

        st.markdown("""
        <div class="card">
            <h2>🌬️</h2>
            <h3>ವಾತಾಯನ</h3>
            <p>ಬೆಳೆಯುವ ಪ್ರದೇಶದಲ್ಲಿ ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
            <h2>🌬️</h2>
            <h3>Good Ventilation</h3>
            <p>Maintain good air circulation in the growing area.</p>
        </div>
        """, unsafe_allow_html=True)

# Advice 4

with advice_col4:

    if is_kannada:

        st.markdown("""
        <div class="card">
            <h2>🔍</h2>
            <h3>ನಿಯಮಿತ ಪರಿಶೀಲನೆ</h3>
            <p>ರೋಗದ ಆರಂಭಿಕ ಲಕ್ಷಣಗಳಿಗಾಗಿ ಅಣಬೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
            <h2>🔍</h2>
            <h3>Regular Inspection</h3>
            <p>Regularly inspect mushrooms for early signs of disease.</p>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# DETECTION SECTION
# ==================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">🔬 ಅಣಬೆ ರೋಗ ಪತ್ತೆ</div>',
        unsafe_allow_html=True
    )

    st.write(
        "ಅಣಬೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು AI ಮೂಲಕ ವಿಶ್ಲೇಷಿಸಿ."
    )

    uploaded_file = st.file_uploader(
        "ಅಣಬೆ ಚಿತ್ರದ ಆಯ್ಕೆ",
        type=["jpg", "jpeg", "png"]
    )

else:

    st.markdown(
        '<div class="section-title">🔬 Mushroom Disease Detection</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload a mushroom image and let the AI analyze it."
    )

    uploaded_file = st.file_uploader(
        "Choose a mushroom image",
        type=["jpg", "jpeg", "png"]
    )

# ==================================================
# PREDICTION
# ==================================================

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns(2)

    # Uploaded Image

    with col1:

        st.image(
            image,
            caption=(
                "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ"
                if is_kannada
                else
                "Uploaded Image"
            ),
            use_container_width=True
        )

    # Resize Image

    image_resized = image.resize((224, 224))

    # Normalize

    image_array = np.array(image_resized) / 255.0

    # Add batch dimension

    image_array = np.expand_dims(image_array, axis=0)

    # Prediction

    predictions = model.predict(
        image_array,
        verbose=0
    )

    predicted_index = np.argmax(predictions[0])

    predicted_class = class_names[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    ) * 100

    # Display name

    if is_kannada:

        display_name = kannada_names[predicted_class]

    else:

        display_name = predicted_class

    # ==================================================
    # RESULT
    # ==================================================

    with col2:

        if is_kannada:

            st.markdown(
                f"""
                <div class="result-card">
                    <h2>🍄 {display_name}</h2>
                    <h3>ವಿಶ್ವಾಸ ಮಟ್ಟ: {confidence:.2f}%</h3>
                    <p>
                    ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರದ ಆಧಾರದ ಮೇಲೆ AI ನೀಡಿದ ಫಲಿತಾಂಶ.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="result-card">
                    <h2>🍄 {display_name}</h2>
                    <h3>Confidence: {confidence:.2f}%</h3>
                    <p>
                    AI prediction based on the uploaded image.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ==================================================
    # DISEASE-SPECIFIC FARMER ADVICE
    # ==================================================

    if is_kannada:

        advice = advice_kannada[predicted_class]

    else:

        advice = advice_english[predicted_class]

    st.markdown(
        f"""
        <div class="advice-card">
            <h2>{advice["title"]}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    for point in advice["points"]:

        st.markdown(
            f"### 💡 {point}"
        )

    # Important disclaimer

    if is_kannada:

        st.info(
            "⚠️ ಈ ವ್ಯವಸ್ಥೆಯು AI ಆಧಾರಿತ ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶನವನ್ನು ನೀಡುತ್ತದೆ. "
            "ಗಂಭೀರ ಸಮಸ್ಯೆಗಳಿದ್ದರೆ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
        )

    else:

        st.info(
            "⚠️ This system provides AI-based preliminary guidance. "
            "For serious crop problems, consult an agricultural expert."
        )

# ==================================================
# SUPPORTED DISEASES
# ==================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">🍄 ಪತ್ತೆ ಮಾಡಬಹುದಾದ ರೋಗಗಳು</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-title">🍄 Supported Diseases</div>',
        unsafe_allow_html=True
    )

disease_cols = st.columns(5)

disease_emojis = [
    "🌱",
    "🦠",
    "🫧",
    "🕸️",
    "💧"
]

for i, disease in enumerate(class_names):

    if is_kannada:

        name = kannada_names[disease]

    else:

        name = disease

    with disease_cols[i]:

        st.markdown(
            f"""
            <div class="disease-card">
                <h2>{disease_emojis[i]}</h2>
                <b>{name}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==================================================
# HOW IT WORKS
# ==================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">⚙️ ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-title">⚙️ How It Works</div>',
        unsafe_allow_html=True
    )

c1, c2, c3 = st.columns(3)

# Step 1

with c1:

    if is_kannada:

        st.markdown("""
        <div class="card">
            <h2>1️⃣</h2>
            <h3>ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ</h3>
            <p>ಅಣಬೆಯ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
            <h2>1️⃣</h2>
            <h3>Upload Image</h3>
            <p>Upload a clear image of the mushroom.</p>
        </div>
        """, unsafe_allow_html=True)

# Step 2

with c2:

    if is_kannada:

        st.markdown("""
        <div class="card">
            <h2>2️⃣</h2>
            <h3>AI ವಿಶ್ಲೇಷಣೆ</h3>
            <p>MobileNetV2 ಮಾದರಿಯು ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
            <h2>2️⃣</h2>
            <h3>AI Analysis</h3>
            <p>MobileNetV2 analyzes the uploaded image.</p>
        </div>
        """, unsafe_allow_html=True)

# Step 3

with c3:

    if is_kannada:

        st.markdown("""
        <div class="card">
            <h2>3️⃣</h2>
            <h3>ಫಲಿತಾಂಶ ಮತ್ತು ಸಲಹೆ</h3>
            <p>ರೋಗದ ಫಲಿತಾಂಶ ಮತ್ತು ರೈತ ಸಲಹೆ ಪಡೆಯಿರಿ.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="card">
            <h2>3️⃣</h2>
            <h3>Result & Advice</h3>
            <p>Get the predicted disease and farmer guidance.</p>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    🍄 AI Based Mushroom Disease Detection System<br>
    Powered by MobileNetV2 & Deep Learning
</div>
""", unsafe_allow_html=True)
