import pandas as pd
import pydeck as pdk
import streamlit as st

from config.settings import APP_TAGLINE, APP_TITLE
from styles import get_css
from utils.map_logic import get_place_coords, get_route_options, load_places
from utils.ui_helpers import route_card, section_title


ROUTE_COLORS = {
    "balanced": [244, 211, 94],
    "fastest": [60, 120, 216],
    "cheapest": [90, 150, 214],
}
REFERENCE_POINT_COLOR = [13, 59, 102, 120]
REFERENCE_TEXT_COLOR = [30, 65, 107]
ROUTE_OUTLINE_COLOR = [255, 248, 225, 210]
DEFAULT_MAP_STYLE = "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"


def route_label(row: pd.Series) -> str:
    return f"{row['route_name']} | {row['time_min']:.0f} นาที | {row['distance_km']:.1f} กม."


def route_zoom_level(distance_km: float) -> float:
    if distance_km <= 2:
        return 16.8
    if distance_km <= 4:
        return 16.3
    if distance_km <= 7:
        return 15.8
    if distance_km <= 10:
        return 15.3
    return 14.8


def nearby_reference_places(places_df: pd.DataFrame, origin: str, destination: str, route_path: list) -> pd.DataFrame:
    reference_df = places_df[~places_df["name"].isin([origin, destination])].copy()
    if reference_df.empty:
        return reference_df

    lons = [point[0] for point in route_path]
    lats = [point[1] for point in route_path]
    min_lon, max_lon = min(lons), max(lons)
    min_lat, max_lat = min(lats), max(lats)

    padding = 0.01
    in_bounds = (
        reference_df["lon"].between(min_lon - padding, max_lon + padding)
        & reference_df["lat"].between(min_lat - padding, max_lat + padding)
    )
    filtered_df = reference_df[in_bounds].copy()

    if filtered_df.empty:
        filtered_df = reference_df.copy()

    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    filtered_df["distance_score"] = (
        (filtered_df["lat"] - center_lat).abs() + (filtered_df["lon"] - center_lon).abs()
    )
    filtered_df = filtered_df.sort_values("distance_score").head(20).copy()
    filtered_df["point_type"] = "จุดอ้างอิงในนครสวรรค์"
    filtered_df["title"] = filtered_df["point_type"]
    filtered_df["detail"] = filtered_df["name"]
    filtered_df["label_size"] = filtered_df["distance_score"].apply(lambda value: 13 if value < 0.01 else 12)

    return filtered_df


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🚗",
    layout="wide",
)

st.markdown(get_css(), unsafe_allow_html=True)

if "routes_df" not in st.session_state:
    st.session_state.routes_df = None
if "last_origin" not in st.session_state:
    st.session_state.last_origin = None
if "last_destination" not in st.session_state:
    st.session_state.last_destination = None
if "selected_route_key" not in st.session_state:
    st.session_state.selected_route_key = "balanced"

places_df = load_places()
place_names = places_df["name"].tolist()

