def get_css() -> str:
    return """
    <style>
    :root {
        --bg: #0D3B66;
        --card: rgba(222, 235, 250, 0.96);
        --card-strong: #FFF8E8;
        --accent: #F4D35E;
        --accent-dark: #EE964B;
        --accent-soft: rgba(244, 211, 94, 0.22);
        --text: #102A43;
        --subtext: #4A6072;
        --line: rgba(13, 59, 102, 0.14);
        --shadow: 0 10px 30px rgba(7, 28, 48, 0.16);
    }

    .stApp {
        background:
            radial-gradient(circle at 12% 10%, rgba(255, 248, 225, 0.34) 0%, rgba(255, 248, 225, 0) 28%),
            radial-gradient(circle at 82% 14%, rgba(244, 211, 94, 0.22) 0%, rgba(244, 211, 94, 0) 20%),
            radial-gradient(circle at 88% 100%, rgba(24, 67, 108, 0.24) 0%, rgba(24, 67, 108, 0) 38%),
            linear-gradient(135deg, #3B79AF 0%, #20527F 48%, #12395D 100%);
        background-attachment: fixed;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background:
            linear-gradient(118deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.04) 18%, rgba(255,255,255,0) 32%),
            radial-gradient(circle at 18% 18%, rgba(255,251,235,0.18) 0%, rgba(255,251,235,0) 16%),
            radial-gradient(circle at 76% 16%, rgba(244,211,94,0.14) 0%, rgba(244,211,94,0) 20%),
            repeating-linear-gradient(
                135deg,
                rgba(255,255,255,0.024) 0px,
                rgba(255,255,255,0.024) 2px,
                rgba(255,255,255,0) 2px,
                rgba(255,255,255,0) 18px
            );
        mix-blend-mode: soft-light;
        opacity: 0.92;
        z-index: 0;
    }

    .block-container {
        position: relative;
        z-index: 1;
    }

    html, body, [class*="css"] {
        font-family: Tahoma, "Noto Sans Thai", "Segoe UI", sans-serif;
        color: var(--text);
        line-height: 1.5;
    }

    p, label, span, div {
        letter-spacing: 0.01em;
    }

    .hero-box {
        background:
            linear-gradient(140deg, rgba(223, 236, 252, 0.98) 0%, rgba(203, 224, 247, 0.94) 100%);
        padding: 42px 28px;
        border-radius: 26px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: var(--shadow);
        border: 1px solid rgba(157, 188, 224, 0.42);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 700;
        color: #0D3B66;
        margin-bottom: 8px;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 19px;
        font-weight: 600;
        color: #284B72;
        line-height: 1.5;
    }

    .main-result {
        background: rgba(223, 236, 252, 0.97);
        padding: 24px;
        border-radius: 22px;
        box-shadow: var(--shadow);
        text-align: center;
        margin-top: 14px;
        margin-bottom: 20px;
        border: 1px solid rgba(157, 188, 224, 0.38);
    }

    .main-result-title {
        font-size: 22px;
        font-weight: 700;
        color: #0D3B66;
        margin-bottom: 8px;
    }

    .main-result-metric {
        font-size: 30px;
        font-weight: 700;
        color: #0D3B66;
        margin-bottom: 10px;
        line-height: 1.25;
    }

    .result-pill {
        margin-top: 15px;
        display: inline-block;
        background: linear-gradient(135deg, #F4D35E 0%, #EE964B 100%);
        padding: 10px 18px;
        border-radius: 14px;
        color: #0A2239;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 8px 20px rgba(238, 150, 75, 0.22);
    }

    .small-note {
        color: #284B72;
        font-size: 15px;
        font-weight: 500;
        margin-top: 10px;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stButton"] button p {
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF;
    }

    div[data-baseweb="select"] > div {
        background: rgba(223, 236, 252, 0.98) !important;
        border: 1px solid rgba(157, 188, 224, 0.34) !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 18px rgba(7, 28, 48, 0.12);
        color: #0D3B66 !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] svg,
    div[data-baseweb="select"] * {
        font-size: 17px;
        font-weight: 600;
        color: #0D3B66 !important;
        fill: #0D3B66 !important;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 12px;
        border: 1px solid rgba(157, 188, 224, 0.34);
        background: rgba(223, 236, 252, 0.98);
        color: var(--text);
    }

    div[data-testid="stButton"] button {
        background: linear-gradient(135deg, #F4D35E 0%, #EE964B 100%);
        color: #0A2239;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.65rem 1rem;
        font-size: 17px;
        box-shadow: 0 10px 24px rgba(238, 150, 75, 0.22);
    }

    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #FFD54F 0%, #F08A3C 100%);
        color: #0A2239;
    }

    .map-box {
        background: rgba(223, 236, 252, 0.95);
        border-radius: 22px;
        box-shadow: var(--shadow);
        padding: 24px;
        border: 1px solid rgba(157, 188, 224, 0.38);
        margin-top: 12px;
    }

    .map-label-overlay {
        position: relative;
        z-index: 5;
        margin-bottom: -54px;
        padding: 14px 16px 0;
        pointer-events: none;
    }

    .map-label-row {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: flex-start;
    }

    .map-label-chip {
        max-width: 42%;
        background: rgba(13, 59, 102, 0.88);
        color: #FFFFFF;
        padding: 10px 14px;
        border-radius: 14px;
        box-shadow: 0 10px 24px rgba(7, 28, 48, 0.24);
        backdrop-filter: blur(6px);
    }

    .map-label-chip.right {
        text-align: right;
        margin-left: auto;
    }

    .map-label-chip-title {
        font-size: 13px;
        font-weight: 700;
        color: rgba(255, 248, 225, 0.92);
        margin-bottom: 3px;
    }

    .map-label-chip-name {
        font-size: 15px;
        font-weight: 700;
        line-height: 1.35;
        color: #FFFFFF;
        word-break: break-word;
    }
    </style>
    """
