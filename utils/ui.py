"""Styling and small HTML building blocks shared by all pages."""
from __future__ import annotations

import html as _html

import streamlit as st

from . import config

# One colour per grade: calm teal-green for "no DR" through to deep red for "proliferative".
GRADE_COLORS = ["#2E8B6E", "#8DB255", "#E0A82E", "#E07B39", "#C8433B"]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=DM+Sans:wght@400;500;600&display=swap');

:root{
  --ink:#0B2533; --deep:#123C4F; --teal:#0F7C86; --teal-soft:#DCEFF1;
  --bg:#F3F8F9; --card:#FFFFFF; --line:#D5E3E7; --text:#17323F; --muted:#587280;
}
html, body, .stApp { font-family:'DM Sans','Segoe UI',system-ui,sans-serif; color:var(--text); }
.stApp { background:var(--bg); }
.block-container { max-width:1160px; padding-top:4rem !important; padding-bottom:4rem; }
#MainMenu, footer { visibility:hidden; }

h1,h2,h3 { font-family:'Fraunces',Georgia,serif !important; color:var(--ink); letter-spacing:-0.01em; }
h2 { font-size:1.55rem !important; margin-top:1.6rem !important; }
h3 { font-size:1.2rem !important; }
p, li { line-height:1.65; }
.stMarkdown p, .stMarkdown li { max-width:74ch; }

