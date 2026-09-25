import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f0fdf4, #ffffff, #ecfdf5);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #064e3b, #047857, #10b981);
    padding: 42px;
    border-radius: 28px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 15px 40px rgba(5, 150, 105, 0.22);
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    padding: 7px 15px;
    border-radius: 30px;
    font-size: 14px;
    margin-bottom: 12px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin: 0;
}

.hero-subtitle {
    font-size: 19px;
    margin-top: 10px;
}

.hero-description {
    font-size: 15px;
    line-height: 1.7;
    opacity: 0.95;
}

/* SECTION */
.section-title {
    color: #064e3b;
    font-size: 27px;
    font-weight: 700;
    margin-top: 28px;
    margin-bottom: 15px;
}

/* DASHBOARD CARDS */
.card {
    background: white;
    border: 1px solid #d1fae5;
    border-radius: 20px;
    padding: 22px;
    min-height: 165px;
    box-shadow: 0 7px 22px rgba(6,78,59,0.08);
}

.card-icon {
    font-size: 34px;
    margin-bottom: 8px;
}

.card-title {
    color: #065f46;
    font-size: 18px;
    font-weight: 700;
}

.card-text {
    color: #4b5563;
    font-size: 13px;
    line-height: 1.6;
}

/* DISEASE */
.disease-card {
    background: white;
    border: 1px solid #d1fae5;
    border-radius: 18px;
    padding: 18px 10px;
    text-align: center;
    min-height: 130px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.05);
}

.disease-icon {
    font-size: 30px;
}

.disease-name {
    color: #065f46;
    font-weight: 700;
    font-size: 14px;
    margin-top: 7px;
}

.disease-description {
    color: #6b7280;
    font-size: 11px;
}

/* HOW IT WORKS */
.step-card {
    background: white;
    border: 1px solid #bbf7d0;
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    min-height: 145px;
}

.step-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #059669;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    font-weight: 700;
    font-size: 17px;
}

.step-icon {
    font-size: 30px;
    margin: 10px 0;
}

.step-name {
    color: #065f46;
    font-weight: 700;
}

