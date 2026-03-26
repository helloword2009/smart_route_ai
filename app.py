import pandas as pd
import pydeck as pdk
import streamlit as st

from config.settings import APP_TITLE, APP_TAGLINE
from styles import get_css
from utils.route_logic import simulate_routes, get_best_routes
from utils.ui_helpers import route_card, section_title
from utils.map_logic import (
    load_places,
    get_place_coords,
    build_route_variants,
    build_fallback_variants,
)



st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🚗",
    layout="wide"
)

# โหลด style แยกไฟล์
st.markdown(get_css(), unsafe_allow_html=True)

# session
if "routes_df" not in st.session_state:
    st.session_state.routes_df = None

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

col1, col2, col3 = st.columns([1.3, 1.3, 0.8])

with col1:
    origin = st.selectbox("ต้นทาง", place_names, index=0)

with col2:
    destination = st.selectbox("ปลายทาง", place_names, index=1)

with col3:
    st.write("")
    st.write("")
    calculate = st.button("คำนวณ", use_container_width=True)

# คำนวณ route
if calculate and origin == destination:
    st.warning("กรุณาเลือกต้นทางและปลายทางให้ต่างกัน")
if calculate and origin and destination and origin != destination:
    st.session_state.routes_df = simulate_routes(origin, destination)

# RESULT
section_title("เส้นทางแนะนำ")

if st.session_state.routes_df is None:
    st.warning("กรอกต้นทางและปลายทาง แล้วกดคำนวณ")
else:
    df = st.session_state.routes_df
    best_routes = get_best_routes(df)
    recommended = best_routes["balanced"]

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
section_title("ตัวเลือกเส้นทาง")

if st.session_state.routes_df is not None:
    fastest = best_routes["fastest"]
    cheapest = best_routes["cheapest"]
    balanced = best_routes["balanced"]

    c1, c2, c3 = st.columns(3)

    with c1:
        route_card(
            
            "เร็วที่สุด",
            fastest["time_min"],
            fastest["distance_km"],
            fastest["fuel_cost_baht"],
            fastest["traffic_status"]
        )

    with c2:
        route_card(
            "ประหยัดที่สุด",
            cheapest["time_min"],
            cheapest["distance_km"],
            cheapest["fuel_cost_baht"],
            cheapest["traffic_status"]
        )

    with c3:
        route_card(
            "แนะนำที่สุด",
            balanced["time_min"],
            balanced["distance_km"],
            balanced["fuel_cost_baht"],
            balanced["traffic_status"]
        )

section_title("แผนที่เส้นทาง")

if st.session_state.routes_df is None:
    st.warning("เลือกต้นทางและปลายทาง แล้วกดคำนวณเพื่อแสดงแผนที่")
else:
    start_lat, start_lon = get_place_coords(places_df, origin)
    end_lat, end_lon = get_place_coords(places_df, destination)

    points_df = pd.DataFrame({
        "name": ["ต้นทาง", "ปลายทาง"],
        "lat": [start_lat, end_lat],
        "lon": [start_lon, end_lon],
    })

    route_variants = build_route_variants(origin, destination)
    if route_variants is None:
        route_variants = build_fallback_variants(start_lat, start_lon, end_lat, end_lon)

    route_df = pd.DataFrame({
        "route_name": ["เร็วที่สุด", "ประหยัดที่สุด", "แนะนำที่สุด"],
        "color": [
            [59, 130, 246],   # น้ำเงิน
            [34, 197, 94],    # เขียว
            [232, 156, 74],   # ส้ม
        ],
        "path": [
            route_variants["fastest"],
            route_variants["cheapest"],
            route_variants["balanced"],
        ]
    })

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=points_df,
        get_position="[lon, lat]",
        get_radius=45,
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
        width_min_pixels=4,
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

    legend_col1, legend_col2, legend_col3 = st.columns(3)

    with legend_col1:
        st.markdown("""
            <div style="font-size:20px; font-weight:700;">
                🔵 เร็วที่สุด
                 </div>
                """, unsafe_allow_html=True)

    with legend_col2:
        st.markdown("""
            <div style="font-size:20px; font-weight:700;">
                    🟢 ประหยัดที่สุด
                    </div>
                    """, unsafe_allow_html=True)

    with legend_col3:
        st.markdown("""
            <div style="font-size:20px; font-weight:700;">
            🟠 แนะนำที่สุด
            </div>
                """, unsafe_allow_html=True)