st.markdown(
    f"""
    <div class="hero-box">
        <div class="hero-title">{APP_TITLE}</div>
        <div class="hero-subtitle">{APP_TAGLINE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

section_title("เลือกการเดินทาง")

col1, col2, col3 = st.columns([1.4, 1.4, 0.8], vertical_alignment="bottom")

with col1:
    origin = st.selectbox("ต้นทาง", place_names, index=0)

with col2:
    destination = st.selectbox("ปลายทาง", place_names, index=1)

with col3:
    calculate = st.button("คำนวณ", use_container_width=True)

if calculate and origin == destination:
    st.warning("กรุณาเลือกต้นทางและปลายทางให้ต่างกัน")

elif calculate and origin and destination and origin != destination:
    try:
        start_lat, start_lon = get_place_coords(places_df, origin)
        end_lat, end_lon = get_place_coords(places_df, destination)

        routes_df = get_route_options(start_lat, start_lon, end_lat, end_lon)
        if routes_df.empty:
            raise ValueError("ไม่พบเส้นทางที่ใช้งานได้")

        st.session_state.routes_df = routes_df
        st.session_state.last_origin = origin
        st.session_state.last_destination = destination
        st.session_state.selected_route_key = (
            "balanced" if "balanced" in routes_df["route_key"].values else routes_df.iloc[0]["route_key"]
        )

    except Exception as e:
        st.session_state.routes_df = None
        st.error(f"เกิดข้อผิดพลาดจาก API: {e}")

section_title("เส้นทางแนะนำ")

selected_route = None

if st.session_state.routes_df is None:
    st.warning("กรอกต้นทางและปลายทาง แล้วกดคำนวณ")
else:
    df = st.session_state.routes_df.copy()
    route_options = {route_label(row): row["route_key"] for _, row in df.iterrows()}
    route_keys = list(route_options.values())

    if st.session_state.selected_route_key not in route_keys:
        st.session_state.selected_route_key = route_keys[0]

    default_index = route_keys.index(st.session_state.selected_route_key)
    selected_label = st.selectbox("เลือกเส้นทางที่ต้องการแสดง", list(route_options.keys()), index=default_index)
    st.session_state.selected_route_key = route_options[selected_label]
    selected_route = df[df["route_key"] == st.session_state.selected_route_key].iloc[0]

    result_html = f"""
    <div class="main-result">
        <div class="main-result-title">เส้นทางที่เลือก</div>
        <div class="main-result-metric">{selected_route['route_name']}</div>
        <div class="result-pill">
            ⏱ {selected_route['time_min']:.0f} นาที &nbsp;&nbsp;
            📍 {selected_route['distance_km']:.1f} กม. &nbsp;&nbsp;
            ⛽ {selected_route['fuel_cost_baht']:.0f} บาท
        </div>
        <div class="small-note">
            แผนที่จะซูมอัตโนมัติตามระยะทางและแสดงจุดอ้างอิงที่อยู่ใกล้เส้นทางในนครสวรรค์ให้มากที่สุดเท่าที่ข้อมูลตอนนี้มี
        </div>
    </div>
    """
    st.markdown(result_html, unsafe_allow_html=True)

section_title("รายละเอียดเส้นทาง")

if selected_route is not None:
    route_card(
        str(selected_route["route_name"]),
        float(selected_route["time_min"]),
        float(selected_route["distance_km"]),
        float(selected_route["fuel_cost_baht"]),
        str(selected_route["traffic_status"]),
    )

section_title("แผนที่เส้นทาง")

if st.session_state.routes_df is None or selected_route is None:
    st.warning("เลือกต้นทางและปลายทาง แล้วกดคำนวณเพื่อแสดงแผนที่")
else:
    map_origin = st.session_state.last_origin
    map_destination = st.session_state.last_destination

    start_lat, start_lon = get_place_coords(places_df, map_origin)
    end_lat, end_lon = get_place_coords(places_df, map_destination)
    route_start_lon, route_start_lat = selected_route["path"][0]
    route_end_lon, route_end_lat = selected_route["path"][-1]

    points_df = pd.DataFrame(
        {
            "name": [map_origin, map_destination],
            "point_type": ["ต้นทาง", "ปลายทาง"],
            "lat": [route_start_lat, route_end_lat],
            "lon": [route_start_lon, route_end_lon],
            "source_lat": [start_lat, end_lat],
            "source_lon": [start_lon, end_lon],
        }
    )
    points_df["title"] = points_df["point_type"]
    points_df["detail"] = points_df.apply(
        lambda row: f"{row['name']}<br/>พิกัดอ้างอิง {row['source_lat']:.5f}, {row['source_lon']:.5f}",
        axis=1,
    )

    route_df = pd.DataFrame([selected_route.to_dict()])
    route_df["color"] = [ROUTE_COLORS.get(selected_route["route_key"], [232, 156, 74])]
    route_df["outline_color"] = [ROUTE_OUTLINE_COLOR]
    route_df["title"] = [selected_route["route_name"]]
    route_df["detail"] = [
        f"{selected_route['time_min']:.0f} นาที | {selected_route['distance_km']:.1f} กม. | {selected_route['fuel_cost_baht']:.0f} บาท"
    ]

    route_outline_layer = pdk.Layer(
        "PathLayer",
        data=route_df,
        get_path="path",
        get_color="outline_color",
        width_scale=7,
        width_min_pixels=6,
        pickable=False,
        rounded=True,
    )

    line_layer = pdk.Layer(
        "PathLayer",
        data=route_df,
        get_path="path",
        get_color="color",
        width_scale=5,
        width_min_pixels=3,
        pickable=True,
        rounded=True,
    )

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=points_df,
        get_position="[lon, lat]",
        get_radius=26,
        get_fill_color=[232, 156, 74, 220],
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=(start_lat + end_lat) / 2,
        longitude=(start_lon + end_lon) / 2,
        zoom=route_zoom_level(float(selected_route["distance_km"])),
        pitch=0,
    )

    deck = pdk.Deck(
        map_style=DEFAULT_MAP_STYLE,
        initial_view_state=view_state,
        layers=[
            route_outline_layer,
            line_layer,
            point_layer,
        ],
        tooltip={
            "html": "<b>{title}</b><br/>{detail}",
            "style": {
                "backgroundColor": "#0D3B66",
                "color": "#FFF8E1",
                "fontSize": "14px",
                "padding": "8px 10px",
                "borderRadius": "8px",
            },
        },
    )
    st.pydeck_chart(deck, use_container_width=True)