/* DETECTION */
.detect-box {
    background: linear-gradient(135deg, #064e3b, #047857);
    padding: 30px;
    border-radius: 25px;
    color: white;
    box-shadow: 0 12px 30px rgba(6,78,59,0.18);
}

.detect-title {
    font-size: 26px;
    font-weight: 700;
}

.detect-text {
    color: #d1fae5;
    line-height: 1.7;
}

/* RESULT */
.result-box {
    background: linear-gradient(135deg, #ecfdf5, #ffffff);
    border: 2px solid #10b981;
    padding: 25px;
    border-radius: 22px;
    text-align: center;
    margin-top: 15px;
}

.result-title {
    color: #065f46;
    font-size: 25px;
    font-weight: 800;
}

.confidence {
    color: #047857;
    font-size: 18px;
    font-weight: 700;
}

/* FARMER */
.farmer-box {
    background: linear-gradient(135deg, #14532d, #166534);
    color: white;
    padding: 28px;
    border-radius: 24px;
    margin-top: 25px;
}

.farmer-box h2 {
    color: white;
}

.farmer-box p {
    color: #dcfce7;
    line-height: 1.7;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #6b7280;
    padding: 30px 10px 10px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LANGUAGE SELECTOR
# =========================================================

st.markdown("""
<div style="
background: linear-gradient(135deg,#064e3b,#059669);
padding: 16px;
border-radius: 18px;
text-align: center;
margin-bottom: 10px;
">

<div style="
color:white;
font-size:17px;
font-weight:700;
">
🌐 SELECT LANGUAGE / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ
</div>

</div>
""", unsafe_allow_html=True)

language = st.radio(
    "Language",
    ["🇬🇧 English", "🇮🇳 ಕನ್ನಡ"],
    horizontal=True,
    label_visibility="collapsed"
)

is_kannada = language == "🇮🇳 ಕನ್ನಡ"


# =========================================================
# TEXT TRANSLATIONS
# =========================================================

if is_kannada:

    hero_badge = "🌱 ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ • ಸ್ಮಾರ್ಟ್ ಕೃಷಿ"
    hero_title = "🍄 ಮಶ್ರೂಮ್ AI ಸಹಾಯಕ"
    hero_subtitle = "ಸ್ಮಾರ್ಟ್ ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ ಮತ್ತು ರೈತರ ಸಹಾಯ"
    hero_description = (
        "ಮಶ್ರೂಮ್‌ನ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ. "
        "AI ಮಾದರಿಯು ಸಂಭವನೀಯ ರೋಗವನ್ನು ಗುರುತಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ "
        "ಮತ್ತು ಸರಳ ರೈತ ಸ್ನೇಹಿ ಮಾಹಿತಿಯನ್ನು ನೀಡುತ್ತದೆ."
    )

    dashboard_title = "🌿 ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್"

    cards = [
        (
            "🔬",
            "AI ರೋಗ ಪತ್ತೆ",
            "ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು AI ಮೂಲಕ ವಿಶ್ಲೇಷಿಸಿ."
        ),
        (
            "🌱",
            "ರೈತ ಮಾರ್ಗದರ್ಶನ",
            "ಮಶ್ರೂಮ್ ಆರೋಗ್ಯದ ಬಗ್ಗೆ ಸರಳ ಮತ್ತು ಉಪಯುಕ್ತ ಮಾಹಿತಿ ಪಡೆಯಿರಿ."
        ),
        (
            "💬",
            "AI ರೈತ ಸಹಾಯಕ",
            "ಮಶ್ರೂಮ್ ರೋಗಗಳು ಮತ್ತು ಕೃಷಿಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ."
        ),
        (
            "📊",
            "ರೋಗ ಮಾಹಿತಿ",
            "ಪತ್ತೆಯಾದ ರೋಗದ ಬಗ್ಗೆ ಸುಲಭವಾಗಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ."
        )
    ]

    detection_title = "📸 ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ"
    detect_title = "🔍 AI ಮೂಲಕ ರೋಗ ಪತ್ತೆ ಮಾಡಿ"
    detect_text = (
        "ಸ್ಪಷ್ಟವಾದ ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ. "
        "AI ಮಾದರಿಯು ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಿ ಸಂಭವನೀಯ ರೋಗ "
        "ಮತ್ತು ವಿಶ್ವಾಸದ ಮಟ್ಟವನ್ನು ತೋರಿಸುತ್ತದೆ."
    )
    upload_text = "ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ"

    disease_title = "🦠 ಪತ್ತೆ ಮಾಡಬಹುದಾದ ಮಶ್ರೂಮ್ ಸ್ಥಿತಿಗಳು"

    disease_names = [
        ("ಆರೋಗ್ಯಕರ", "ರೋಗ ಪತ್ತೆಯಾಗಿಲ್ಲ"),
        ("ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್", "ಬ್ಯಾಕ್ಟೀರಿಯಾ ಸೋಂಕು"),
        ("ಡ್ರೈ ಬಬಲ್", "ಶಿಲೀಂಧ್ರ ರೋಗ"),
        ("ಕಾಬ್‌ವೆಬ್", "ಶಿಲೀಂಧ್ರ ಸೋಂಕು"),
        ("ವೆಟ್ ಬಬಲ್", "ಶಿಲೀಂಧ್ರ ರೋಗ")
    ]

    how_title = "⚡ ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?"

    steps = [
        ("1", "📷", "ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"),
        ("2", "🤖", "AI ವಿಶ್ಲೇಷಣೆ"),
        ("3", "🔬", "ರೋಗದ ಫಲಿತಾಂಶ"),
        ("4", "🌱", "ರೈತ ಮಾರ್ಗದರ್ಶನ")
    ]

    farmer_title = "👨‍🌾 ಮಶ್ರೂಮ್ ರೈತರಿಗಾಗಿ"
    farmer_text = (
        "ಮಶ್ರೂಮ್‌ಗಳಲ್ಲಿ ಕಾಣಿಸಿಕೊಳ್ಳುವ ರೋಗದ ಲಕ್ಷಣಗಳನ್ನು "
        "ಆರಂಭದಲ್ಲೇ ಗುರುತಿಸುವುದು ರೈತರಿಗೆ ಸಹಾಯ ಮಾಡಬಹುದು. "
        "ಈ ವ್ಯವಸ್ಥೆಯು AI ಆಧಾರಿತ ರೋಗ ಪತ್ತೆ ಮತ್ತು ಸರಳ "
        "ಮಾಹಿತಿಯನ್ನು ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ ನೀಡುತ್ತದೆ."
    )

    result_title = "ಪತ್ತೆಯಾದ ಫಲಿತಾಂಶ"
    confidence_text = "AI ವಿಶ್ವಾಸ ಮಟ್ಟ"

else:

    hero_badge = "🌱 AI Powered Agriculture • Smart Farming"
    hero_title = "🍄 Mushroom AI Assistant"
    hero_subtitle = "Smart Mushroom Disease Detection & Farmer Support"
    hero_description = (
        "Upload a mushroom image and let our AI model analyze it "
        "for possible diseases and provide simple farmer-friendly information."
    )

    dashboard_title = "🌿 Smart Farming Dashboard"

    cards = [
        (
            "🔬",
            "AI Disease Detection",
            "Upload a mushroom image and let AI analyze it."
        ),
        (
            "🌱",
            "Farmer Guidance",
            "Get simple and practical mushroom health information."
        ),
        (
            "💬",
            "AI Farmer Assistant",
            "Ask questions about diseases and mushroom cultivation."
        ),
        (
            "📊",
            "Disease Insights",
            "Understand detected diseases through simple information."
        )
    ]

    detection_title = "📸 Detect Mushroom Disease"
    detect_title = "🔍 Start Your AI Diagnosis"
    detect_text = (
        "Upload a clear photograph of your mushroom. "
        "The AI model will analyze the image and show "
        "the predicted disease and confidence level."
    )
    upload_text = "Choose a mushroom image"

    disease_title = "🦠 Supported Mushroom Conditions"

    disease_names = [
        ("Healthy", "No disease detected"),
        ("Bacterial Blotch", "Bacterial infection"),
        ("Dry Bubble", "Fungal disease"),
        ("Cobweb", "Fungal infection"),
        ("Wet Bubble", "Fungal disease")
    ]

    how_title = "⚡ How It Works"

    steps = [
        ("1", "📷", "Upload Image"),
        ("2", "🤖", "AI Analysis"),
        ("3", "🔬", "Disease Result"),
        ("4", "🌱", "Farmer Guidance")
    ]

    farmer_title = "👨‍🌾 Built for Mushroom Farmers"
    farmer_text = (
        "Early identification of visible disease symptoms can help "
        "farmers take timely action. This system provides AI-based "
        "disease prediction and simple information in one place."
    )

    result_title = "Predicted Result"
    confidence_text = "AI Confidence"


# =========================================================
# HERO
# =========================================================

st.markdown(
    f"""
<div class="hero">

<div class="hero-badge">
{hero_badge}
</div>

<div class="hero-title">
{hero_title}
</div>

<div class="hero-subtitle">
<b>{hero_subtitle}</b>
</div>

<div class="hero-description">
{hero_description}
</div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

st.markdown(
    f'<div class="section-title">{dashboard_title}</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

for col, card in zip(
    [col1, col2, col3, col4],
    cards
):

    with col:

        st.markdown(
            f"""
<div class="card">

<div class="card-icon">
{card[0]}
</div>

<div class="card-title">
{card[1]}
</div>

<div class="card-text">
{card[2]}
</div>

</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# AI DETECTION
# =========================================================

st.markdown(
    f'<div class="section-title">{detection_title}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
<div class="detect-box">

<div class="detect-title">
{detect_title}
</div>

<div class="detect-text">
{detect_text}
</div>

</div>
""",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    upload_text,
    type=["jpg", "jpeg", "png"]
)


# =========================================================
# MODEL
# =========================================================

MODEL_PATH = "mushroom_disease_mobilenetv2.keras"

class_names = [
    "Healthy",
    "Bacterial Blotch",
    "Dry Bubble",
    "Cobweb",
    "Wet Bubble"
]


@st.cache_resource
def load_mushroom_model():

    return tf.keras.models.load_model(
        MODEL_PATH
    )


# =========================================================
# PREDICTION
# =========================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    col_img, col_result = st.columns(
        [1, 1]
    )

    with col_img:

        st.image(
            image,
            caption=(
                "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ"
                if is_kannada
                else "Uploaded Mushroom Image"
            ),
            use_container_width=True
        )

    with col_result:

        with st.spinner(
            "AI ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ..."
            if is_kannada
            else "AI is analyzing the image..."
        ):

            model = load_mushroom_model()

            img = image.resize(
                (224, 224)
            )

            img_array = (
                np.array(img) / 255.0
            )

            img_array = np.expand_dims(
                img_array,
                axis=0
            )

            predictions = model.predict(
                img_array,
                verbose=0
            )

            predicted_index = int(
                np.argmax(
                    predictions[0]
                )
            )

            confidence = (
                float(
                    predictions[0][predicted_index]
                ) * 100
            )

            predicted_class = class_names[
                predicted_index
            ]

        kannada_names = {

            "Healthy":
                "ಆರೋಗ್ಯಕರ",

            "Bacterial Blotch":
                "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್",

            "Dry Bubble":
                "ಡ್ರೈ ಬಬಲ್",

            "Cobweb":
                "ಕಾಬ್‌ವೆಬ್",

            "Wet Bubble":
                "ವೆಟ್ ಬಬಲ್"
        }

        display_name = (
            kannada_names[predicted_class]
            if is_kannada
            else predicted_class
        )

        st.markdown(
            f"""
<div class="result-box">

<div class="result-title">
{result_title}
</div>

<div style="
font-size:35px;
margin:15px;
">
🍄
</div>

<div style="
font-size:24px;
font-weight:800;
color:#064e3b;
">
{display_name}
</div>

<div class="confidence">
{confidence_text}: {confidence:.2f}%
</div>

</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# SUPPORTED DISEASES
# =========================================================

st.markdown(
    f'<div class="section-title">{disease_title}</div>',
    unsafe_allow_html=True
)

disease_icons = [
    "🍄",
    "🟠",
    "🟤",
    "⚪",
    "🔵"
]

d1, d2, d3, d4, d5 = st.columns(5)

for col, icon, disease in zip(
    [d1, d2, d3, d4, d5],
    disease_icons,
    disease_names
):

    with col:

        st.markdown(
            f"""
<div class="disease-card">

<div class="disease-icon">
{icon}
</div>

<div class="disease-name">
{disease[0]}
</div>

<div class="disease-description">
{disease[1]}
</div>

</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# HOW IT WORKS
# =========================================================

st.markdown(
    f'<div class="section-title">{how_title}</div>',
    unsafe_allow_html=True
)

s1, s2, s3, s4 = st.columns(4)

for col, step in zip(
    [s1, s2, s3, s4],
    steps
):

    with col:

        st.markdown(
            f"""
<div class="step-card">

<div class="step-number">
{step[0]}
</div>

<div class="step-icon">
{step[1]}
</div>

<div class="step-name">
{step[2]}
</div>

</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# FARMER SUPPORT
# =========================================================

st.markdown(
    f"""
<div class="farmer-box">

<h2>{farmer_title}</h2>

<p>
{farmer_text}
</p>

<p>
🌱 {"ಸರಳ ಬಳಕೆ" if is_kannada else "Simple interface"}
&nbsp; • &nbsp;

📱 {"ಮೊಬೈಲ್ ಸ್ನೇಹಿ" if is_kannada else "Mobile friendly"}
&nbsp; • &nbsp;

🌐 {"ಕನ್ನಡ ಮತ್ತು English" if is_kannada else "English & Kannada"}
&nbsp; • &nbsp;

🤖 {"AI ಆಧಾರಿತ" if is_kannada else "AI powered"}
</p>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

footer_warning = (
    "⚠️ AI ಫಲಿತಾಂಶಗಳು ಮಾಹಿತಿ ಉದ್ದೇಶಕ್ಕಾಗಿ ಮಾತ್ರ. "
    "ಪ್ರಮುಖ ಬೆಳೆ ನಿರ್ಧಾರಗಳಿಗಾಗಿ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
    if is_kannada
    else
    "⚠️ AI predictions are for informational purposes. "
    "For important crop decisions, consult an agricultural expert."
)

st.markdown(
    f"""
<div class="footer">

🍄 <b>Mushroom AI Assistant</b>

<br>

{"AI ಆಧಾರಿತ ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ ಮತ್ತು ರೈತರ ಸಹಾಯ"
 if is_kannada
 else
 "AI-based mushroom disease detection and farmer support"}

<br><br>

{footer_warning}

</div>
""",
    unsafe_allow_html=True
)
