"""Diabetic Retinopathy Grading Using Deep Learning: Streamlit entry point.

Run with:  streamlit run app.py
"""
import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")  # quieter TensorFlow console

import streamlit as st

from utils import config, ui
from views import about, dataset, home, performance, predict

st.set_page_config(
    page_title="DR Grading Using Deep Learning",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)
ui.inject_css()

PAGES = {
    "Home": lambda: home.render(go),
    "Predict": lambda: predict.render(go),
    "Dataset": dataset.render,
    "Model performance": performance.render,
    "About": about.render,
}


def go(page: str) -> None:
    """Button callback: switch page."""
    st.session_state["page"] = page


st.session_state.setdefault("page", "Home")

with st.sidebar:
    ui.html(
        f'<div class="brand">{ui.logo_mark()}<div class="t">DR Grading<br>Using Deep Learning</div></div>'
    )
    for name in PAGES:
        st.button(
            name,
            key=f"nav_{name}",
            width="stretch",
            type="primary" if st.session_state["page"] == name else "secondary",
            on_click=go,
            args=(name,),
        )

    found = config.MODEL_PATH.is_file()
    color = "#5FD3A1" if found else "#FF8A80"
    text = "Model file found" if found else "Model file missing"
    ui.html(
        f'<div class="side-note"><span class="status"><span class="dot" style="background:{color}"></span>{text}</span></div>'
    )
    members = "<br>".join(f"<b>{ui.esc(s['name'])}</b><br>Roll No. {ui.esc(s['roll'])}" for s in config.STUDENTS)
    ui.html(f'<div class="side-note">{members}</div>')
    ui.html('<div class="side-note">For education only. Not a medical device.</div>')

PAGES[st.session_state["page"]]()
