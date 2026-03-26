import streamlit as st
import streamlit.components.v1 as components


def section_title(title: str) -> None:
    html = f"""
    <div style="
        background: #FFF9F3;
        padding: 14px 18px;
        border-radius: 16px;
        border-left: 6px solid #E89C4A;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 14px;
    ">
        <h3 style="margin:0; color:#2B2B2B;">{title}</h3>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def route_card(title: str, time_min: float, distance_km: float, fuel_cost: float, traffic_status: str) -> None:
    traffic_color = "#2E8B57"
    if traffic_status == "ปานกลาง":
        traffic_color = "#D97706"
    elif traffic_status == "หนาแน่น":
        traffic_color = "#DC2626"

    html = f"""
    <div style="
        background: #FFF9F3;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 12px;
        border: 1px solid rgba(232, 156, 74, 0.18);
        height: 220px;
    ">
        <div style="
            font-size: 20px;
            font-weight: 700;
            color: #8B5E3C;
            margin-bottom: 10px;
        ">
            {title}
        </div>

        <div style="
            font-size: 16px;
            color: #2B2B2B;
            line-height: 1.9;
        ">
            ⏱ {time_min:.0f} นาที<br>
            📍 {distance_km:.1f} กม.<br>
            ⛽ {fuel_cost:.0f} บาท<br>
            <span style="color:{traffic_color}; font-weight:700;">🚦 {traffic_status}</span>
        </div>
    </div>
    """

    components.html(html, height=240)