def get_css() -> str:
    return """
    <style>
    :root {
        --bg: #CD853F;
        --card: #FFF9F3;
        --accent: #E89C4A;
        --accent-dark: #C97D2B;
        --text: #2B2B2B;
        --subtext: #6B5B4D;
        --shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    .stApp {
        background: var(--bg);
    }

    html, body, [class*="css"] {
        font-family: "Segoe UI", sans-serif;
        color: var(--text);
    }

    .hero-box {
        background: linear-gradient(135deg, #FFF3E8 0%, #FFE3CC 100%);
        padding: 42px 28px;
        border-radius: 26px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: var(--shadow);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #8B5E3C;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #5C4A3D;
    }

    .main-result {
        background: white;
        padding: 24px;
        border-radius: 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
        margin-top: 14px;
        margin-bottom: 20px;
    }

    .main-result-title {
        font-size: 24px;
        font-weight: 700;
        color: var(--accent-dark);
        margin-bottom: 8px;
    }

    .main-result-metric {
        font-size: 28px;
        font-weight: 800;
        color: var(--accent-dark);
        margin-bottom: 10px;
    }

    .result-pill {
        margin-top: 15px;
        display: inline-block;
        background: #E89C4A;
        padding: 10px 18px;
        border-radius: 14px;
        color: white;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }

    .small-note {
        color: var(--subtext);
        font-size: 14px;
        margin-top: 10px;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.10);
        background: #FFFDF9;
        color: var(--text);
    }

    div[data-testid="stButton"] button {
        background: #F4A261;
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.65rem 1rem;
    }

    div[data-testid="stButton"] button:hover {
        background: #E58D45;
        color: white;
    }

    .map-box {
        background: var(--card);
        border-radius: 22px;
        box-shadow: var(--shadow);
        padding: 24px;
        border: 1px solid rgba(232, 156, 74, 0.18);
        margin-top: 12px;
    }

    
    </style>
    """