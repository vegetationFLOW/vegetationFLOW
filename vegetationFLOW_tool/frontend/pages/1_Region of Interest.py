# Imports
import yaml
import json

# Imports from additional packages
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import Draw


st.set_page_config(
    page_title="ROI",
    page_icon=":world_map:",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# ------------------------------------ Cached Functions and Resources
@st.cache_data
def load_content():
    with open("content/roi.yaml", "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
    return content

# ---------------------------------- Session State
if "uploaded_roi" not in st.session_state:
    st.session_state["uploaded_roi"] = None

if "roi_map" not in st.session_state:
    st.session_state["roi_map"] = None

# ----------------------------------- UI Related
content = load_content()
st.markdown("<h1 style='text-align: center;'>Welcome to ROI Data Collection!</h1>", unsafe_allow_html=True)
st.subheader("Your First Step Towards Powerful Satellite Analysis")
st.markdown(content["introduction"])
st.markdown("### **Instructions**")
st.markdown(content["instruction_intro"])
col1, col2, col3 = st.columns(3, gap="medium", border=True)
with col1:
    st.markdown(
        "<h4 style='text-align: center;'>1. Draw Your Regions:</h4>",
        unsafe_allow_html=True
    )
    for feat in content["step_1"]:
        st.markdown(f"- {feat}")
with col2:
    st.markdown(
        "<h4 style='text-align: center;'>2. Name Your Features:</h4>",
        unsafe_allow_html=True
    )
    for feat in content["step_2"]:
        st.markdown(f"- {feat}")
with col3:
    st.markdown(
        "<h4 style='text-align: center;'>3. Download Your Data:</h4>",
        unsafe_allow_html=True
    )
    for feat in content["step_3"]:
        st.markdown(f"- {feat}")
st.markdown(content["outro"])

# -------------------------------------------------- Map UI

if st.session_state["roi_map"] is None:
    m = folium.Map(location=[-37, 175], zoom_start=8)
    draw = Draw(
        export=False,
        draw_options={
            "polyline": False,
            "rectangle": True,
            "circle": False,
            "marker": False,
            "circlemarker": False,
        }
    )
    draw.add_to(m)
    st.session_state["roi_map"] = m
else:
    m = st.session_state["roi_map"]

ui_map = st_folium(m, height=650, width=None)

if ui_map["all_drawings"]:
    geojson_data = {
                        "type": "FeatureCollection",
                        "features": ui_map["all_drawings"]
                    }
    geojson_str = json.dumps(geojson_data)
    _, left, right = st.columns([1,4,2], gap="medium") 
    with left:
        shapefile_name = st.text_input(label="Filename", label_visibility="collapsed", placeholder="Provide a filename...")
    
    with right:
        if len(shapefile_name) == 0:
            st.download_button(
                label="Download GeoJSON",
                data=geojson_str,
                file_name=f"{shapefile_name}.geojson",
                disabled=True,
                help="Provide a filename before downloading", 
                )
        else:
            st.download_button(
                label="Download GeoJSON",
                data=geojson_str,
                file_name=f"{shapefile_name}.geojson",
                mime="application/geo+json",
                )