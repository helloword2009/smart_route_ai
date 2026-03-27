import pandas as pd
import pydeck as pdk
import streamlit as st

from config.settings import APP_TITLE, APP_TAGLINE
from styles import get_css
from utils.ui_helpers import route_card, section_title
from utils.map_logic import load_places, get_place_coords, get_real_route_from_ors

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🚗",
    layout="wide"
)

st.markdown(get_css(), unsafe_allow_html=True)

# session
if "routes_df" not in st.session_state:
    st.session_state.routes_df = None
if "last_origin" not in st.session_state:
    st.session_state.last_origin = None
if "last_destination" not in st.session_state:
    st.session_state.last_destination = None

places_df = load_places()
place_names = places_df["name"].tolist()

# HERO
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">{APP_TITLE}</div>
    <div class="hero-subtitle">{APP_TAGLINE}</div>
</div>
""", unsafe_allow_html=True)

# INPUT
section_title("เลือกการเดินทาง")

col1, col2, col3 = st.columns([1.4, 1.4, 0.8], vertical_alignment="bottom")

with col1:
    origin = st.selectbox("ต้นทาง", place_names, index=0)

with col2:
    destination = st.selectbox("ปลายทาง", place_names, index=1)

with col3:
    calculate = st.button("คำนวณ", use_container_width=True)

# CALCULATE
if calculate and origin == destination:
    st.warning("กรุณาเลือกต้นทางและปลายทางให้ต่างกัน")

elif calculate and origin and destination and origin != destination:
    try:
        start_lat, start_lon = get_place_coords(places_df, origin)
        end_lat, end_lon = get_place_coords(places_df, destination)

        real_route = get_real_route_from_ors(start_lat, start_lon, end_lat, end_lon)

        route_rows = [
            {
                "route_key": "balanced",
                "route_name": "🟠 แนะนำที่สุด",
                "distance_km": real_route["distance_km"],
                "time_min": real_route["time_min"],
                "fuel_cost_baht": round(real_route["distance_km"] * 2.2),
                "traffic_status": "สมดุล",
                "path": real_route["path"],
            }
        ]

        st.session_state.routes_df = pd.DataFrame(route_rows)
        st.session_state.last_origin = origin
        st.session_state.last_destination = destination

    except Exception as e:
        st.session_state.routes_df = None
        st.error(f"เกิดข้อผิดพลาดจาก API: {e}")

# RESULT
section_title("เส้นทางแนะนำ")

if st.session_state.routes_df is None:
    st.warning("กรอกต้นทางและปลายทาง แล้วกดคำนวณ")
else:
    df = st.session_state.routes_df
    recommended = df.iloc[0]

    result_html = f"""
    <div class="main-result">
        <div class="main-result-title">🚗 เส้นทางที่แนะนำ</div>
        <div class="main-result-metric">{recommended['route_name']}</div>
        <div class="result-pill">
            ⏱ {recommended['time_min']:.0f} นาที &nbsp;&nbsp;
            📍 {recommended['distance_km']:.1f} กม. &nbsp;&nbsp;
            ⛽ {recommended['fuel_cost_baht']:.0f} บาท
        </div>
        <div class="small-note">
            เหมาะสำหรับผู้ที่ต้องการสมดุลระหว่างเวลาเดินทางและค่าน้ำมัน
        </div>
    </div>
    """
    st.markdown(result_html, unsafe_allow_html=True)

# ROUTE OPTIONS
section_title("รายละเอียดเส้นทาง")

if st.session_state.routes_df is not None:
    recommended = st.session_state.routes_df.iloc[0]

    route_card(
        "แนะนำที่สุด",
        recommended["time_min"],
        recommended["distance_km"],
        recommended["fuel_cost_baht"],
        recommended["traffic_status"]
    )

# MAP
section_title("แผนที่เส้นทาง")

if st.session_state.routes_df is None:
    st.warning("เลือกต้นทางและปลายทาง แล้วกดคำนวณเพื่อแสดงแผนที่")
else:
    map_origin = st.session_state.last_origin
    map_destination = st.session_state.last_destination

    start_lat, start_lon = get_place_coords(places_df, map_origin)
    end_lat, end_lon = get_place_coords(places_df, map_destination)

    points_df = pd.DataFrame({
        "name": ["ต้นทาง", "ปลายทาง"],
        "lat": [start_lat, end_lat],
        "lon": [start_lon, end_lon],
    })

    route_df = st.session_state.routes_df.copy()
    route_df["color"] = [[232, 156, 74]]

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=points_df,
        get_position="[lon, lat]",
        get_radius=35,
        get_fill_color=[232, 156, 74, 220],
        pickable=True,
    )

    text_layer = pdk.Layer(
        "TextLayer",
        data=points_df,
        get_position="[lon, lat]",
        get_text="name",
        get_size=14,
        get_color=[43, 43, 43],
        get_alignment_baseline="'bottom'",
    )

    line_layer = pdk.Layer(
        "PathLayer",
        data=route_df,
        get_path="path",
        get_color="color",
        width_scale=8,
        width_min_pixels=5,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=(start_lat + end_lat) / 2,
        longitude=(start_lon + end_lon) / 2,
        zoom=12.5,
        pitch=0,
    )

    deck = pdk.Deck(
        map_style="light",
        initial_view_state=view_state,
        layers=[line_layer, point_layer, text_layer],
        tooltip={"text": "{route_name}"}
    )

    st.pydeck_chart(deck, use_container_width=True)

    st.markdown("""
    <div style="font-size:20px; font-weight:700; margin-top:8px;">
        🟠 แนะนำที่สุด
    </div>
    """, unsafe_allow_html=True)