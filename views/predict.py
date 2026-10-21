"""Page 2: Predict."""
import hashlib

import streamlit as st

from utils import config, prediction, preprocessing, ui


def _missing_model_notice(detail: str) -> None:
    ui.notice(
        "err",
        "<b>The trained model could not be loaded.</b><br>"
        f"{ui.esc(detail).replace(chr(10), '<br>')}<br><br>"
        f"Expected location: <b>{ui.esc(config.MODEL_PATH)}</b>",
    )


def render(go) -> None:
    ui.page_header(
        "Predict DR grade",
        "Upload a retinal fundus photograph to see the grade predicted by the trained model.",
    )

    # ---- load the model once (cached for every later prediction)
    if not config.MODEL_PATH.is_file():
        _missing_model_notice("Model file not found.")
        st.markdown(
            "**Fix:** copy `diabetic_retinopathy_model.keras` into the `models` folder of this project, "
            "then refresh the page."
        )
        return
    try:
        with st.spinner("Loading the trained model (only the first time)…"):
            model = prediction.get_model()
    except prediction.ModelLoadError as exc:
        _missing_model_notice(str(exc))
        return

    ss = st.session_state
    ss.setdefault("uploader_key", 0)

    uploaded = st.file_uploader(
        "Retinal fundus image (JPG, JPEG or PNG)",
        type=config.ALLOWED_EXTENSIONS,
        key=f"uploader_{ss.uploader_key}",
        help=f"Maximum {config.MAX_UPLOAD_MB} MB.",
    )

    if uploaded is None:
        ss.pop("result", None)
        ui.html(
            '<div class="empty"><b>No image yet.</b><br>Drag a fundus photograph into the box above, '
            "or click Browse files.</div>"
        )
        return

    data = uploaded.getvalue()
    try:
        image = preprocessing.load_image(data)
    except preprocessing.InvalidImageError as exc:
        ui.notice("err", f"<b>This image can't be used.</b><br>{ui.esc(exc)}")
        return

    left, right = st.columns([1, 1], gap="large")

    with right:
        with st.expander("Advanced: preprocessing options"):
            st.caption(
                "Defaults match the saved model (it normalises pixels itself, so it expects 0–255 values). "
                "Change these only to check how sensitive the result is to preprocessing."
            )
            scaling = st.selectbox(
                "Pixel scaling", config.PIXEL_SCALING_OPTIONS,
                index=config.PIXEL_SCALING_OPTIONS.index(config.PIXEL_SCALING),
                format_func=lambda v: {"raw_0_255": "Raw 0–255 (default)", "zero_to_one": "Divide by 255"}[v],
            )
            backend = st.selectbox(
                "Resize method", config.RESIZE_BACKEND_OPTIONS,
                index=config.RESIZE_BACKEND_OPTIONS.index(config.RESIZE_BACKEND),
                format_func=lambda v: {"pillow": "Pillow bilinear (default)", "tensorflow": "TensorFlow bilinear"}[v],
            )
        clicked = st.button("Predict DR grade", type="primary", width="stretch")

    with left:
        st.image(image, caption=f"{uploaded.name} · {image.size[0]} × {image.size[1]} px", width="stretch")

    file_id = f"{hashlib.sha1(data).hexdigest()}|{scaling}|{backend}"

    if clicked:
        try:
            with right, st.spinner("Running the model…"):
                result = prediction.predict(model, image, scaling, backend)
            ss["result"] = {"id": file_id, "value": result}
        except (prediction.PredictionError, ValueError) as exc:
            ss.pop("result", None)
            with right:
                ui.notice("err", f"<b>Prediction failed.</b><br>{ui.esc(exc)}")
        except Exception as exc:  # noqa: BLE001 - never show a raw traceback to the user
            ss.pop("result", None)
            with right:
                ui.notice("err", f"<b>Unexpected error while predicting.</b><br>{ui.esc(type(exc).__name__)}: {ui.esc(exc)}")

    current = ss.get("result")
    if current and current["id"] == file_id:
        result = current["value"]
        with right:
            ui.result_card(result)
            ui.notice(
                "info",
                "The percentage is the <b>model's output score</b> (softmax output), not a medically "
                "confirmed probability.",
            )
            ranked = sorted(result.scores, reverse=True)
            if result.score < 0.5 or (ranked[0] - ranked[1]) < 0.15:
                ui.notice(
                    "warn",
                    "The model's scores are spread across several grades for this image, so the result is "
                    "uncertain. Treat it with extra caution.",
                )
            ui.notice(
                "warn",
                "The model has no “not a retina” option: it will assign a grade to <i>any</i> image. "
                "Only upload genuine fundus photographs. For education only; not a diagnosis.",
            )
            if st.button("Upload another image", width="stretch"):
                ss["uploader_key"] += 1
                ss.pop("result", None)
                st.rerun()
