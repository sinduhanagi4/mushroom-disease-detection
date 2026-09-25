import streamlit as st

# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Mushroom AI Assistant",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CUSTOM DESIGN
# ---------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #dcfce7 0%, transparent 28%),
        radial-gradient(circle at 90% 20%, #d1fae5 0%, transparent 25%),
        linear-gradient(135deg, #f0fdf4 0%, #ffffff 45%, #ecfdf5 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #064e3b, #047857, #10b981);
    padding: 45px 40px;
    border-radius: 28px;
    color: white;
    box-shadow: 0 15px 40px rgba(5, 150, 105, 0.25);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
    opacity: 0.95;
    margin-bottom: 5px;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    padding: 8px 16px;
    border-radius: 30px;
    font-size: 14px;
    margin-bottom: 15px;
}

/* SECTION TITLE */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #064e3b;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* DASHBOARD CARDS */
.card {
    background: rgba(255,255,255,0.9);
    padding: 25px;
    border-radius: 22px;
    min-height: 175px;
    border: 1px solid #d1fae5;
    box-shadow: 0 8px 25px rgba(6, 78, 59, 0.08);
    transition: all 0.25s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(6, 78, 59, 0.15);
}

.card-icon {
    font-size: 38px;
    margin-bottom: 10px;
}

.card h3 {
    color: #065f46;
    margin-bottom: 8px;
}

.card p {
    color: #4b5563;
    font-size: 14px;
    line-height: 1.6;
}

/* DISEASE CARDS */
.disease {
    background: white;
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #d1fae5;
    box-shadow: 0 5px 18px rgba(0,0,0,0.05);
}

.disease-icon {
    font-size: 32px;
}

.disease h4 {
    color: #065f46;
    margin: 8px 0 3px 0;
}

.disease p {
    font-size: 12px;
    color: #6b7280;
}

/* HOW IT WORKS */
.step {
    background: linear-gradient(135deg, #ffffff, #f0fdf4);
    padding: 22px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #bbf7d0;
}

.step-number {
    background: #059669;
    color: white;
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 18px;
}

/* FARMER SECTION */
.farmer-box {
    background: linear-gradient(135deg, #14532d, #166534);
    color: white;
    padding: 30px;
    border-radius: 25px;
    margin-top: 25px;
    box-shadow: 0 12px 30px rgba(20,83,45,0.2);
}

.farmer-box h2 {
    color: white;
}

.farmer-box p {
    color: #dcfce7;
    line-height: 1.7;
}

/* LANGUAGE BUTTONS */
div[data-testid="stRadio"] > div {
    justify-content: center;
    gap: 12px;
}

div[data-testid="stRadio"] label {
    background: white;
    border: 2px solid #10b981;
    border-radius: 14px;
    padding: 10px 28px;
    font-weight: 700;
    color: #065f46;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #6b7280;
    padding: 30px 10px 10px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# TOP LANGUAGE SELECTOR
# ---------------------------------------------------------

st.markdown("""
<div style="
    background: linear-gradient(135deg, #064e3b, #059669);
    padding: 18px 25px;
    border-radius: 20px;
    margin-bottom: 15px;
    box-shadow: 0 8px 25px rgba(5,150,105,0.20);
    text-align: center;
">

<div style="
    color: white;
    font-size: 17px;
    font-weight: 700;
">
🌐 SELECT LANGUAGE / ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ
</div>

</div>
""", unsafe_allow_html=True)

language = st.radio(
    "Select Language",
    ["🇬🇧 English", "🇮🇳 ಕನ್ನಡ"],
    horizontal=True,
    label_visibility="collapsed"
)


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.markdown("""
<div class="hero">

<div class="badge">🌱 AI Powered Agriculture • Smart Farming</div>

<h1>🍄 Mushroom AI Assistant</h1>

<p><b>Smart Mushroom Disease Detection & Farmer Support</b></p>

<p>
Use Artificial Intelligence to identify common mushroom diseases
and receive simple, farmer-friendly guidance.
</p>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

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
        <p>
        Upload a mushroom image and our deep learning model
        analyzes it for possible diseases.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-icon">🌱</div>
        <h3>Farmer Guidance</h3>
        <p>
        Get easy-to-understand information and practical
        guidance related to mushroom health.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-icon">💬</div>
        <h3>AI Farmer Assistant</h3>
        <p>
        Ask questions about mushroom diseases, symptoms,
        prevention and cultivation.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-icon">📊</div>
        <h3>Disease Insights</h3>
        <p>
        Understand detected diseases through simple
        explanations and visual information.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# DETECTION HIGHLIGHT
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📸 Detect Mushroom Disease</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="farmer-box">

<h2>🔍 Start Your AI Diagnosis</h2>

<p>
Upload a clear photograph of your mushroom.
The AI system will analyze the image and provide
a predicted disease class with confidence.
</p>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SUPPORTED DISEASES
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🦠 Supported Mushroom Conditions</div>',
    unsafe_allow_html=True
)

d1, d2, d3, d4, d5 = st.columns(5)

diseases = [
    ("🍄", "Healthy", "No disease detected"),
    ("🟠", "Bacterial Blotch", "Bacterial infection"),
    ("🟤", "Dry Bubble", "Fungal disease"),
    ("⚪", "Cobweb", "Fungal infection"),
    ("🔵", "Wet Bubble", "Fungal disease")
]

for col, disease in zip([d1, d2, d3, d4, d5], diseases):

    with col:

        st.markdown(f"""
        <div class="disease">

            <div class="disease-icon">
                {disease[0]}
            </div>

            <h4>{disease[1]}</h4>

            <p>{disease[2]}</p>

        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">⚡ How It Works</div>',
    unsafe_allow_html=True
)

s1, s2, s3, s4 = st.columns(4)

steps = [
    ("1", "📷", "Upload Image"),
    ("2", "🤖", "AI Analysis"),
    ("3", "🔬", "Disease Result"),
    ("4", "🌱", "Farmer Guidance")
]

for col, step in zip([s1, s2, s3, s4], steps):

    with col:

        st.markdown(f"""
        <div class="step">

            <div class="step-number">
                {step[0]}
            </div>

            <div style="font-size:30px; margin:12px;">
                {step[1]}
            </div>

            <b>{step[2]}</b>

        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# FARMER BENEFITS
# ---------------------------------------------------------

st.markdown("""
<div class="farmer-box">

<h2>👨‍🌾 Built for Mushroom Farmers</h2>

<p>
Early identification of visible disease symptoms can help farmers
take timely action. This system provides an AI-based prediction
and easy-to-understand information in one place.
</p>

<p>
🌱 Simple interface &nbsp; • &nbsp;
📱 Mobile friendly &nbsp; • &nbsp;
🌐 English & Kannada &nbsp; • &nbsp;
🤖 AI powered
</p>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("""
<div class="footer">

🍄 <b>Mushroom AI Assistant</b><br>

AI-based mushroom disease detection and farmer support

<br><br>

⚠️ AI predictions are for informational purposes.
For important crop decisions, consult an agricultural expert.

</div>
""", unsafe_allow_html=True)
