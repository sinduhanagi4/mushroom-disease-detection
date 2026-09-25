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

        html = f'''
<div class="disease">
    <div class="disease-icon">{disease[0]}</div>
    <h4>{disease[1]}</h4>
    <p>{disease[2]}</p>
</div>
'''

        st.markdown(html, unsafe_allow_html=True)


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

        html = f'''
<div class="step">
    <div class="step-number">{step[0]}</div>
    <div style="font-size:30px; margin:12px;">{step[1]}</div>
    <b>{step[2]}</b>
</div>
'''

        st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# FARMER BENEFITS
# ---------------------------------------------------------
