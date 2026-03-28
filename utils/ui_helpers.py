import streamlit as st
import streamlit.components.v1 as components


def section_title(title: str) -> None:
    html = f"""
    <div style="
        background: rgba(223, 236, 252, 0.96);
        padding: 12px 16px;
        border-radius: 16px;
        border: 1px solid rgba(157, 188, 224, 0.38);
        margin-bottom: 12px;
        box-shadow: 0 8px 18px rgba(7, 28, 48, 0.12);
    ">
        <h3 style="
            margin:0;
            color:#0D3B66;
            font-size:18px;
            font-weight:700;
            letter-spacing:-0.01em;
        ">{title}</h3>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def route_card(title: str, time_min: float, distance_km: float, fuel_cost: float, traffic_status: str) -> None:
    traffic_color = "#2E8B57"
    if traffic_status == "\u0e1b\u0e32\u0e19\u0e01\u0e25\u0e32\u0e07":
        traffic_color = "#D97706"
    elif traffic_status == "\u0e2b\u0e19\u0e32\u0e41\u0e19\u0e48\u0e19":
        traffic_color = "#DC2626"

    html = f"""
    <div style="
        background: rgba(223, 236, 252, 0.97);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 10px 28px rgba(7, 28, 48, 0.14);
        margin-bottom: 12px;
        border: 1px solid rgba(157, 188, 224, 0.36);
    ">
        <div style="
            font-size: 18px;
            font-weight: 700;
            color: #0D3B66;
            margin-bottom: 14px;
        ">
            {title}
        </div>

        <div style="
            display: grid;
            gap: 10px;
            font-size: 15px;
            color: #102A43;
            line-height: 1.6;
        ">
            <div>\u0e40\u0e27\u0e25\u0e32\u0e40\u0e14\u0e34\u0e19\u0e17\u0e32\u0e07 <strong>{time_min:.0f} \u0e19\u0e32\u0e17\u0e35</strong></div>
            <div>\u0e23\u0e30\u0e22\u0e30\u0e17\u0e32\u0e07 <strong>{distance_km:.1f} \u0e01\u0e21.</strong></div>
            <div>\u0e04\u0e48\u0e32\u0e19\u0e49\u0e33\u0e21\u0e31\u0e19\u0e1b\u0e23\u0e30\u0e21\u0e32\u0e13 <strong>{fuel_cost:.0f} \u0e1a\u0e32\u0e17</strong></div>
            <div style="color:{traffic_color}; font-weight:700;">\u0e2a\u0e20\u0e32\u0e1e\u0e08\u0e23\u0e32\u0e08\u0e23: {traffic_status}</div>
        </div>
    </div>
    """

    components.html(html, height=220)
