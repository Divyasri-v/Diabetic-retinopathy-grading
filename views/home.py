"""Page 1: Home."""
import streamlit as st

from utils import config, ui

GRADE_INFO = [
    ("No DR", "No visible signs of diabetic damage in the retina."),
    ("Mild", "Only microaneurysms: tiny swellings in the smallest blood vessels."),
    ("Moderate", "More than microaneurysms, such as small bleeds or fluid deposits, but not yet severe."),
    ("Severe", "Many bleeds and vessel changes across the retina; high risk of progressing."),
    ("Proliferative", "New, fragile blood vessels grow; risk of serious bleeding and vision loss."),
]


def render(go) -> None:
    ui.html(
        f"""
        <div class="hero">
        <div class="copy">
        <h1>{ui.esc(config.APP_TITLE)}</h1>
        <p>Upload a retinal fundus photograph and a trained EfficientNetB0 network assigns it one of
        five severity grades, from No DR to Proliferative DR.</p>
        <div class="chips"><span class="chip">APTOS 2019 dataset</span>
        <span class="chip">EfficientNetB0</span><span class="chip">224 × 224 input</span>
        <span class="chip">5 severity grades</span></div>
        </div>
        <div class="art">{ui.retina_svg()}</div>
        </div>
        """
    )
    st.write("")
    st.button("Go to prediction", type="primary", on_click=go, args=("Predict",), key="home_cta")

    st.markdown("## What is diabetic retinopathy?")
    st.markdown(
        "Diabetic retinopathy (DR) is a complication of diabetes. Persistently high blood sugar "
        "damages the tiny blood vessels in the retina, the light-sensitive layer at the back of the eye. "
        "Early stages usually cause no symptoms, which is why regular retinal screening matters. "
        "Without treatment, DR can lead to permanent vision loss."
    )
    st.markdown("Doctors grade DR on a five-step scale. This project predicts the same five grades:")
    steps = "".join(
        f'<div class="step" style="--c:{ui.GRADE_COLORS[i]}"><div class="g">{i}</div>'
        f'<div class="n">{ui.esc(n)}</div><div class="d">{ui.esc(d)}</div></div>'
        for i, (n, d) in enumerate(GRADE_INFO)
    )
    ui.html(f'<div class="scale">{steps}</div>')

    st.markdown("## Project objectives")
    c1, c2 = st.columns(2, gap="medium")
    objectives = [
        ("Grade DR automatically", "Classify fundus photographs into five severity grades using transfer learning."),
        ("Make it usable", "Wrap the trained model in a simple website where anyone can upload an image and see the result."),
        ("Report results honestly", "Show the recorded test accuracy (74.55%) alongside the model's limitations."),
        ("Support, not replace, screening", "Show how deep learning could help prioritise images for clinician review."),
    ]
    for i, (t, d) in enumerate(objectives):
        with (c1 if i % 2 == 0 else c2):
            ui.html(f'<div class="card"><h4>{ui.esc(t)}</h4><p>{ui.esc(d)}</p></div>')
            st.write("")

    st.markdown("## How a prediction works")
    c = st.columns(4, gap="medium")
    flow = [
        ("1. Upload", "Choose a JPG or PNG fundus photograph."),
        ("2. Prepare", "The image is converted to RGB and resized to 224 × 224 pixels."),
        ("3. Predict", "The trained EfficientNetB0 model outputs five scores."),
        ("4. Review", "The highest score gives the predicted grade; all five scores are shown."),
    ]
    for col, (t, d) in zip(c, flow):
        with col:
            ui.html(f'<div class="card"><h4>{ui.esc(t)}</h4><p>{ui.esc(d)}</p></div>')

    ui.notice(
        "warn",
        "<b>Educational project.</b> This tool is not a medical device and must not be used to diagnose "
        "or treat any condition. Always consult a qualified eye-care professional.",
    )
