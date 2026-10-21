"""Page 4: Model performance."""
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from utils import config, evaluation, ui


def _confusion_figure(cm: np.ndarray):
    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    ax.imshow(cm, cmap="GnBu")
    labels = [f"{i}" for i in range(config.NUM_CLASSES)]
    ax.set_xticks(range(5), labels)
    ax.set_yticks(range(5), labels)
    ax.set_xlabel("Predicted grade")
    ax.set_ylabel("True grade")
    ax.set_title("Confusion matrix (counts)", loc="left", color="#0B2533")
    thresh = cm.max() / 2 if cm.max() else 0
    for i in range(5):
        for j in range(5):
            ax.text(j, i, int(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "#17323F", fontsize=11)
    fig.tight_layout()
    return fig


def render() -> None:
    r = config.RECORDED
    ui.page_header("Model performance", "Results recorded when the model was trained and tested.")

    c = st.columns(4, gap="medium")
    with c[0]:
        ui.html(ui.metric("Test accuracy", f"{r['test_accuracy_pct']:.2f}%", f"on {r['test_images']} test images", accent=True))
    with c[1]:
        ui.html(ui.metric("Test loss", f"≈ {r['test_loss']:.3f}", "sparse categorical cross-entropy"))
    with c[2]:
        ui.html(ui.metric("Training epochs", str(r["epochs"]), f"batch size {r['batch_size']}"))
    with c[3]:
        ui.html(ui.metric("Input size", "224 × 224", "RGB pixels"))

    ui.notice(
        "info",
        "These figures are <b>previously recorded project results</b>. This website did not recalculate them. "
        "Accuracy of 74.55% means roughly three in four test images received the correct grade; "
        "performance on new images from other cameras or hospitals may be lower.",
    )

    st.markdown("## Confusion matrix and classification report")
    try:
        cm = evaluation.load_confusion_matrix()
    except (ValueError, OSError) as exc:
        cm = None
        ui.notice("err", f"<b>Could not read the evaluation results.</b><br>{ui.esc(exc)}")

    if cm is None:
        ui.notice(
            "warn",
            "<b>No evaluation results are available yet.</b> A confusion matrix and classification report can "
            "only be shown from real predictions on labelled test images, and none are stored with this project. "
            "To generate them, run <code>python scripts/evaluate_model.py</code> with your test images "
            "(see the README, section “Optional: generate the confusion matrix”). They will then appear here automatically.",
        )
        return

    m = evaluation.metrics_from_confusion(cm)
    left, right = st.columns([1, 1.1], gap="large")
    with left:
        fig = _confusion_figure(cm)
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    with right:
        st.markdown("**Per-grade results**")
        st.dataframe(
            {
                "Grade": [f"{i} — {config.CLASS_NAMES[i]}" for i in range(5)],
                "Precision": np.round(m["precision"], 3),
                "Recall": np.round(m["recall"], 3),
                "F1-score": np.round(m["f1"], 3),
                "Images": m["support"],
            },
            hide_index=True,
            width="stretch",
        )
        st.caption(
            f"Computed from the saved confusion matrix: {int(cm.sum())} images, "
            f"accuracy {m['accuracy'] * 100:.2f}%, macro F1 {m['macro_f1']:.3f}."
        )
    measured = evaluation.load_metrics_json()
    if measured:
        st.caption(f"Re-measured by scripts/evaluate_model.py: {measured}")
    report = evaluation.load_report_text()
    if report:
        with st.expander("Full classification report (text)"):
            st.code(report)
