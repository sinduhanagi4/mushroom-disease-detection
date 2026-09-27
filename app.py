import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PAGE STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f0fdf4;
    }

    .section-title {
        color: #065f46;
        font-size: 28px;
        font-weight: 800;
        margin-top: 20px;
    }

    /* HERO */

    .hero-box {
        background: linear-gradient(
            135deg,
            #064e3b,
            #047857,
            #10b981
        );

        padding: 45px 30px;
        border-radius: 25px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 35px;

        box-shadow:
            0 10px 30px rgba(0, 100, 70, 0.20);
    }

    .hero-badge {
        display: inline-block;

        background: rgba(255,255,255,0.18);

        color: white;

        padding: 10px 20px;

        border-radius: 30px;

        font-size: 15px;

        margin-bottom: 18px;
    }

    .hero-title {
        color: white;

        font-size: 44px;

        font-weight: 800;

        margin: 10px 0;
    }

    .hero-subtitle {
        color: #d1fae5;

        font-size: 22px;

        font-weight: 600;

        margin-bottom: 12px;
    }

    .hero-description {
        color: #ecfdf5;

        font-size: 17px;

        max-width: 750px;

        margin: auto;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LANGUAGE SELECTION
# ============================================================

language = st.radio(
    "🌐 Select Language / ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ",
    ["🇬🇧 English", "🇮🇳 ಕನ್ನಡ"],
    horizontal=True
)

is_kannada = language == "🇮🇳 ಕನ್ನಡ"


# ============================================================
# HERO SECTION
# ============================================================

# ============================================================
# HERO SECTION - NO HTML
# ============================================================

if is_kannada:

    hero_badge = "🌱 AI ಆಧಾರಿತ ಕೃಷಿ • ಸ್ಮಾರ್ಟ್ ಫಾರ್ಮಿಂಗ್"
    hero_title = "🍄 ಮಶ್ರೂಮ್ AI ಸಹಾಯಕ"
    hero_subtitle = "ಸ್ಮಾರ್ಟ್ ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ ಮತ್ತು ರೈತ ಸಹಾಯ"
    hero_description = (
        "ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು "
        "ಸರಳ ರೈತ ಸ್ನೇಹಿ ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಿರಿ."
    )

else:

    hero_badge = "🌱 AI Powered Agriculture • Smart Farming"
    hero_title = "🍄 Mushroom AI Assistant"
    hero_subtitle = "Smart Mushroom Disease Detection & Farmer Support"
    hero_description = (
        "Upload a mushroom image and receive simple, "
        "farmer-friendly disease guidance."
    )


# Highlighted badge
st.success(hero_badge)


# Centered title
left, center, right = st.columns([1, 3, 1])

with center:

    st.markdown(
        f"## {hero_title}"
    )

    st.markdown(
        f"### {hero_subtitle}"
    )

    st.write(
        hero_description
    )


st.divider()

# ============================================================
# DASHBOARD
# ============================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">'
        '🌿 ಸ್ಮಾರ್ಟ್ ಫಾರ್ಮಿಂಗ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್'
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-title">'
        '🌿 Smart Farming Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🔬 AI Detection",
        "5 Diseases"
    )


with col2:

    st.metric(
        "🤖 Model",
        "MobileNetV2"
    )


with col3:

    st.metric(
        "📷 Input",
        "Image"
    )


with col4:

    st.metric(
        "🌱 Support",
        "Farmer"
    )


st.divider()


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return tf.keras.models.load_model(
        "mushroom_disease_mobilenetv2.keras"
    )


try:

    model = load_model()

