"""Page 3: Dataset."""
import matplotlib.pyplot as plt
import streamlit as st

from utils import config, ui

# Class counts of the public APTOS 2019 training set (3,662 labelled images), as listed on Kaggle.
APTOS_CLASS_COUNTS = [1805, 370, 999, 193, 295]


def _bar_chart(labels, values, colors, title, ylabel):
    fig, ax = plt.subplots(figsize=(6, 3.4))
    bars = ax.bar(labels, values, color=colors, width=0.62)
    ax.set_title(title, fontsize=12, color="#0B2533", loc="left", pad=12)
    ax.set_ylabel(ylabel, color="#587280")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#D5E3E7")
    ax.spines["bottom"].set_color("#D5E3E7")
    ax.tick_params(colors="#587280", labelsize=9)
    ax.bar_label(bars, fmt="{:,.0f}", fontsize=9, color="#17323F", padding=3)
    ax.set_ylim(0, max(values) * 1.15)
    fig.tight_layout()
    return fig


def render() -> None:
    r = config.RECORDED
    ui.page_header("Dataset", "APTOS 2019 Blindness Detection: the images this model learned from.")

    st.markdown(
        "The **APTOS 2019 Blindness Detection** dataset was released for a Kaggle competition organised by the "
        "Asia Pacific Tele-Ophthalmology Society. It contains colour retinal fundus photographs taken with "
        "different cameras and in different conditions, so image quality varies. A clinician rated each image "
        "for diabetic retinopathy severity on a scale of 0 to 4. The dataset exists to help build automated "
        "screening tools that can flag DR early, especially where eye specialists are scarce."
    )

    c = st.columns(4, gap="medium")
    cards = [
        ("Total labelled images", f"{r['total_images']:,}", "", True),
        ("Training", f"{r['train_images']:,}", "images", False),
        ("Validation", f"{r['val_images']:,}", "images", False),
        ("Testing", f"{r['test_images']:,}", "images", False),
    ]
    for col, (lab, val, sub, acc) in zip(c, cards):
        with col:
            ui.html(ui.metric(lab, val, sub, accent=acc))

    st.markdown("## The five grades")
    rows = [
        (0, "No DR", "Healthy retina with no visible diabetic changes."),
        (1, "Mild DR", "Microaneurysms only."),
        (2, "Moderate DR", "More than microaneurysms but less than severe DR."),
        (3, "Severe DR", "Widespread bleeding and vessel abnormalities; high risk of progression."),
        (4, "Proliferative DR", "Abnormal new vessels (neovascularisation); the most advanced stage."),
    ]
    st.table({"Grade": [x[0] for x in rows], "Name": [x[1] for x in rows], "Meaning": [x[2] for x in rows]})

    st.markdown("## Charts")
    left, right = st.columns(2, gap="large")
    with left:
        fig = _bar_chart(
            ["Training", "Validation", "Testing"],
            [r["train_images"], r["val_images"], r["test_images"]],
            ["#0F7C86", "#5BA9B0", "#9CCBD0"],
            "How the 3,662 images were split",
            "Images",
        )
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    with right:
        fig = _bar_chart(
            [f"Grade {i}" for i in range(5)],
            APTOS_CLASS_COUNTS,
            ui.GRADE_COLORS,
            "Images per grade in APTOS 2019 (public listing)",
            "Images",
        )
        st.pyplot(fig, width="stretch")
        plt.close(fig)
    st.caption(
        "The split sizes are the project's recorded values. The per-grade counts come from the public APTOS "
        "2019 dataset description on Kaggle, not from this website. They show the dataset is heavily "
        "imbalanced: most images are Grade 0."
    )

    ui.notice(
        "info",
        "<b>The dataset is not needed to use this website.</b> Predictions come from the already-trained model "
        "file in the <b>models</b> folder; no dataset images are loaded or stored here.",
    )
