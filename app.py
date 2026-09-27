import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
    radial-gradient(circle at top left, #dcfce7 0%, transparent 30%),
    radial-gradient(circle at bottom right, #d1fae5 0%, transparent 30%),
    linear-gradient(135deg, #f0fdf4, #ecfdf5);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* HERO */

.hero {
    background: linear-gradient(135deg, #064e3b, #047857, #10b981);
    padding: 42px 35px;
    border-radius: 28px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 12px 35px rgba(6, 78, 59, 0.25);
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.16);
    padding: 8px 18px;
    border-radius: 30px;
    font-size: 14px;
    margin-bottom: 15px;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin: 5px 0;
}

.hero p {
    font-size: 17px;
    opacity: 0.95;
}

/* SECTION */

.section-title {
    color: #064e3b;
    font-size: 27px;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 15px;
}

/* CARDS */

.card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    margin-bottom: 18px;
    box-shadow: 0 7px 22px rgba(0,0,0,0.08);
    border: 1px solid #d1fae5;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.12);
}

.card-icon {
    font-size: 35px;
}

.card h3 {
    color: #065f46;
    margin-bottom: 5px;
}

.card p {
    color: #4b5563;
}

/* DETECTION */

.detect-box {
    background: white;
    padding: 28px;
    border-radius: 22px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid #bbf7d0;
}

/* RESULT */

.result-box {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    border-left: 7px solid #059669;
    padding: 28px;
    border-radius: 20px;
    margin-top: 20px;
    box-shadow: 0 7px 20px rgba(0,0,0,0.06);
}

.result-title {
    color: #065f46;
    font-size: 25px;
    font-weight: 800;
}

.result-disease {
    color: #064e3b;
    font-size: 32px;
    font-weight: 800;
    margin-top: 8px;
}

.status-healthy {
    display: inline-block;
    background: #dcfce7;
    color: #166534;
    padding: 7px 15px;
    border-radius: 20px;
    font-weight: 700;
    margin-top: 8px;
}

.status-disease {
    display: inline-block;
    background: #fee2e2;
    color: #991b1b;
    padding: 7px 15px;
    border-radius: 20px;
    font-weight: 700;
    margin-top: 8px;
}

/* CONFIDENCE */

.confidence-box {
    background: white;
    padding: 20px;
    border-radius: 16px;
    margin-top: 18px;
    border: 1px solid #d1fae5;
}

.confidence-number {
    font-size: 25px;
    font-weight: 800;
    color: #047857;
}

.confidence-track {
    width: 100%;
    height: 15px;
    background: #d1fae5;
    border-radius: 20px;
    overflow: hidden;
    margin-top: 10px;
}

.confidence-fill {
    height: 15px;
    background: linear-gradient(
        90deg,
        #10b981,
        #059669
    );
    border-radius: 20px;
}

/* ADVICE */

.advice-box {
    background: #fff7ed;
    border-left: 6px solid #f97316;
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
}

.warning-box {
    background: #fef2f2;
    border-left: 6px solid #ef4444;
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
}

/* CHAT */

.chat-container {
    background: white;
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid #bbf7d0;
}

.chat-welcome {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    padding: 20px;
    border-radius: 18px;
    border-left: 6px solid #059669;
    margin-bottom: 20px;
}

.chat-welcome h3 {
    color: #065f46;
    margin-top: 0;
}

.quick-title {
    color: #065f46;
    font-weight: 700;
    margin-top: 18px;
    margin-bottom: 10px;
}

.category-box {
    background: #f0fdf4;
    padding: 15px;
    border-radius: 15px;
    margin-top: 15px;
    margin-bottom: 10px;
    border: 1px solid #bbf7d0;
}

.category-title {
    color: #047857;
    font-weight: 700;
}

/* STEPS */

.step {
    background: white;
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #d1fae5;
    box-shadow: 0 5px 18px rgba(0,0,0,0.06);
}

.step-number {
    background: #059669;
    color: white;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    font-weight: 800;
    font-size: 18px;
}

/* FOOTER */

.footer {
    text-align: center;
    padding: 30px 10px 10px;
    color: #6b7280;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LANGUAGE
# --------------------------------------------------

language = st.radio(
    "Language",
    ["🇬🇧 English", "🇮🇳 ಕನ್ನಡ"],
    horizontal=True,
    label_visibility="collapsed"
)

is_kannada = language == "🇮🇳 ಕನ್ನಡ"


# --------------------------------------------------
# HERO
# --------------------------------------------------

if is_kannada:
    hero_title = "🍄 ಮಶ್ರೂಮ್ AI ಸಹಾಯಕ"
    hero_subtitle = "ಸ್ಮಾರ್ಟ್ ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ ಮತ್ತು ರೈತ ಸಹಾಯ"
    hero_desc = "ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಮಶ್ರೂಮ್ ರೋಗದ ಬಗ್ಗೆ ಸರಳ ರೈತ ಸ್ನೇಹಿ ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಿರಿ."
else:
    hero_title = "🍄 Mushroom AI Assistant"
    hero_subtitle = "Smart Mushroom Disease Detection & Farmer Support"
    hero_desc = "Upload a mushroom image and receive simple, farmer-friendly disease guidance."

st.markdown(f"""
<div class="hero">

<div class="hero-badge">
🌱 AI Powered Agriculture • Smart Farming
</div>

<h1>{hero_title}</h1>

<h3>{hero_subtitle}</h3>

<p>{hero_desc}</p>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🌿 Smart Farming Dashboard</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
    <div class="card-icon">🔬</div>
    <h3>AI Disease Detection</h3>
    <p>Detect common mushroom diseases using an image.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <div class="card-icon">🌱</div>
    <h3>Farmer Guidance</h3>
    <p>Get simple practical advice for mushroom care.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <div class="card-icon">💬</div>
    <h3>AI Farmer Assistant</h3>
    <p>Ask questions about mushroom diseases and farming.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
    <div class="card-icon">📊</div>
    <h3>Disease Insights</h3>
    <p>Learn about common mushroom diseases.</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "mushroom_disease_mobilenetv2.keras"
    )


model = load_model()

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


# --------------------------------------------------
# FARMER ADVICE
# --------------------------------------------------

advice = {

"Healthy": {
"en": "The mushroom appears healthy. Maintain good hygiene, suitable moisture and proper ventilation.",
"kn": "ಮಶ್ರೂಮ್ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತದೆ. ಉತ್ತಮ ಸ್ವಚ್ಛತೆ, ಸೂಕ್ತ ತೇವಾಂಶ ಮತ್ತು ಸರಿಯಾದ ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
},

"Bacterial Blotch": {
"en": "Maintain hygiene, avoid excess surface moisture and improve ventilation.",
"kn": "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ, ಹೆಚ್ಚುವರಿ ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ ಮತ್ತು ಗಾಳಿಯ ಹರಿವನ್ನು ಸುಧಾರಿಸಿ."
},

"Dry Bubble": {
"en": "Remove infected mushrooms carefully and maintain proper growing-room hygiene.",
"kn": "ಸೋಂಕಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಬೆಳೆಯುವ ಕೊಠಡಿಯಲ್ಲಿ ಉತ್ತಮ ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
},

"Cobweb": {
"en": "Remove affected areas, maintain cleanliness and avoid excessive humidity.",
"kn": "ಬಾಧಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ, ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ ಮತ್ತು ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."
},

"Wet Bubble": {
"en": "Remove infected material carefully and maintain proper hygiene and moisture control.",
"kn": "ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಉತ್ತಮ ಸ್ವಚ್ಛತೆ ಹಾಗೂ ತೇವಾಂಶ ನಿಯಂತ್ರಣವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
}

}


# --------------------------------------------------
# DETECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🔬 Mushroom Disease Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="detect-box">',
    unsafe_allow_html=True
)

if is_kannada:
    st.write("📷 ಮಶ್ರೂಮ್‌ನ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.")
else:
    st.write("📷 Upload a clear image of the mushroom.")

uploaded_file = st.file_uploader(
    "Upload image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.image(
        image,
        caption="Uploaded Mushroom",
        width=350
    )

    # Resize for model

    img = image.resize(
        (224, 224)
    )

    # Normalize

    img_array = np.array(img) / 255.0

    # Add batch dimension

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # Prediction

    prediction = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = np.argmax(
        prediction[0]
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = (
        float(
            prediction[0][predicted_index]
        ) * 100
    )

    display_name = (
        kannada_names[predicted_class]
        if is_kannada
        else predicted_class
    )


    # --------------------------------------------------
    # RESULT STATUS
    # --------------------------------------------------

    if predicted_class == "Healthy":

        status_html = (
            '<span class="status-healthy">'
            '🟢 Healthy'
            '</span>'
        )

        status_kn = "🟢 ಆರೋಗ್ಯಕರ"

    else:

        status_html = (
            '<span class="status-disease">'
            '🔴 Disease Detected'
            '</span>'
        )

        status_kn = "🔴 ರೋಗ ಪತ್ತೆಯಾಗಿದೆ"


    # --------------------------------------------------
    # MAIN RESULT
    # --------------------------------------------------

    st.markdown(f"""
    <div class="result-box">

        <div class="result-title">
        {'🔍 ಪತ್ತೆಯಾದ ಫಲಿತಾಂಶ' if is_kannada else '🔍 Detection Result'}
        </div>

        <div class="result-disease">
        {display_name}
        </div>

        {
            status_kn
            if is_kannada
            else status_html
        }

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------
    # CONFIDENCE BAR
    # --------------------------------------------------

    confidence_width = min(
        max(confidence, 0),
        100
    )

    st.markdown(f"""
    <div class="confidence-box">

        <div>
        {'📊 ವಿಶ್ವಾಸ ಮಟ್ಟ' if is_kannada else '📊 Prediction Confidence'}
        </div>

        <div class="confidence-number">
        {confidence:.2f}%
        </div>

        <div class="confidence-track">

            <div
            class="confidence-fill"
            style="width:{confidence_width}%;">
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    # --------------------------------------------------
    # RECOMMENDED ACTION
    # --------------------------------------------------

    if predicted_class == "Healthy":

        if is_kannada:

            st.markdown("""
            <div class="advice-box">

            <b>🌱 ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮ</b>

            <p>
            ಮಶ್ರೂಮ್ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತದೆ.
            ಉತ್ತಮ ಸ್ವಚ್ಛತೆ, ಸೂಕ್ತ ತೇವಾಂಶ ಮತ್ತು
            ಗಾಳಿಯ ಹರಿವನ್ನು ಮುಂದುವರಿಸಿ.
            </p>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="advice-box">

            <b>🌱 Recommended Action</b>

            <p>
            The mushroom appears healthy.
            Continue good hygiene, suitable
            moisture and proper ventilation.
            </p>

            </div>
            """, unsafe_allow_html=True)

    else:

        advice_text = advice[
            predicted_class
        ][
            "kn" if is_kannada else "en"
        ]

        if is_kannada:

            st.markdown(f"""
            <div class="warning-box">

            <b>⚠️ ರೋಗ ಪತ್ತೆಯಾಗಿದೆ</b>

            <p>
            ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರದಲ್ಲಿ
            <b>{display_name}</b> ಎಂದು ಮಾದರಿ
            ಗುರುತಿಸಿದೆ.
            </p>

            <p>
            <b>🌱 ಶಿಫಾರಸು:</b><br>
            {advice_text}
            </p>

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="warning-box">

            <b>⚠️ Disease Detected</b>

            <p>
            The model identified
            <b>{display_name}</b>
            in the uploaded image.
            </p>

            <p>
            <b>🌱 Recommended Action:</b><br>
            {advice_text}
            </p>

            </div>
            """, unsafe_allow_html=True)


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# FARMER ADVICE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🌱 Useful Farmer Advice</div>',
    unsafe_allow_html=True
)

a1, a2, a3, a4 = st.columns(4)

with a1:
    st.markdown("""
    <div class="card">
    <div class="card-icon">🧼</div>
    <h3>Hygiene</h3>
    <p>Keep the growing area and tools clean.</p>
    </div>
    """, unsafe_allow_html=True)

with a2:
    st.markdown("""
    <div class="card">
    <div class="card-icon">💧</div>
    <h3>Moisture Control</h3>
    <p>Avoid excessive moisture on mushroom surfaces.</p>
    </div>
    """, unsafe_allow_html=True)

with a3:
    st.markdown("""
    <div class="card">
    <div class="card-icon">🌬️</div>
    <h3>Ventilation</h3>
    <p>Maintain proper air circulation.</p>
    </div>
    """, unsafe_allow_html=True)

with a4:
    st.markdown("""
    <div class="card">
    <div class="card-icon">👀</div>
    <h3>Inspection</h3>
    <p>Check mushrooms regularly for unusual changes.</p>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# SUPPORTED DISEASES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🦠 Supported Diseases</div>',
    unsafe_allow_html=True
)

d1, d2, d3, d4, d5 = st.columns(5)

diseases = [
    ("🍄", "Healthy"),
    ("🦠", "Bacterial Blotch"),
    ("⚪", "Dry Bubble"),
    ("🕸️", "Cobweb"),
    ("💧", "Wet Bubble")
]

for col, (icon, name) in zip(
    [d1, d2, d3, d4, d5],
    diseases
):

    with col:

        display_name = (
            kannada_names[name]
            if is_kannada
            else name
        )

        st.markdown(f"""
        <div class="card" style="text-align:center;">

        <div class="card-icon">
        {icon}
        </div>

        <b>
        {display_name}
        </b>

        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">⚙️ How It Works</div>',
    unsafe_allow_html=True
)

h1, h2, h3 = st.columns(3)

with h1:
    st.markdown("""
    <div class="step">

    <div class="step-number">1</div>

    <h3>📷 Upload</h3>

    <p>
    Upload a mushroom image.
    </p>

    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown("""
    <div class="step">

    <div class="step-number">2</div>

    <h3>🤖 Analyze</h3>

    <p>
    MobileNetV2 analyzes the image.
    </p>

    </div>
    """, unsafe_allow_html=True)

with h3:
    st.markdown("""
    <div class="step">

    <div class="step-number">3</div>

    <h3>🌱 Guidance</h3>

    <p>
    Receive disease information and farmer advice.
    </p>

    </div>
    """, unsafe_allow_html=True)


# ==================================================
# FARMER ASSISTANT
# ==================================================

st.markdown(
    '<div class="section-title">💬 AI Farmer Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chat-container">',
    unsafe_allow_html=True
)


if is_kannada:

    st.markdown("""
    <div class="chat-welcome">

    <h3>👋 ನಮಸ್ಕಾರ ರೈತರೆ!</h3>

    <p>
    ಮಶ್ರೂಮ್ ರೋಗಗಳು, ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆ,
    ಸ್ವಚ್ಛತೆ, ತೇವಾಂಶ ಮತ್ತು ಗಾಳಿಯ ಹರಿವಿನ
    ಬಗ್ಗೆ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ.
    </p>

    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div class="chat-welcome">

    <h3>👋 Hello Farmer!</h3>

    <p>
    Ask me about mushroom diseases,
    prevention, hygiene, moisture,
    ventilation and taking good photos.
    </p>

    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# CHATBOT FUNCTION
# --------------------------------------------------

def get_chatbot_response(
    question,
    kannada
):

    q = question.lower()

    if kannada:

        if "ಬ್ಯಾಕ್ಟೀರಿಯಲ್" in q or "blotch" in q:

            return (
                "🦠 **ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್:** "
                "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ, "
                "ಹೆಚ್ಚುವರಿ ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ "
                "ಮತ್ತು ಗಾಳಿಯ ಹರಿವನ್ನು ಸುಧಾರಿಸಿ."
            )

        elif "ಡ್ರೈ ಬಬಲ್" in q:

            return (
                "⚪ **ಡ್ರೈ ಬಬಲ್:** "
                "ಬಾಧಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ "
                "ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಬೆಳೆಯುವ ಪ್ರದೇಶವನ್ನು "
                "ಸ್ವಚ್ಛವಾಗಿಡಿ."
            )

        elif "ಕಾಬ್" in q or "cobweb" in q:

            return (
                "🕸️ **ಕಾಬ್‌ವೆಬ್:** "
                "ಬಾಧಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ, "
                "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ ಮತ್ತು "
                "ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."
            )

        elif "ವೆಟ್ ಬಬಲ್" in q:

            return (
                "💧 **ವೆಟ್ ಬಬಲ್:** "
                "ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ "
                "ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಸ್ವಚ್ಛತೆ ಹಾಗೂ "
                "ತೇವಾಂಶ ನಿಯಂತ್ರಣವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )

        elif "ತಡೆ" in q or "prevent" in q:

            return (
                "🌱 **ರೋಗ ತಡೆಗಟ್ಟಲು:** "
                "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ, "
                "ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ, "
                "ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವು ಇರಲಿ ಮತ್ತು "
                "ಮಶ್ರೂಮ್‌ಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
            )

        elif "ಫೋಟೋ" in q or "ಚಿತ್ರ" in q:

            return (
                "📷 **ಉತ್ತಮ ಫೋಟೋ:** "
                "ಉತ್ತಮ ಬೆಳಕಿನಲ್ಲಿ ಸ್ಪಷ್ಟವಾದ ಚಿತ್ರ ತೆಗೆದುಕೊಳ್ಳಿ. "
                "ಮಶ್ರೂಮ್ ಸಂಪೂರ್ಣವಾಗಿ ಕಾಣುವಂತೆ ಮಾಡಿ ಮತ್ತು "
                "ಮಸುಕಾದ ಚಿತ್ರಗಳನ್ನು ತಪ್ಪಿಸಿ."
            )

        elif "ಸ್ವಚ್ಛ" in q:

            return (
                "🧼 ಬೆಳೆಯುವ ಕೊಠಡಿ, ಉಪಕರಣಗಳು "
                "ಮತ್ತು ಕೈಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ."
            )

        elif "ತೇವಾಂಶ" in q:

            return (
                "💧 ಅತಿಯಾದ ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು "
                "ತಪ್ಪಿಸಿ ಮತ್ತು ಸೂಕ್ತ ತೇವಾಂಶವನ್ನು "
                "ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )

        elif "ಗಾಳಿ" in q or "ವಾತಾಯನ" in q:

            return (
                "🌬️ ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವು "
                "ಬೆಳೆಯುವ ಪರಿಸರವನ್ನು ಸೂಕ್ತವಾಗಿಡಲು "
                "ಸಹಾಯ ಮಾಡುತ್ತದೆ."
            )

        else:

            return (
                "🌱 ರೋಗ, ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆ, "
                "ಸ್ವಚ್ಛತೆ, ತೇವಾಂಶ ಅಥವಾ "
                "ಗಾಳಿಯ ಹರಿವಿನ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ."
            )

    else:

        if "bacterial" in q or "blotch" in q:

            return (
                "🦠 **Bacterial Blotch:** "
                "Maintain hygiene, avoid excess "
                "surface moisture and improve ventilation."
            )

        elif "dry bubble" in q:

            return (
                "⚪ **Dry Bubble:** "
                "Carefully remove affected mushrooms "
                "and maintain good growing-room hygiene."
            )

        elif "cobweb" in q:

            return (
                "🕸️ **Cobweb:** "
                "Remove affected areas, maintain "
                "cleanliness and avoid excessive humidity."
            )

        elif "wet bubble" in q:

            return (
                "💧 **Wet Bubble:** "
                "Carefully remove infected material "
                "and maintain hygiene and moisture control."
            )

        elif "prevent" in q:

            return (
                "🌱 **Disease Prevention:** "
                "Maintain good hygiene, avoid excessive "
                "moisture, provide suitable ventilation "
                "and inspect mushrooms regularly."
            )

        elif "photo" in q or "picture" in q:

            return (
                "📷 **Good Mushroom Photo:** "
                "Use good lighting, keep the mushroom "
                "clearly visible and avoid blurry images."
            )

        elif "hygiene" in q or "clean" in q:

            return (
                "🧼 Keep the growing room, tools "
                "and hands clean."
            )

        elif "moisture" in q or "humidity" in q:

            return (
                "💧 Avoid excessive surface moisture "
                "and maintain suitable moisture conditions."
            )

        elif "ventilation" in q or "air" in q:

            return (
                "🌬️ Good air circulation helps "
                "maintain a suitable growing environment."
            )

        else:

            return (
                "🌱 Ask me about diseases, prevention, "
                "hygiene, moisture, ventilation or "
                "taking a good mushroom photo."
            )


# --------------------------------------------------
# QUICK QUESTIONS
# --------------------------------------------------

st.markdown(
    '<div class="quick-title">⚡ Quick Questions</div>',
    unsafe_allow_html=True
)

if is_kannada:

    questions = [
        "🦠 ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್ ಎಂದರೇನು?",
        "⚪ ಡ್ರೈ ಬಬಲ್ ಬಗ್ಗೆ ತಿಳಿಸಿ",
        "🕸️ ಕಾಬ್‌ವೆಬ್ ಬಗ್ಗೆ ತಿಳಿಸಿ",
        "💧 ವೆಟ್ ಬಬಲ್ ಬಗ್ಗೆ ತಿಳಿಸಿ",
        "🌱 ರೋಗಗಳನ್ನು ಹೇಗೆ ತಡೆಯುವುದು?",
        "🧼 ಸ್ವಚ್ಛತೆಯನ್ನು ಹೇಗೆ ಕಾಪಾಡುವುದು?",
        "💧 ತೇವಾಂಶವನ್ನು ಹೇಗೆ ನಿಯಂತ್ರಿಸುವುದು?",
        "🌬️ ಗಾಳಿಯ ಹರಿವು ಏಕೆ ಮುಖ್ಯ?",
        "📷 ಉತ್ತಮ ಫೋಟೋ ಹೇಗೆ ತೆಗೆದುಕೊಳ್ಳುವುದು?"
    ]

else:

    questions = [
        "🦠 What is Bacterial Blotch?",
        "⚪ Tell me about Dry Bubble",
        "🕸️ Tell me about Cobweb",
        "💧 Tell me about Wet Bubble",
        "🌱 How can I prevent diseases?",
        "🧼 How should I maintain hygiene?",
        "💧 How can I control moisture?",
        "🌬️ Why is ventilation important?",
        "📷 How should I take a good photo?"
    ]


selected_question = None

question_cols = st.columns(3)

for i, question in enumerate(questions):

    with question_cols[i % 3]:

        if st.button(
            question,
            use_container_width=True
        ):

            selected_question = question


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_question = st.chat_input(
    "Ask your question..."
    if not is_kannada
    else
    "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
)

if selected_question:

    user_question = selected_question


# --------------------------------------------------
# PROCESS
# --------------------------------------------------

if user_question:

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    response = get_chatbot_response(
        user_question,
        is_kannada
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()


# --------------------------------------------------
# CLEAR CHAT
# --------------------------------------------------

if st.session_state.messages:

    if st.button(
        "🗑️ Clear Chat"
        if not is_kannada
        else
        "🗑️ ಚಾಟ್ ತೆರವುಗೊಳಿಸಿ",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

if is_kannada:

    st.info(
        "⚠️ AI ಫಲಿತಾಂಶವು ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ಮಾತ್ರ. "
        "ಗಂಭೀರ ಸಮಸ್ಯೆಗಳಿದ್ದರೆ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
    )

else:

    st.info(
        "⚠️ AI results are for preliminary guidance only. "
        "For serious problems, consult an agricultural expert."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">

🍄 <b>Mushroom AI Assistant</b><br>

AI Based Mushroom Disease Detection Using
Image Processing & Deep Learning<br><br>

🌱 Smart Farming • 🤖 Artificial Intelligence • 👨‍🌾 Farmer Support

</div>
""", unsafe_allow_html=True)
