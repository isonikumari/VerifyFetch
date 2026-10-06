import base64
from pathlib import Path

import streamlit as st
from langchain_google_genai.chat_models import GoogleRateLimitError

from main import run_fact_check


st.set_page_config(
    page_title="Fact Checker",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

background_path = Path(__file__).parent / "assets" / "fact-check-background.svg"
background_image = base64.b64encode(background_path.read_bytes()).decode("ascii")

st.markdown(
    f"""
    <style>
    :root {{
        color-scheme: dark;
        --ink: #edf3fa;
        --muted: #a1b1c5;
        --accent: #9ae6c0;
        --panel: rgba(12, 25, 42, 0.88);
        --line: rgba(177, 200, 224, 0.16);
    }}

    .stApp {{
        background: #081321;
        color: var(--ink);
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background-image:
            linear-gradient(180deg, rgba(8, 19, 33, 0.28), rgba(8, 19, 33, 0.88)),
            url("data:image/svg+xml;base64,{background_image}");
        background-size: cover;
        background-position: center;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        position: relative;
        z-index: 1;
    }}

    .block-container {{
        max-width: 980px;
        padding: 2.5rem 1.5rem 5rem;
    }}

    .brand-row {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #edf3fa;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.14em;
    }}

    .brand-mark {{
        display: grid;
        width: 2.35rem;
        height: 2.35rem;
        place-items: center;
        border: 1px solid rgba(154, 230, 192, 0.48);
        border-radius: 0.75rem;
        color: var(--accent);
        font-size: 0.78rem;
        letter-spacing: 0.04em;
    }}

    .brand-note {{
        display: block;
        margin-top: 0.2rem;
        color: var(--muted);
        font-size: 0.62rem;
        font-weight: 500;
        letter-spacing: 0.16em;
    }}

    .hero {{
        max-width: 720px;
        margin: 3.6rem 0 2rem;
    }}

    .eyebrow {{
        margin: 0 0 0.85rem;
        color: var(--accent);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
    }}

    .hero h1 {{
        margin: 0;
        color: var(--ink);
        font-size: clamp(2.6rem, 6vw, 4.4rem);
        font-weight: 650;
        letter-spacing: -0.055em;
        line-height: 1.04;
    }}

    .hero p:last-child {{
        max-width: 570px;
        margin: 1rem 0 0;
        color: #b5c3d3;
        font-size: 1.08rem;
        line-height: 1.7;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: var(--line);
        border-radius: 1.15rem;
        background: var(--panel);
        box-shadow: 0 18px 60px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(16px);
    }}

    [data-testid="stWidgetLabel"] p,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{
        color: #dce6f1;
    }}

    div[data-testid="stTextInput"] input {{
        min-height: 3.1rem;
        border-color: rgba(177, 200, 224, 0.23);
        border-radius: 0.7rem;
        background: rgba(5, 15, 27, 0.75);
    }}

    div[data-testid="stTextInput"] input:focus {{
        border-color: var(--accent);
        box-shadow: 0 0 0 1px var(--accent);
    }}

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {{
        min-height: 2.9rem;
        border: 1px solid rgba(154, 230, 192, 0.45);
        border-radius: 0.7rem;
        background: #9ae6c0;
        color: #082018;
        font-weight: 700;
        transition: transform 140ms ease, background 140ms ease;
    }}

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {{
        border-color: #b8f3d3;
        background: #b8f3d3;
        color: #082018;
        transform: translateY(-1px);
    }}

    [data-testid="stExpander"] {{
        overflow: hidden;
        border: 1px solid var(--line);
        border-radius: 0.85rem;
        background: rgba(12, 25, 42, 0.78);
    }}

    [data-testid="stExpander"] summary p {{
        color: var(--ink);
        font-weight: 600;
    }}

    [data-testid="stCaptionContainer"] p {{
        color: var(--muted);
    }}

    @media (max-width: 640px) {{
        .block-container {{
            padding: 1.5rem 1rem 3rem;
        }}

        .hero {{
            margin-top: 2.6rem;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brand-row">
        <span class="brand-mark">FC</span>
        <span>FACT CHECKER
            <span class="brand-note">INDEPENDENT CLAIM ANALYSIS</span>
        </span>
    </div>
    <section class="hero">
        <p class="eyebrow">Research before you share</p>
        <h1>Separate the claim<br>from the evidence.</h1>
        <p>Get a clear, evidence-led breakdown of a claim, with the option to run an additional quality review.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.subheader("Analyze a claim")
    st.caption("Enter a statement you’d like to check. We’ll break it down and search for supporting evidence.")

    with st.form("fact_check_form"):
        claim = st.text_input(
            "Claim",
            placeholder="e.g. A specific statement you want to verify",
        )
        review_column, submit_column = st.columns([3, 2], vertical_alignment="center")
        with review_column:
            review = st.checkbox(
                "Run quality review",
                value=False,
                help="Adds a critic and possible revision pass to improve the report. This takes longer and uses additional requests.",
            )
        with submit_column:
            submitted = st.form_submit_button(
                "Analyze claim",
                type="primary",
                use_container_width=True,
            )

if submitted:
    if not claim.strip():
        st.warning("Enter a claim before starting the analysis.")
    else:
        try:
            with st.spinner("Checking the claim and gathering evidence..."):
                st.session_state["fact_check_result"] = run_fact_check(
                    claim.strip(),
                    review=review,
                )
                st.session_state["fact_check_claim"] = claim.strip()
        except GoogleRateLimitError:
            st.error(
                "Gemini rejected this request because the API project's quota or rate "
                "limit has been reached. Replacing the API key does not reset a quota "
                "shared by keys in the same Google Cloud project."
            )
            st.markdown(
                "Check [Gemini API usage](https://ai.dev/rate-limit) and "
                "[rate limits and billing](https://ai.google.dev/gemini-api/docs/rate-limits). "
                "Wait for the applicable quota to reset, enable billing or request a "
                "higher quota, or use an API key from a project with available quota."
            )
            st.stop()

if "fact_check_result" in st.session_state:
    result = st.session_state["fact_check_result"]
    st.markdown("### Your fact check")
    st.caption("Claim analyzed")
    st.write(st.session_state["fact_check_claim"])

    with st.container(border=True):
        st.markdown("#### Final report")
        st.write(result["report"])

    with st.expander("Sub-claims", expanded=False):
        st.write(result["sub_claims"])

    with st.expander("Evidence gathered", expanded=False):
        st.write(result["evidence"])

    with st.expander("Quality review", expanded=False):
        st.write(result["feedback"])
