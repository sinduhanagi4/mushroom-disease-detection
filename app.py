import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #f5fff8;
}

.hero {
    background: linear-gradient(135deg, #064e3b, #047857, #10b981);
    padding: 45px 30px;
    border-radius: 28px;
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    font-size: 19px;
}

.section-title {
    color: #065f46;
    font-size: 30px;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 20px;
}

.dashboard-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    min-height: 175px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.08);
}

.dashboard-card:hover {
    transform: translateY(-4px);
}

.card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    min-height: 175px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.result-card {
    background: linear-gradient(135deg, #dcfce7, #ffffff);
    padding: 30px;
    border-radius: 25px;
    border-left: 8px solid #059669;
    margin-top: 20px;
}

.advice-card {
    background: linear-gradient(135deg, #fff7ed, #fffbeb);
    padding: 25px;
    border-radius: 20px;
    border-left: 8px solid #f59e0b;
    margin-top: 25px;
    margin-bottom: 20px;
}

.chatbot-card {
    background: linear-gradient(135deg, #ecfdf5, #ffffff);
    padding: 25px;
    border-radius: 22px;
    border-left: 8px solid #10b981;
    margin-top: 20px;
}

.disease-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    min-height: 130px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.07);
}

.footer {
    text-align: center;
    padding: 35px;
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

kannada_names = {
    "Healthy": "ಆರೋಗ್ಯಕರ",
    "Bacterial Blotch": "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್",
    "Dry Bubble": "ಡ್ರೈ ಬಬಲ್",
    "Cobweb": "ಕಾಬ್‌ವೆಬ್",
    "Wet Bubble": "ವೆಟ್ ಬಬಲ್"
}

# ==================================================
# DISEASE-SPECIFIC ADVICE - ENGLISH
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
# DISEASE-SPECIFIC ADVICE - KANNADA
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
# HERO
# ==================================================

if is_kannada:
    hero_title = "🍄 ಅಣಬೆ ರೋಗ ಪತ್ತೆ ವ್ಯವಸ್ಥೆ"
    hero_text = "AI ಮತ್ತು Deep Learning ಬಳಸಿ ಅಣಬೆಗಳ ರೋಗವನ್ನು ಗುರುತಿಸಿ"
else:
    hero_title = "🍄 Mushroom AI Assistant"
    hero_text = "Smart Mushroom Disease Detection & Farmer Support"

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
        '<div class="section-title">🌿 ಸ್ಮಾರ್ಟ್ ಫಾರ್ಮಿಂಗ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="section-title">🌿 Smart Farming Dashboard</div>',
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    if is_kannada:
        title = "AI ರೋಗ ಪತ್ತೆ"
        text = "ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ರೋಗವನ್ನು ಗುರುತಿಸಿ"
    else:
        title = "AI Disease Detection"
        text = "Upload an image to detect disease"

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h2>🔬</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    if is_kannada:
        title = "ರೈತ ಮಾರ್ಗದರ್ಶನ"
        text = "ರೋಗದ ಆಧಾರದ ಮೇಲೆ ಸಲಹೆ ಪಡೆಯಿರಿ"
    else:
        title = "Farmer Guidance"
        text = "Get advice based on the prediction"

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h2>🌱</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    if is_kannada:
        title = "AI ಸಹಾಯಕ"
        text = "ಅಣಬೆ ಕೃಷಿಯ ಬಗ್ಗೆ ಸಹಾಯ ಪಡೆಯಿರಿ"
    else:
        title = "AI Assistant"
        text = "Get help with mushroom farming"

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h2>🤖</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    if is_kannada:
        title = "ರೋಗ ಮಾಹಿತಿ"
        text = "ಸಾಮಾನ್ಯ ಅಣಬೆ ರೋಗಗಳ ಮಾಹಿತಿ"
    else:
        title = "Disease Insights"
        text = "Learn about common mushroom diseases"

    st.markdown(
        f"""
        <div class="dashboard-card">
            <h2>📊</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# STEP 4 - HOMEPAGE FARMER ADVICE
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

with advice_col1:

    if is_kannada:
        title = "ಸ್ವಚ್ಛತೆ"
        text = "ಬೆಳೆಯುವ ಪ್ರದೇಶ ಮತ್ತು ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ."
    else:
        title = "Maintain Hygiene"
        text = "Keep the growing area and equipment clean."

    st.markdown(
        f"""
        <div class="card">
            <h2>🧼</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with advice_col2:

    if is_kannada:
        title = "ತೇವಾಂಶ ನಿಯಂತ್ರಣ"
        text = "ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ ಮತ್ತು ಪರಿಸರವನ್ನು ಗಮನಿಸಿ."
    else:
        title = "Control Moisture"
        text = "Avoid excessive moisture and monitor the growing environment."

    st.markdown(
        f"""
        <div class="card">
            <h2>💧</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with advice_col3:

    if is_kannada:
        title = "ವಾತಾಯನ"
        text = "ಬೆಳೆಯುವ ಪ್ರದೇಶದಲ್ಲಿ ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
    else:
        title = "Good Ventilation"
        text = "Maintain good air circulation in the growing area."

    st.markdown(
        f"""
        <div class="card">
            <h2>🌬️</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with advice_col4:

    if is_kannada:
        title = "ನಿಯಮಿತ ಪರಿಶೀಲನೆ"
        text = "ರೋಗದ ಆರಂಭಿಕ ಲಕ್ಷಣಗಳಿಗಾಗಿ ಅಣಬೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ."
    else:
        title = "Regular Inspection"
        text = "Regularly inspect mushrooms for early signs of disease."

    st.markdown(
        f"""
        <div class="card">
            <h2>🔍</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# DISEASE DETECTION
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

    with col1:

        st.image(
            image,
            caption="ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ"
            if is_kannada
            else "Uploaded Image",
            use_container_width=True
        )

    image_resized = image.resize((224, 224))

    image_array = np.array(image_resized) / 255.0

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    predictions = model.predict(
        image_array,
        verbose=0
    )

    predicted_index = np.argmax(predictions[0])

    predicted_class = class_names[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    ) * 100

    display_name = (
        kannada_names[predicted_class]
        if is_kannada
        else predicted_class
    )

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
    # DISEASE-SPECIFIC ADVICE
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
        st.markdown(f"### 💡 {point}")

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

    name = (
        kannada_names[disease]
        if is_kannada
        else disease
    )

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

with c1:

    if is_kannada:
        title = "ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"
        text = "ಅಣಬೆಯ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
    else:
        title = "Upload Image"
        text = "Upload a clear image of the mushroom."

    st.markdown(
        f"""
        <div class="card">
            <h2>1️⃣</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    if is_kannada:
        title = "AI ವಿಶ್ಲೇಷಣೆ"
        text = "MobileNetV2 ಮಾದರಿಯು ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ."
    else:
        title = "AI Analysis"
        text = "MobileNetV2 analyzes the uploaded image."

    st.markdown(
        f"""
        <div class="card">
            <h2>2️⃣</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    if is_kannada:
        title = "ಫಲಿತಾಂಶ ಮತ್ತು ಸಲಹೆ"
        text = "ರೋಗದ ಫಲಿತಾಂಶ ಮತ್ತು ರೈತ ಸಲಹೆ ಪಡೆಯಿರಿ."
    else:
        title = "Result & Advice"
        text = "Get the predicted disease and farmer guidance."

    st.markdown(
        f"""
        <div class="card">
            <h2>3️⃣</h2>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# STEP 5 - AI FARMER CHATBOT
# ==================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">🤖 AI ರೈತ ಸಹಾಯಕ</div>',
        unsafe_allow_html=True
    )

    st.write(
        "ಅಣಬೆ ಕೃಷಿ ಮತ್ತು ರೋಗಗಳ ಬಗ್ಗೆ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ."
    )

else:

    st.markdown(
        '<div class="section-title">🤖 AI Farmer Assistant</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask questions about mushroom farming and disease prevention."
    )

# Chat history

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input

if is_kannada:

    user_question = st.chat_input(
        "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ಬರೆಯಿರಿ..."
    )

else:

    user_question = st.chat_input(
        "Ask your mushroom farming question..."
    )

# ==================================================
# CHATBOT RESPONSE
# ==================================================

if user_question:

    # Save user question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    question = user_question.lower()

    # ==================================================
    # KANNADA CHATBOT
    # ==================================================

    if is_kannada:

        if "ಬ್ಯಾಕ್ಟೀರಿಯಲ್" in question or "blotch" in question:

            response = (
                "🦠 ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್ ಕಂಡುಬಂದರೆ, "
                "ಬಾಧಿತ ಅಣಬೆಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ. "
                "ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ ಮತ್ತು ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )

        elif "ಡ್ರೈ ಬಬಲ್" in question or "dry bubble" in question:

            response = (
                "🫧 ಡ್ರೈ ಬಬಲ್ ಸಮಸ್ಯೆ ಕಂಡುಬಂದರೆ, "
                "ಬಾಧಿತ ಅಣಬೆಗಳು ಮತ್ತು ಕಲುಷಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ. "
                "ಸ್ವಚ್ಛತೆ ಮತ್ತು ವಾತಾಯನವನ್ನು ಉತ್ತಮವಾಗಿಡಿ."
            )

        elif "ಕಾಬ್" in question or "cobweb" in question:

            response = (
                "🕸️ ಕಾಬ್‌ವೆಬ್ ರೋಗದ ಸಂದರ್ಭದಲ್ಲಿ ಬಾಧಿತ ಪ್ರದೇಶವನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ನಿರ್ವಹಿಸಿ. "
                "ಬೆಳೆಯುವ ಪ್ರದೇಶವನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ ಮತ್ತು ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )

        elif "ವೆಟ್ ಬಬಲ್" in question or "wet bubble" in question:

            response = (
                "💧 ವೆಟ್ ಬಬಲ್ ಕಂಡುಬಂದರೆ, ಬಾಧಿತ ಅಣಬೆಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ. "
                "ಕಲುಷಿತ ವಸ್ತು ಹರಡದಂತೆ ನೋಡಿಕೊಳ್ಳಿ ಮತ್ತು ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ನಿಯಂತ್ರಿಸಿ."
            )

        elif "ಸ್ವಚ್ಛ" in question or "hygiene" in question:

            response = (
                "🧼 ಅಣಬೆ ಕೃಷಿಯಲ್ಲಿ ಸ್ವಚ್ಛತೆ ಬಹಳ ಮುಖ್ಯ. "
                "ಬೆಳೆಯುವ ಪ್ರದೇಶ, ಉಪಕರಣಗಳು ಮತ್ತು ಕೆಲಸದ ಸ್ಥಳವನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ."
            )

        elif "ತೇವಾಂಶ" in question or "moisture" in question:

            response = (
                "💧 ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ. "
                "ಬೆಳೆಯುವ ಪ್ರದೇಶದ ಪರಿಸರವನ್ನು ನಿಯಮಿತವಾಗಿ ಗಮನಿಸಿ ಮತ್ತು ಉತ್ತಮ ವಾತಾಯನವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )

        elif "ಗಾಳಿ" in question or "ವಾತಾಯನ" in question or "ventilation" in question:

            response = (
                "🌬️ ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವು ಅಣಬೆ ಕೃಷಿಯಲ್ಲಿ ಮುಖ್ಯವಾಗಿದೆ. "
                "ಬೆಳೆಯುವ ಪ್ರದೇಶದಲ್ಲಿ ಸೂಕ್ತ ವಾತಾಯನವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )

        elif "ರೋಗ" in question or "disease" in question:

            response = (
                "🔍 ರೋಗದ ಆರಂಭಿಕ ಲಕ್ಷಣಗಳಿಗಾಗಿ ಅಣಬೆಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ. "
                "ಬಾಧಿತ ಅಣಬೆಗಳನ್ನು ಆರೋಗ್ಯಕರ ಅಣಬೆಗಳಿಂದ ಪ್ರತ್ಯೇಕವಾಗಿ ನಿರ್ವಹಿಸಿ."
            )

        else:

            response = (
                "🤖 ನಾನು ಅಣಬೆ ರೋಗಗಳು, ಸ್ವಚ್ಛತೆ, ತೇವಾಂಶ, "
                "ವಾತಾಯನ ಮತ್ತು ರೈತ ಮಾರ್ಗದರ್ಶನದ ಬಗ್ಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. "
                "ಉದಾಹರಣೆಗೆ: 'ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್ ಬಗ್ಗೆ ಹೇಳಿ'."
            )

    # ==================================================
    # ENGLISH CHATBOT
    # ==================================================

    else:

        if "bacterial" in question or "blotch" in question:

            response = (
                "🦠 If Bacterial Blotch is detected, "
                "carefully remove visibly affected mushrooms. "
                "Avoid excessive moisture and maintain good ventilation."
            )

        elif "dry bubble" in question:

            response = (
                "🫧 If Dry Bubble is detected, "
                "carefully remove affected mushrooms and contaminated material. "
                "Maintain good hygiene and ventilation."
            )

        elif "cobweb" in question:

            response = (
                "🕸️ If Cobweb is detected, carefully manage affected areas. "
                "Keep the growing area clean and maintain good air circulation."
            )

        elif "wet bubble" in question:

            response = (
                "💧 If Wet Bubble is detected, carefully remove affected mushrooms. "
                "Avoid spreading contaminated material and control excessive moisture."
            )

        elif "hygiene" in question or "clean" in question:

            response = (
                "🧼 Good hygiene is important in mushroom cultivation. "
                "Keep the growing area, tools and working surfaces clean."
            )

        elif "moisture" in question or "humidity" in question:

            response = (
                "💧 Avoid excessive moisture. "
                "Monitor the growing environment regularly and maintain good ventilation."
            )

        elif "ventilation" in question or "air" in question:

            response = (
                "🌬️ Good air circulation is important for mushroom cultivation. "
                "Maintain suitable ventilation in the growing area."
            )

        elif "disease" in question:

            response = (
                "🔍 Regularly inspect mushrooms for early signs of disease. "
                "Handle affected mushrooms separately from healthy mushrooms."
            )

        else:

            response = (
                "🤖 I can help with mushroom diseases, hygiene, "
                "moisture, ventilation and farmer guidance. "
                "For example, ask: 'What is Bacterial Blotch?'"
            )

    # Save response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Display response

    with st.chat_message("assistant"):
        st.write(response)

# ==================================================
# FOOTER
# ==================================================

st.markdown("""
<div class="footer">
    🍄 AI Based Mushroom Disease Detection System<br>
    Powered by MobileNetV2 & Deep Learning
</div>
""", unsafe_allow_html=True)