/* ---------- sidebar */
section[data-testid="stSidebar"] { background:var(--ink); border-right:0; }
section[data-testid="stSidebar"] * { color:#D3E6EA; }
section[data-testid="stSidebar"] .stButton > button {
  width:100%; justify-content:flex-start; text-align:left; border:0; border-radius:10px;
  background:transparent; padding:.6rem .9rem; font-weight:500; box-shadow:none;
}
section[data-testid="stSidebar"] .stButton > button > div,
section[data-testid="stSidebar"] .stButton > button p { justify-content:flex-start !important; text-align:left !important; width:100%; }
section[data-testid="stSidebar"] .stButton > button:hover { background:rgba(255,255,255,.08); }
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
  background:var(--teal); color:#fff; }
section[data-testid="stSidebar"] .stButton > button[kind="primary"] * { color:#fff; }
.brand { display:flex; gap:.7rem; align-items:center; padding:.4rem .4rem 1.2rem; }
.brand .mark { width:38px; height:38px; flex:none; }
.brand .t { font-family:'Fraunces',Georgia,serif; font-size:1.05rem; line-height:1.2; color:#fff; }
.side-note { font-size:.82rem; line-height:1.5; padding:.9rem .4rem 0; color:#9FBAC2 !important; }
.side-note b { color:#fff; font-weight:600; }
.status { display:inline-flex; align-items:center; gap:.45rem; font-size:.82rem; padding:.25rem .7rem;
  border-radius:999px; background:rgba(255,255,255,.08); }
.dot { width:8px; height:8px; border-radius:50%; display:inline-block; }

/* ---------- hero */
.hero { background:linear-gradient(135deg,#0B2533 0%,#123C4F 100%); border-radius:24px;
  padding:2.6rem 2.8rem; display:flex; gap:2rem; align-items:center; }
.hero .copy { flex:1 1 55%; }
.hero h1 { color:#fff; font-size:2.6rem; line-height:1.12; margin:0 0 1rem; font-weight:600; }
.hero p { color:#BCD6DC; font-size:1.05rem; margin:0; max-width:52ch; }
.hero .chips { margin-top:1.4rem; display:flex; gap:.5rem; flex-wrap:wrap; }
.chip { font-size:.82rem; padding:.3rem .8rem; border-radius:999px; background:rgba(255,255,255,.1); color:#E4F1F3; }
.hero .art { flex:0 0 300px; }
.hero .art svg { width:100%; height:auto; display:block; }

/* ---------- page header */
.page-head { margin-bottom:1.4rem; }
.page-head h1 { font-size:2.1rem; margin:0 0 .35rem; font-weight:600; }
.page-head p { color:var(--muted); margin:0; font-size:1.05rem; }

/* ---------- cards */
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:1.2rem 1.35rem; height:100%; }
.card h4 { margin:0 0 .35rem; font-size:1.02rem; color:var(--ink); }
.card p { margin:0; color:var(--muted); font-size:.95rem; }
.metric { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:1.1rem 1.3rem; }
.metric .lab { color:var(--muted); font-size:.9rem; }
.metric .val { font-family:'Fraunces',Georgia,serif; font-size:2.2rem; color:var(--ink); line-height:1.15; font-weight:600; }
.metric .sub { color:var(--muted); font-size:.85rem; margin-top:.15rem; }
.metric.accent { background:var(--teal); border-color:var(--teal); }
.metric.accent .lab, .metric.accent .sub { color:#CDEBEE; }
.metric.accent .val { color:#fff; }

/* ---------- severity scale */
.scale { display:grid; grid-template-columns:repeat(5,1fr); gap:.6rem; }
.scale .step { background:var(--card); border:1px solid var(--line); border-top:6px solid var(--c); border-radius:10px; padding:.9rem 1rem 1rem; }
.scale .g { font-family:'Fraunces',Georgia,serif; font-size:1.7rem; color:var(--c); line-height:1; font-weight:600; }
.scale .n { font-weight:600; color:var(--ink); margin:.35rem 0 .3rem; }
.scale .d { font-size:.88rem; color:var(--muted); line-height:1.5; }

/* ---------- result */
.result { background:var(--card); border:1px solid var(--line); border-left:10px solid var(--c); border-radius:14px; padding:1.4rem 1.6rem; }
.result .kicker { color:var(--muted); font-size:.9rem; }
.result .grade { font-family:'Fraunces',Georgia,serif; font-size:2.1rem; color:var(--ink); font-weight:600; line-height:1.15; margin:.15rem 0 .6rem; }
.result .score { display:flex; align-items:baseline; gap:.6rem; }
.result .score b { font-family:'Fraunces',Georgia,serif; font-size:2.4rem; color:var(--c); font-weight:600; }
.result .score span { color:var(--muted); font-size:.92rem; }
.bars { margin-top:1.1rem; }
.bar-row { display:grid; grid-template-columns:11.5rem 1fr 4.2rem; gap:.8rem; align-items:center; margin:.5rem 0; font-size:.93rem; }
.bar-row .track { background:#E8F0F2; border-radius:999px; height:12px; overflow:hidden; }
.bar-row .fill { height:100%; border-radius:999px; background:var(--c); }
.bar-row.top .name { font-weight:600; color:var(--ink); }
.bar-row .pct { text-align:right; font-variant-numeric:tabular-nums; }

/* ---------- notices */
.note { border-radius:10px; padding:.9rem 1.1rem; font-size:.94rem; line-height:1.55; margin:.8rem 0; }
.note.info { background:var(--teal-soft); border:1px solid #B9DDE1; color:#0E4650; }
.note.warn { background:#FFF4DA; border:1px solid #F0D79A; color:#6B4A07; }
.note.err { background:#FDECEA; border:1px solid #F2B8B2; color:#7A1F17; }
.note b { color:inherit; }
.empty { border:2px dashed #B7CDD3; border-radius:14px; padding:2.2rem 1.5rem; text-align:center; color:var(--muted); background:#fff; }
.person { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:1rem 1.2rem; }
.person .nm { font-weight:600; color:var(--ink); font-size:1.05rem; }
.person .rl { color:var(--muted); font-size:.92rem; }

/* ---------- widgets */
.stButton > button[kind="primary"] { background:var(--teal); border:0; border-radius:10px; font-weight:600; padding:.6rem 1.3rem; }
.stButton > button[kind="primary"]:hover { background:#0B656E; }
[data-testid="stFileUploader"] section { background:#fff; border:2px dashed #9FC0C8; border-radius:14px; }
a:focus-visible, button:focus-visible { outline:3px solid #F2B65E !important; outline-offset:2px; }

@media (max-width:900px){
  .hero { flex-direction:column; padding:1.8rem; }
  .hero .art { flex-basis:auto; max-width:260px; }
  .scale { grid-template-columns:1fr; }
  .bar-row { grid-template-columns:8rem 1fr 3.6rem; }
}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def _flat(markup: str) -> str:
    """Strip indentation/blank lines so Markdown never mistakes the HTML for a code block."""
    return "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())


def html(markup: str) -> None:
    st.markdown(_flat(markup), unsafe_allow_html=True)


def esc(text) -> str:
    return _html.escape(str(text))


def retina_svg() -> str:
    return (config.ASSETS_DIR / "retina.svg").read_text(encoding="utf-8")


def logo_mark() -> str:
    return (
        '<svg class="mark" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<circle cx="20" cy="20" r="19" fill="#0F7C86"/>'
        '<circle cx="20" cy="20" r="12" fill="none" stroke="#fff" stroke-width="2"/>'
        '<circle cx="23" cy="19" r="5" fill="#fff"/></svg>'
    )


def page_header(title: str, subtitle: str = "") -> None:
    sub = f"<p>{esc(subtitle)}</p>" if subtitle else ""
    html(f'<div class="page-head"><h1>{esc(title)}</h1>{sub}</div>')


def notice(kind: str, body_html: str) -> None:
    """kind: info | warn | err. body_html may contain <b> tags; escape user text first."""
    html(f'<div class="note {kind}">{body_html}</div>')


def metric(label: str, value: str, sub: str = "", accent: bool = False) -> str:
    cls = "metric accent" if accent else "metric"
    sub_html = f'<div class="sub">{esc(sub)}</div>' if sub else ""
    return f'<div class="{cls}"><div class="lab">{esc(label)}</div><div class="val">{esc(value)}</div>{sub_html}</div>'


def score_bars(scores, predicted: int) -> str:
    rows = []
    for g, s in enumerate(scores):
        top = " top" if g == predicted else ""
        rows.append(
            f'<div class="bar-row{top}" style="--c:{GRADE_COLORS[g]}">'
            f'<div class="name">Grade {g} — {esc(config.CLASS_NAMES[g])}</div>'
            f'<div class="track"><div class="fill" style="width:{s * 100:.2f}%"></div></div>'
            f'<div class="pct">{s * 100:.2f}%</div></div>'
        )
    return '<div class="bars">' + "".join(rows) + "</div>"


def result_card(result) -> None:
    c = GRADE_COLORS[result.grade]
    html(
        f"""
        <div class="result" style="--c:{c}">
        <div class="kicker">Predicted grade</div>
        <div class="grade">Grade {result.grade} — {esc(result.label)}</div>
        <div class="score"><b>{result.score * 100:.2f}%</b><span>model output score for this grade</span></div>
        {score_bars(result.scores, result.grade)}
        </div>
        """
    )
