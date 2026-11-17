
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from io import BytesIO

try:
    from streamlit_mic_recorder import speech_to_text
except ImportError:
    speech_to_text = None

try:
    from gtts import gTTS
except ImportError:
    gTTS = None


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# PAGE DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #f0fdf4;
}
.main-title {
    color: #065f46;
    text-align: center;
    font-size: 38px;
    font-weight: 800;
}
.sub-title {
    color: #047857;
    text-align: center;
    font-size: 21px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# LANGUAGE SELECTION
language = st.radio(
    "🌐 Select Language / ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ",
    ["🇬🇧 English", "🇮🇳 ಕನ್ನಡ"],
    horizontal=True
)

is_kannada = language == "🇮🇳 ಕನ್ನಡ"

if is_kannada:
    title = "🍄 ಮಶ್ರೂಮ್ AI ಸಹಾಯಕ"
    subtitle = "ಸ್ಮಾರ್ಟ್ ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ ಮತ್ತು ರೈತ ಸಹಾಯ"
    description = "ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ರೈತ ಸ್ನೇಹಿ ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಿರಿ."
else:
    title = "🍄 Mushroom AI Assistant"
    subtitle = "Smart Mushroom Disease Detection & Farmer Support"
    description = "Upload a mushroom image and receive farmer-friendly disease guidance."


# HERO SECTION
st.success(
    "🌱 AI ಆಧಾರಿತ ಕೃಷಿ • ಸ್ಮಾರ್ಟ್ ಫಾರ್ಮಿಂಗ್"
    if is_kannada else
    "🌱 AI Powered Agriculture • Smart Farming"
)

st.markdown(
    f'<div class="main-title">{title}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="sub-title">{subtitle}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align:center'>{description}</p>",
    unsafe_allow_html=True
)

st.divider()


# DASHBOARD
st.markdown(
    "## 🌿 ಸ್ಮಾರ್ಟ್ ಫಾರ್ಮಿಂಗ್ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್"
    if is_kannada else
    "## 🌿 Smart Farming Dashboard"
)

st.write(
    "ಮಶ್ರೂಮ್ ಕೃಷಿಗೆ ಅಗತ್ಯವಾದ ಸಹಾಯವನ್ನು ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ ಪಡೆಯಿರಿ."
    if is_kannada else
    "Get smart support for mushroom farming in one place."
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info(
        "### 🔬 AI ರೋಗ ಪತ್ತೆ\n\nಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
        if is_kannada else
        "### 🔬 AI Disease Detection\n\nUpload a mushroom image."
    )

with c2:
    st.success(
        "### 🌱 ರೈತ ಮಾರ್ಗದರ್ಶನ\n\nಉಪಯುಕ್ತ ಸಲಹೆಗಳನ್ನು ಪಡೆಯಿರಿ."
        if is_kannada else
        "### 🌱 Farmer Guidance\n\nGet useful recommendations."
    )

with c3:
    st.warning(
        "### 💬 ರೈತ ಸಹಾಯಕ\n\nನಿಮ್ಮ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ."
        if is_kannada else
        "### 💬 Farmer Assistant\n\nAsk your questions."
    )

with c4:
    st.error(
        "### 🦠 ರೋಗ ಮಾಹಿತಿ\n\nಐದು ವರ್ಗಗಳ ಮಾಹಿತಿ."
        if is_kannada else
        "### 🦠 Disease Information\n\nInformation about five classes."
    )

st.divider()


# DISEASE CLASSES
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


# FARMER ADVICE
advice = {
    "Healthy": {
        "en": "The mushroom appears healthy. Maintain hygiene, suitable moisture and proper ventilation.",
        "kn": "ಮಶ್ರೂಮ್ ಆರೋಗ್ಯಕರವಾಗಿ ಕಾಣುತ್ತದೆ. ಸ್ವಚ್ಛತೆ, ಸೂಕ್ತ ತೇವಾಂಶ ಮತ್ತು ಗಾಳಿಯ ಹರಿವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."
    },
    "Bacterial Blotch": {
        "en": "Maintain hygiene, avoid excess surface moisture and improve ventilation.",
        "kn": "ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ, ಹೆಚ್ಚುವರಿ ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ ಮತ್ತು ಗಾಳಿಯ ಹರಿವನ್ನು ಸುಧಾರಿಸಿ."
    },
    "Dry Bubble": {
        "en": "Remove infected mushrooms carefully and maintain growing-room hygiene.",
        "kn": "ಸೋಂಕಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಕೊಠಡಿಯನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ."
    },
    "Cobweb": {
        "en": "Remove affected areas, maintain cleanliness and avoid excessive humidity.",
        "kn": "ಬಾಧಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ, ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ ಮತ್ತು ಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."
    },
    "Wet Bubble": {
        "en": "Remove infected material carefully and maintain hygiene and moisture control.",
        "kn": "ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ ಮತ್ತು ತೇವಾಂಶವನ್ನು ನಿಯಂತ್ರಿಸಿ."
    }
}


# LOAD MODEL WHEN NEEDED
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "mushroom_disease_mobilenetv2.keras"
    )


# DISEASE DETECTION
st.divider()

st.markdown(
    "## 🔬 ಮಶ್ರೂಮ್ ರೋಗ ಪತ್ತೆ"
    if is_kannada else
    "## 🔬 Mushroom Disease Detection"
)

st.write(
    "ಸ್ಪಷ್ಟವಾದ ಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
    if is_kannada else
    "Upload a clear mushroom image for disease detection."
)

upload_col, help_col = st.columns(2)

with upload_col:
    uploaded_file = st.file_uploader(
        "ಚಿತ್ರವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ / Choose an image",
        type=["jpg", "jpeg", "png"]
    )

with help_col:
    st.info(
        "ಉತ್ತಮ ಬೆಳಕು ಬಳಸಿ. ಮಶ್ರೂಮ್ ಸ್ಪಷ್ಟವಾಗಿ ಕಾಣಲಿ."
        if is_kannada else
        "Use good lighting and keep the mushroom clearly visible."
    )

if uploaded_file is not None:

    try:
        image = Image.open(uploaded_file).convert("RGB")

        image_col, result_col = st.columns(2)

        with image_col:
            st.subheader(
                "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ"
                if is_kannada else
                "Uploaded Image"
            )
            st.image(image, use_container_width=True)

        with st.spinner(
            "ಮಾದರಿ ಲೋಡ್ ಆಗುತ್ತಿದೆ..."
            if is_kannada else
            "Loading model and analyzing image..."
        ):

            model = load_model()

            resized_image = image.resize((224, 224))

            image_array = np.asarray(
                resized_image,
                dtype=np.float32
            ) / 255.0

            image_array = np.expand_dims(
                image_array,
                axis=0
            )

            prediction = model.predict(
                image_array,
                verbose=0
            )

        predicted_index = int(
            np.argmax(prediction[0])
        )

        predicted_class = class_names[predicted_index]

        confidence = float(
            prediction[0][predicted_index]
        ) * 100

        display_name = (
            kannada_names[predicted_class]
            if is_kannada
            else predicted_class
        )

        with result_col:

            st.subheader(
                "ಪತ್ತೆಯಾದ ಫಲಿತಾಂಶ"
                if is_kannada else
                "Detection Result"
            )

            if predicted_class == "Healthy":
                st.success(f"🟢 {display_name}")
            else:
                st.error(f"🔴 {display_name}")

            st.write(
                "ವಿಶ್ವಾಸ ಮಟ್ಟ"
                if is_kannada else
                "Prediction Confidence"
            )

            st.progress(
                min(max(confidence / 100, 0.0), 1.0)
            )

            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

        advice_text = advice[predicted_class][
            "kn" if is_kannada else "en"
        ]

        st.info(
            f"🌱 **ರೈತರಿಗೆ ಸಲಹೆ**\n\n{advice_text}"
            if is_kannada else
            f"🌱 **Farmer Advice**\n\n{advice_text}"
        )

    except Exception as error:
        st.error(
            "ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ."
            if is_kannada else
            "Image analysis failed."
        )
        st.exception(error)


# GENERAL FARMER GUIDANCE
st.divider()

st.markdown(
    "## 🌱 ರೈತರಿಗೆ ಉಪಯುಕ್ತ ಸಲಹೆಗಳು"
    if is_kannada else
    "## 🌱 Useful Farmer Advice"
)

a1, a2 = st.columns(2)

with a1:
    st.info(
        "### 🧼 ಸ್ವಚ್ಛತೆ\n\nಬೆಳೆಯುವ ಕೊಠಡಿ ಮತ್ತು ಉಪಕರಣಗಳನ್ನು ಸ್ವಚ್ಛವಾಗಿಡಿ."
        if is_kannada else
        "### 🧼 Hygiene\n\nKeep the growing room and tools clean."
    )

    st.success(
        "### 🌬️ ಗಾಳಿಯ ಹರಿವು\n\nಉತ್ತಮ ಗಾಳಿಯ ಸಂಚಾರ ಇರಲಿ."
        if is_kannada else
        "### 🌬️ Ventilation\n\nMaintain good air circulation."
    )

with a2:
    st.warning(
        "### 💧 ತೇವಾಂಶ ನಿಯಂತ್ರಣ\n\nಅತಿಯಾದ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."
        if is_kannada else
        "### 💧 Moisture Control\n\nAvoid excessive surface moisture."
    )

    st.info(
        "### 👀 ಪರಿಶೀಲನೆ\n\nಮಶ್ರೂಮ್‌ಗಳನ್ನು ನಿಯಮಿತವಾಗಿ ಪರಿಶೀಲಿಸಿ."
        if is_kannada else
        "### 👀 Regular Inspection\n\nInspect mushrooms regularly."
    )


# SUPPORTED DISEASES
st.divider()

st.markdown(
    "## 🦠 ಪತ್ತೆಹಚ್ಚಬಹುದಾದ ರೋಗಗಳು"
    if is_kannada else
    "## 🦠 Supported Diseases"
)

icons = ["🍄", "🦠", "⚪", "🕸️", "💧"]

disease_columns = st.columns(5)

for column, disease, icon in zip(
    disease_columns,
    class_names,
    icons
):
    with column:
        name = (
            kannada_names[disease]
            if is_kannada
            else disease
        )
        st.info(f"{icon} **{name}**")


# HOW IT WORKS
st.divider()

st.markdown(
    "## ⚙️ ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?"
    if is_kannada else
    "## ⚙️ How It Works"
)

h1, h2, h3 = st.columns(3)

with h1:
    st.info(
        "### 1️⃣ ಚಿತ್ರ ಅಪ್‌ಲೋಡ್\n\nಮಶ್ರೂಮ್ ಚಿತ್ರವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ."
        if is_kannada else
        "### 1️⃣ Upload Image\n\nChoose a mushroom photo."
    )

with h2:
    st.warning(
        "### 2️⃣ AI ವಿಶ್ಲೇಷಣೆ\n\nMobileNetV2 ಚಿತ್ರವನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತದೆ."
        if is_kannada else
        "### 2️⃣ AI Analysis\n\nMobileNetV2 analyzes the image."
    )

with h3:
    st.success(
        "### 3️⃣ ರೈತ ಮಾರ್ಗದರ್ಶನ\n\nಫಲಿತಾಂಶ ಮತ್ತು ಸಲಹೆ ಪಡೆಯಿರಿ."
        if is_kannada else
        "### 3️⃣ Farmer Guidance\n\nView the result and advice."
    )


# CHATBOT FUNCTION
def get_chatbot_response(question, kannada):

    q = question.lower()

    if kannada:

        if "ಬ್ಯಾಕ್ಟೀರಿಯಲ್" in q or "blotch" in q:
            return "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್: ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ ಮತ್ತು ಹೆಚ್ಚುವರಿ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."

        if "ಡ್ರೈ ಬಬಲ್" in q or "dry bubble" in q:
            return "ಡ್ರೈ ಬಬಲ್: ಸೋಂಕಿತ ಮಶ್ರೂಮ್‌ಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ತೆಗೆದುಹಾಕಿ."

        if "ಕಾಬ್" in q or "cobweb" in q:
            return "ಕಾಬ್‌ವೆಬ್: ಬಾಧಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ ಮತ್ತು ಸ್ವಚ್ಛತೆಯನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."

        if "ವೆಟ್ ಬಬಲ್" in q or "wet bubble" in q:
            return "ವೆಟ್ ಬಬಲ್: ಸೋಂಕಿತ ವಸ್ತುಗಳನ್ನು ತೆಗೆದುಹಾಕಿ ಮತ್ತು ತೇವಾಂಶವನ್ನು ನಿಯಂತ್ರಿಸಿ."

        if "ತಡೆ" in q or "prevent" in q:
            return "ರೋಗ ತಡೆಗಟ್ಟಲು ಸ್ವಚ್ಛತೆ, ಗಾಳಿಯ ಹರಿವು ಮತ್ತು ಸೂಕ್ತ ತೇವಾಂಶವನ್ನು ಕಾಪಾಡಿಕೊಳ್ಳಿ."

        if "ತೇವಾಂಶ" in q or "moisture" in q:
            return "ಅತಿಯಾದ ಮೇಲ್ಮೈ ತೇವಾಂಶವನ್ನು ತಪ್ಪಿಸಿ."

        if "ಗಾಳಿ" in q or "ventilation" in q:
            return "ಉತ್ತಮ ಗಾಳಿಯ ಹರಿವು ಬೆಳೆಯುವ ಪರಿಸರಕ್ಕೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ."

        return "ದಯವಿಟ್ಟು ಮಶ್ರೂಮ್ ರೋಗಗಳು, ಸ್ವಚ್ಛತೆ, ತೇವಾಂಶ ಅಥವಾ ಗಾಳಿಯ ಹರಿವಿನ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ."

    else:

        if "bacterial" in q or "blotch" in q:
            return "Bacterial Blotch: Maintain hygiene and avoid excess surface moisture."

        if "dry bubble" in q:
            return "Dry Bubble: Carefully remove affected mushrooms and maintain cleanliness."

        if "cobweb" in q:
            return "Cobweb: Remove affected areas and avoid excessive humidity."

        if "wet bubble" in q:
            return "Wet Bubble: Remove infected material carefully and maintain hygiene."

        if "prevent" in q:
            return "Disease prevention: Maintain hygiene, suitable moisture and good ventilation."

        if "hygiene" in q or "clean" in q:
            return "Keep the growing room and tools clean."

        if "moisture" in q:
            return "Avoid excessive surface moisture."

        if "ventilation" in q or "air" in q:
            return "Good air circulation helps maintain a suitable growing environment."

        return "Ask me about mushroom diseases, hygiene, moisture, ventilation or disease prevention."


# FARMER ASSISTANT
st.divider()

st.markdown(
    "## 💬 AI ರೈತ ಸಹಾಯಕ"
    if is_kannada else
    "## 💬 AI Farmer Assistant"
)

st.write(
    "ಮಶ್ರೂಮ್ ರೋಗಗಳ ಬಗ್ಗೆ ನಿಮ್ಮ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ."
    if is_kannada else
    "Ask questions about mushroom diseases and prevention."
)

if "messages" not in st.session_state:
    st.session_state.messages = []


# VOICE ASSISTANT
st.markdown(
    "### 🎙️ ಧ್ವನಿ ರೈತ ಸಹಾಯಕ"
    if is_kannada else
    "### 🎙️ Voice Farmer Assistant"
)

voice_question = None

if speech_to_text is not None:

    voice_question = speech_to_text(
        language="kn-IN" if is_kannada else "en-US",
        start_prompt="🎙️ ಪ್ರಶ್ನೆ ಕೇಳಿ" if is_kannada else "🎙️ Ask by Voice",
        stop_prompt="⏹️ ನಿಲ್ಲಿಸಿ" if is_kannada else "⏹️ Stop",
        just_once=True,
        use_container_width=True,
        key="voice_kn" if is_kannada else "voice_en"
    )

else:
    st.caption(
        "Voice input is unavailable. Check requirements.txt."
    )


# QUICK QUESTIONS
quick_questions = (
    [
        "ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲಾಚ್ ಎಂದರೇನು?",
        "ಡ್ರೈ ಬಬಲ್ ಬಗ್ಗೆ ತಿಳಿಸಿ",
        "ಕಾಬ್‌ವೆಬ್ ಬಗ್ಗೆ ತಿಳಿಸಿ",
        "ವೆಟ್ ಬಬಲ್ ಬಗ್ಗೆ ತಿಳಿಸಿ",
        "ರೋಗಗಳನ್ನು ಹೇಗೆ ತಡೆಯುವುದು?"
    ]
    if is_kannada else
    [
        "What is Bacterial Blotch?",
        "Tell me about Dry Bubble",
        "Tell me about Cobweb",
        "Tell me about Wet Bubble",
        "How can I prevent diseases?"
    ]
)

st.markdown(
    "### ⚡ ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು"
    if is_kannada else
    "### ⚡ Quick Questions"
)

quick_columns = st.columns(3)
selected_question = None

for index, question in enumerate(quick_questions):

    with quick_columns[index % 3]:

        if st.button(
            question,
            use_container_width=True,
            key=f"quick_{index}"
        ):
            selected_question = question


# CHAT HISTORY
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


typed_question = st.chat_input(
    "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ..."
    if is_kannada else
    "Ask your question..."
)

user_question = (
    typed_question
    or selected_question
    or voice_question
)

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

    # VOICE RESPONSE
    if (
        voice_question
        and user_question == voice_question
        and gTTS is not None
    ):

        try:
            audio_buffer = BytesIO()

            gTTS(
                text=response,
                lang="kn" if is_kannada else "en"
            ).write_to_fp(audio_buffer)

            st.audio(
                audio_buffer.getvalue(),
                format="audio/mp3"
            )

        except Exception:
            st.info("Text response is available.")

    st.rerun()


# CLEAR CHAT
if st.session_state.messages:

    if st.button(
        "🗑️ ಚಾಟ್ ತೆರವುಗೊಳಿಸಿ"
        if is_kannada else
        "🗑️ Clear Chat"
    ):

        st.session_state.messages = []
        st.rerun()


# DISCLAIMER
st.divider()

st.warning(
    "AI ಫಲಿತಾಂಶವು ಪ್ರಾಥಮಿಕ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ಮಾತ್ರ. ಗಂಭೀರ ಸಮಸ್ಯೆಗಳಿದ್ದರೆ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ."
    if is_kannada else
    "AI results are for preliminary guidance only. For serious problems, consult an agricultural expert."
)

st.divider()

st.caption(
    "🍄 Mushroom AI Assistant | AI Based Mushroom Disease Detection Using Image Processing & Deep Learning"
)
