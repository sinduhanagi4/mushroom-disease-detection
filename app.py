import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main background */
.stApp {
    background:
        linear-gradient(135deg, #f1f8e9 0%, #ffffff 45%, #e8f5e9 100%);
}

/* Header */
.hero {
    background: linear-gradient(135deg, #1b5e20, #43a047, #81c784);
    padding: 45px 30px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(46, 125, 50, 0.25);
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    margin: 5px;
}

/* Section title */
.section-title {
    color: #1b5e20;
    font-size: 28px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* Feature cards */
.card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    min-height: 170px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border: 1px solid #e8f5e9;
}

.card h3 {
    color: #2e7d32;
    margin-bottom: 10px;
}

.card p {
    color: #555;
    line-height: 1.6;
}

/* Footer */
.footer {
    margin-top: 40px;
    padding: 20px;
    text-align: center;
    color: #666;
    border-top: 1px solid #c8e6c9;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">

<h1>🍄 Mushroom AI Assistant</h1>

<p>Smart Mushroom Disease Detection</p>

<p>🌱 AI-powered support for mushroom farmers</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LANGUAGE
# --------------------------------------------------

language = st.radio(
    "🌐 Choose Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    ["English", "ಕನ್ನಡ"],
    horizontal=True
)

st.markdown("---")

# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if language == "English":

    st.markdown("""
    <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0 5px 18px rgba(0,0,0,0.06);
        text-align:center;
    ">

    <h2 style="color:#2e7d32;">🌱 Welcome, Farmer!</h2>

    <p style="font-size:17px;color:#555;">
    Upload a mushroom image to detect possible diseases
    and receive useful farming guidance.
    </p>

    </div>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div style="
        background:white;
        padding:25px;
        border-radius:20px;
        box-shadow:0 5px 18px rgba(0,0,0,0.06);
        text-align:center;
    ">

    <h2 style="color:#2e7d32;">🌱 ರೈತರಿಗೆ ಸ್ವಾಗತ!</h2>

    <p style="font-size:17px;color:#555;">
    ಅಣಬೆ ಚಿತ್ರದ ಮೂಲಕ ಸಂಭವನೀಯ ರೋಗವನ್ನು ಗುರುತಿಸಿ
    ಮತ್ತು ಉಪಯುಕ್ತ ಕೃಷಿ ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಿರಿ.
    </p>

    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FEATURE CARDS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">🌟 What You Can Do</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
    <h3>🔬 AI Detection</h3>
    <p>
    Upload a mushroom image and use our trained
    deep-learning model to identify the possible condition.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <h3>🌱 Farmer Guidance</h3>
    <p>
    Get simple information and practical guidance
    related to the detected mushroom condition.
    </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
    <h3>💬 AI Assistant</h3>
    <p>
    Ask questions about mushroom diseases,
    cultivation, prevention and basic care.
    </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">

🍄 <b>Mushroom AI Assistant</b>

<br>

AI-Based Mushroom Disease Detection Using Image Processing and Deep Learning

<br><br>

⚠️ AI predictions are for assistance and should be confirmed
with a qualified agricultural expert.

</div>
""", unsafe_allow_html=True)

