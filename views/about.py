"""Page 5: About."""
import streamlit as st

from utils import config, ui


def render() -> None:
    ui.page_header("About this project", config.APP_TITLE)

    st.markdown("## Project overview")
    st.markdown(
        "This project grades diabetic retinopathy from retinal fundus photographs. A convolutional neural "
        "network (EfficientNetB0) was trained on the APTOS 2019 dataset, and this website lets anyone upload a "
        "photograph and see the model's predicted grade without retraining anything."
    )

    st.markdown("## Project members")
    cols = st.columns(len(config.STUDENTS), gap="medium")
    for col, s in zip(cols, config.STUDENTS):
        with col:
            ui.html(
                f'<div class="person"><div class="nm">{ui.esc(s["name"])}</div>'
                f'<div class="rl">Roll Number: {ui.esc(s["roll"])}</div></div>'
            )

    st.markdown("## Technologies used")
    tech = [
        ("Python", "Programming language for the whole project."),
        ("TensorFlow and Keras", "Load and run the trained deep-learning model."),
        ("Streamlit", "Builds this website interface."),
        ("Pillow and NumPy", "Read, convert and resize images into model input."),
        ("Matplotlib", "Draws the charts on the Dataset and Performance pages."),
        ("scikit-learn", "Evaluation metrics when labelled test data is available."),
    ]
    c1, c2 = st.columns(2, gap="medium")
    for i, (t, d) in enumerate(tech):
        with (c1 if i % 2 == 0 else c2):
            ui.html(f'<div class="card"><h4>{ui.esc(t)}</h4><p>{ui.esc(d)}</p></div>')
            st.write("")

    st.markdown("## How the model works")
    st.markdown(
        "The model uses **transfer learning**. EfficientNetB0, a network pre-trained on a large general image "
        "collection, extracts visual features from the photograph. A global average pooling layer summarises "
        "them, a dropout layer (rate 0.3) reduces overfitting, and a final dense layer with a softmax "
        "activation outputs five scores that add up to 1, one per DR grade. The grade with the highest score "
        "is reported as the prediction.\n\n"
        "Before an image reaches the network it is converted to RGB and resized to 224 × 224 pixels. "
        "EfficientNetB0 contains its own rescaling and normalisation layers, so raw 0–255 pixel values are supplied."
    )
    st.caption(
        "Architecture details above were read from the saved model file. The model was trained for "
        f"{config.RECORDED['epochs']} epochs with batch size {config.RECORDED['batch_size']}."
    )

    a, b = st.columns(2, gap="large")
    with a:
        st.markdown("## Advantages")
        st.markdown(
            "- Gives a result in seconds with no specialist equipment beyond the photograph.\n"
            "- Consistent: the same image always gives the same output.\n"
            "- Shows scores for all five grades, not just the top one.\n"
            "- Runs locally; uploaded images are not sent anywhere.\n"
            "- Transfer learning allowed training on a modest dataset."
        )
    with b:
        st.markdown("## Limitations")
        st.markdown(
            "- Recorded test accuracy is 74.55%, so roughly one in four test images was misgraded.\n"
            "- The dataset is imbalanced; rarer grades (1, 3, 4) are harder for the model.\n"
            "- Trained on one dataset; other cameras or populations may perform worse.\n"
            "- It cannot tell whether an image is a real fundus photograph.\n"
            "- Scores are model outputs, not calibrated medical probabilities."
        )

    st.markdown("## Future enhancements")
    st.markdown(
        "- Fine-tune more layers and compare other architectures.\n"
        "- Rebalance classes with augmentation or weighted loss.\n"
        "- Add heat-map explanations (Grad-CAM) showing which regions influenced the grade.\n"
        "- Check image quality and reject non-fundus images automatically.\n"
        "- Validate on additional datasets and with clinician review."
    )

    ui.notice(
        "warn",
        "<b>Medical disclaimer.</b> This is an academic project for education and demonstration. It is not a "
        "medical device, has not been clinically validated, and must not be used to diagnose, treat or make "
        "decisions about any health condition. Consult a qualified ophthalmologist for any eye concern.",
    )