except Exception as e:

    st.error(
        "❌ Model could not be loaded."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# CLASS NAMES
# ============================================================

class_names = [
    "Healthy",
    "Bacterial Blotch",
    "Dry Bubble",
    "Cobweb",
    "Wet Bubble"
]


kannada_names = {

    "Healthy": "ಆರೋಗ್ಯಕರ",

    "Bacterial Blotch":
        "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್",

    "Dry Bubble":
        "ಡ್ರೈ ಬಬಲ್",

    "Cobweb":
        "ಕಾಬ್‌ವೆಬ್",

    "Wet Bubble":
        "ವೆಟ್ ಬಬಲ್"
}


# ============================================================
# FARMER ADVICE
# ============================================================

advice = {

    "Healthy": {

        "en":
            "The mushroom appears healthy. "
            "Maintain good hygiene, suitable moisture "
            "and proper ventilation.",

        "kn":
            "ಮಶ್ರೂಮ್ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತದೆ. "
            "ಉತ್ತಮ ಸ್ವಚ್ಛತೆ, ಸೂಕ್ತ ತೇವಾಂಶ ಮತ್ತು "
            "ಸರಿಯಾದ ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
    },

    "Bacterial Blotch": {

        "en":
            "Maintain hygiene, avoid excess surface "
            "moisture and improve ventilation.",

        "kn":
            "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ, ಹೆಚ್ಚುವರಿ "
            "ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ ಮತ್ತು "
            "ಗಾಳಿಯ ಹರಿವನ್ನು ಸುಧಾರಿಸಿ."
    },

    "Dry Bubble": {

        "en":
            "Remove infected mushrooms carefully "
            "and maintain proper growing-room hygiene.",

        "kn":
            "ಸೋಂಕಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ "
            "ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಬೆಳೆಯುವ ಕೊಠಡಿಯಲ್ಲಿ "
            "ಉತ್ತಮ ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
    },

    "Cobweb": {

        "en":
            "Remove affected areas, maintain cleanliness "
            "and avoid excessive humidity.",

        "kn":
            "ಬಾಧಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ, ಸ್ವಚ್ಛತೆಯನ್ನು "
            "ಕಾಪಾಡಿಕೊಳ್ಳಿ ಮತ್ತು ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."
    },

    "Wet Bubble": {

        "en":
            "Remove infected material carefully and "
            "maintain proper hygiene and moisture control.",

        "kn":
            "ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ "
            "ಮತ್ತು ಉತ್ತಮ ಸ್ವಚ್ಛತೆ ಹಾಗೂ ತೇವಾಂಶ "
            "ನಿಯಂತ್ರಣವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
    }
}


# ============================================================
# DISEASE DETECTION
# ============================================================

if is_kannada:

    st.markdown(
        '<div class="section-title">'
        '🔬 ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "📷 ಮಶ್ರೂಮ್‌ನ ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
    )

else:

    st.markdown(
        '<div class="section-title">'
        '🔬 Mushroom Disease Detection'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "📷 Upload a clear image of the mushroom."
    )


uploaded_file = st.file_uploader(
    "Choose a mushroom image",
    type=["jpg", "jpeg", "png"]
)


# ============================================================
# PREDICTION
# ============================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")


    st.subheader("📷 Uploaded Mushroom")

    st.image(
        image,
        width=400
    )


    # --------------------------------------------------------
    # PREPROCESS IMAGE
    # --------------------------------------------------------

    img = image.resize(
        (224, 224)
    )

    img_array = np.array(
        img
    )

    img_array = img_array / 255.0

    img_array = np.expand_dims(
        img_array,
        axis=0
    )


    # --------------------------------------------------------
    # PREDICT
    # --------------------------------------------------------

    with st.spinner(
        "🤖 Analyzing mushroom..."
        if not is_kannada
        else
        "🤖 ಮಶ್ರೂಮ್ ಅನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ..."
    ):

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


    if is_kannada:

        display_name = kannada_names[
            predicted_class
        ]

    else:

        display_name = predicted_class


    # ========================================================
    # RESULT
    # ========================================================

    st.divider()

    if is_kannada:

        st.subheader(
            "🔍 ಪತ್ತೆಯಾದ ಫಲಿತಾಂಶ"
        )

    else:

        st.subheader(
            "🔍 Detection Result"
        )


    if predicted_class == "Healthy":

        st.success(
            f"🟢 {display_name}"
        )

    else:

        if is_kannada:

            st.error(
                f"🔴 ರೋಗ ಪತ್ತೆಯಾಗಿದೆ: {display_name}"
            )

        else:

            st.error(
                f"🔴 Disease Detected: {display_name}"
            )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    if is_kannada:

        st.subheader(
            "📊 ವಿಶ್ವಾಸ ಮಟ್ಟ"
        )

    else:

        st.subheader(
            "📊 Prediction Confidence"
        )


    st.metric(
        "Confidence",
        f"{confidence:.2f}%"
    )


    st.progress(
        min(
            max(
                confidence / 100,
                0.0
            ),
            1.0
        )
    )


    # ========================================================
    # FARMER RECOMMENDATION
    # ========================================================

    advice_text = advice[
        predicted_class
    ][
        "kn" if is_kannada else "en"
    ]


    if predicted_class == "Healthy":

        st.success(
            (
                f"🌱 **ಶಿಫಾರಸು:** {advice_text}"
                if is_kannada
                else
                f"🌱 **Recommended Action:** {advice_text}"
            )
        )

    else:

        st.warning(
            (
                f"⚠️ **ರೈತರಿಗೆ ಸಲಹೆ:** {advice_text}"
                if is_kannada
                else
                f"⚠️ **Farmer Advice:** {advice_text}"
            )
        )


# ============================================================
# GENERAL FARMER ADVICE
# ============================================================

st.divider()


if is_kannada:

    st.markdown(
        '<div class="section-title">'
        '🌱 ರೈತರಿಗೆ ಉಪಯುಕ್ತ ಸಲಹೆಗಳು'
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-title">'
        '🌱 Useful Farmer Advice'
        '</div>',
        unsafe_allow_html=True
    )


a1, a2, a3, a4 = st.columns(4)


with a1:

    st.info(
        "🧼 **Hygiene**\n\n"
        "Keep the growing area and tools clean."
    )


with a2:

    st.info(
        "💧 **Moisture Control**\n\n"
        "Avoid excessive surface moisture."
    )


with a3:

    st.info(
        "🌬️ **Ventilation**\n\n"
        "Maintain proper air circulation."
    )


with a4:

    st.info(
        "👀 **Regular Inspection**\n\n"
        "Check mushrooms regularly."
    )


# ============================================================
# SUPPORTED DISEASES
# ============================================================

st.divider()


if is_kannada:

    st.markdown(
        '<div class="section-title">'
        '🦠 ಪತ್ತೆಹಚ್ಚಬಹುದಾದ ರೋಗಗಳು'
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-title">'
        '🦠 Supported Diseases'
        '</div>',
        unsafe_allow_html=True
    )


d1, d2, d3, d4, d5 = st.columns(5)


disease_columns = [
    d1,
    d2,
    d3,
    d4,
    d5
]


disease_icons = [
    "🍄",
    "🦠",
    "⚪",
    "🕸️",
    "💧"
]


for column, disease, icon in zip(
    disease_columns,
    class_names,
    disease_icons
):

    with column:

        name = (
            kannada_names[disease]
            if is_kannada
            else disease
        )

        st.info(
            f"{icon} **{name}**"
        )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()


if is_kannada:

    st.markdown(
        '<div class="section-title">'
        '⚙️ ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?'
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-title">'
        '⚙️ How It Works'
        '</div>',
        unsafe_allow_html=True
    )


h1, h2, h3 = st.columns(3)


with h1:

    st.success(
        "### 1️⃣ Upload\n\n"
        "Upload a mushroom image."
    )


with h2:

    st.success(
        "### 2️⃣ Analyze\n\n"
        "MobileNetV2 analyzes the image."
    )


with h3:

    st.success(
        "### 3️⃣ Guidance\n\n"
        "Receive disease information and advice."
    )


# ============================================================
# FARMER ASSISTANT
# ============================================================

st.divider()


st.markdown(
    '<div class="section-title">'
    '💬 AI Farmer Assistant'
    '</div>',
    unsafe_allow_html=True
)


if is_kannada:

    st.info(
        "👋 **ನಮಸ್ಕಾರ ರೈತರೆ!**\n\n"
        "ಮಶ್ರೂಮ್ ರೋಗಗಳು, ಸ್ವಚ್ಛತೆ, "
        "ತೇವಾಂಶ, ಗಾಳಿಯ ಹರಿವು ಮತ್ತು "
        "ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ."
    )

else:

    st.info(
        "👋 **Hello Farmer!**\n\n"
        "Ask about mushroom diseases, hygiene, "
        "moisture, ventilation and disease prevention."
    )


# ============================================================
# CHATBOT FUNCTION
# ============================================================

def get_chatbot_response(
    question,
    kannada
):

    q = question.lower()


    # ========================================================
    # KANNADA
    # ========================================================

    if kannada:

        if (
            "ಬ್ಯಾಕ್ಟೀರಿಯಲ್" in q
            or
            "blotch" in q
        ):

            return (
                "🦠 **ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್:**\n\n"
                "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ, "
                "ಹೆಚ್ಚುವರಿ ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ "
                "ಮತ್ತು ಗಾಳಿಯ ಹರಿವನ್ನು ಸುಧಾರಿಸಿ."
            )


        if "ಡ್ರೈ ಬಬಲ್" in q:

            return (
                "⚪ **ಡ್ರೈ ಬಬಲ್:**\n\n"
                "ಸೋಂಕಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ "
                "ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಬೆಳೆಯುವ ಪ್ರದೇಶವನ್ನು "
                "ಸ್ವಚ್ಛವಾಗಿಡಿ."
            )


        if (
            "ಕಾಬ್" in q
            or
            "cobweb" in q
        ):

            return (
                "🕸️ **ಕಾಬ್‌ವೆಬ್:**\n\n"
                "ಬಾಧಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ, "
                "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ ಮತ್ತು "
                "ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."
            )


        if "ವೆಟ್ ಬಬಲ್" in q:

            return (
                "💧 **ವೆಟ್ ಬಬಲ್:**\n\n"
                "ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ "
                "ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಸ್ವಚ್ಛತೆ ಹಾಗೂ "
                "ತೇವಾಂಶ ನಿಯಂತ್ರಣವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )


        if (
            "ತಡೆ" in q
            or
            "prevent" in q
        ):

            return (
                "🌱 **ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆ:**\n\n"
                "ಉತ್ತಮ ಸ್ವಚ್ಛತೆ ಕಾಪಾಡಿಕೊಳ್ಳಿ, "
                "ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ, "
                "ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವು ಇರಲಿ ಮತ್ತು "
                "ಮಶ್ರೂಮ್‌ಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
            )


        if (
            "ಸ್ವಚ್ಛ" in q
            or
            "hygiene" in q
        ):

            return (
                "🧼 ಬೆಳೆಯುವ ಕೊಠಡಿ, ಉಪಕರಣಗಳು "
                "ಮತ್ತು ಕೈಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ."
            )


        if (
            "ತೇವಾಂಶ" in q
            or
            "moisture" in q
        ):

            return (
                "💧 ಅತಿಯಾದ ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು "
                "ತಪ್ಪಿಸಿ ಮತ್ತು ಸೂಕ್ತ ತೇವಾಂಶವನ್ನು "
                "ಕಾಪಾಡಿಕೊಳ್ಳಿ."
            )


        if (
            "ಗಾಳಿ" in q
            or
            "ವಾತಾಯನ" in q
            or
            "ventilation" in q
        ):

            return (
                "🌬️ ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವು "
                "ಬೆಳೆಯುವ ಪರಿಸರವನ್ನು ಸೂಕ್ತವಾಗಿಡಲು "
                "ಸಹಾಯ ಮಾಡುತ್ತದೆ."
            )


        if (
            "ಫೋಟೋ" in q
            or
            "ಚಿತ್ರ" in q
        ):

            return (
                "📷 ಉತ್ತಮ ಫೋಟೋ ತೆಗೆದುಕೊಳ್ಳಲು "
                "ಉತ್ತಮ ಬೆಳಕನ್ನು ಬಳಸಿ. "
                "ಮಶ್ರೂಮ್ ಸ್ಪಷ್ಟವಾಗಿ ಕಾಣಬೇಕು "
                "ಮತ್ತು ಚಿತ್ರ ಮಸುಕಾಗಿರಬಾರದು."
            )


        return (
            "🌱 ದಯವಿಟ್ಟು ರೋಗ, ಸ್ವಚ್ಛತೆ, "
            "ತೇವಾಂಶ, ಗಾಳಿಯ ಹರಿವು ಅಥವಾ "
            "ರೋಗ ತಡೆಗಟ್ಟುವಿಕೆಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ."
        )


    # ========================================================
    # ENGLISH
    # ========================================================

    else:

        if (
            "bacterial" in q
            or
            "blotch" in q
        ):

            return (
                "🦠 **Bacterial Blotch:**\n\n"
                "Maintain hygiene, avoid excess surface "
                "moisture and improve ventilation."
            )


        if "dry bubble" in q:

            return (
                "⚪ **Dry Bubble:**\n\n"
                "Carefully remove affected mushrooms "
                "and maintain good growing-room hygiene."
            )


        if "cobweb" in q:

            return (
                "🕸️ **Cobweb:**\n\n"
                "Remove affected areas, maintain "
                "cleanliness and avoid excessive humidity."
            )


        if "wet bubble" in q:

            return (
                "💧 **Wet Bubble:**\n\n"
                "Carefully remove infected material "
                "and maintain hygiene and moisture control."
            )


        if (
            "prevent" in q
            or
            "prevention" in q
        ):

            return (
                "🌱 **Disease Prevention:**\n\n"
                "Maintain good hygiene, avoid excessive "
                "moisture, provide suitable ventilation "
                "and inspect mushrooms regularly."
            )


        if (
            "hygiene" in q
            or
            "clean" in q
        ):

            return (
                "🧼 Keep the growing room, tools "
                "and hands clean."
            )


        if (
            "moisture" in q
            or
            "humidity" in q
        ):

            return (
                "💧 Avoid excessive surface moisture "
                "and maintain suitable moisture conditions."
            )


        if (
            "ventilation" in q
            or
            "air" in q
        ):

            return (
                "🌬️ Good air circulation helps "
                "maintain a suitable growing environment."
            )


        if (
            "photo" in q
            or
            "picture" in q
            or
            "image" in q
        ):

            return (
                "📷 **Good Mushroom Photo:**\n\n"
                "Use good lighting, keep the mushroom "
                "clearly visible and avoid blurry images."
            )


        return (
            "🌱 Ask me about diseases, prevention, "
            "hygiene, moisture, ventilation or "
            "taking a good mushroom photo."
        )


# ============================================================
# QUICK QUESTIONS
# ============================================================

if is_kannada:

    quick_questions = [

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

    quick_questions = [

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


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# QUICK QUESTION BUTTONS
# ============================================================

st.subheader("⚡ Quick Questions")


q1, q2, q3 = st.columns(3)


selected_question = None


for i, question in enumerate(
    quick_questions
):

    column = [
        q1,
        q2,
        q3
    ][i % 3]


    with column:

        if st.button(
            question,
            use_container_width=True,
            key=f"quick_{i}"
        ):

            selected_question = question


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Ask your question..."
    if not is_kannada
    else
    "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
)


if selected_question is not None:

    user_question = selected_question


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )


    response = get_chatbot_response(
        user_question,
        is_kannada
    )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    st.rerun()


# ============================================================
# CLEAR CHAT
# ============================================================

if len(
    st.session_state.messages
) > 0:

    if st.button(
        "🗑️ Clear Chat"
        if not is_kannada
        else
        "🗑️ ಚಾಟ್ ತೆರವುಗೊಳಿಸಿ"
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()


if is_kannada:

    st.warning(
        "⚠️ AI ಫಲಿತಾಂಶವು ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ಮಾತ್ರ. "
        "ಗಂಭೀರ ಸಮಸ್ಯೆಗಳಿದ್ದರೆ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
    )

else:

    st.warning(
        "⚠️ AI results are for preliminary guidance only. "
        "For serious problems, consult an agricultural expert."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🍄 Mushroom AI Assistant | "
    "AI Based Mushroom Disease Detection Using "
    "Image Processing & Deep Learning"
)
