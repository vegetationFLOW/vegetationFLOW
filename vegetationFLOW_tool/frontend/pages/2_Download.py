import json
import requests
import yaml
import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
from shapely.geometry import shape, GeometryCollection

BACKEND_API = "http://localhost:8000/" # Update the Port Number if changed in docker-compose

st.set_page_config(
    page_title="Download",
    page_icon=":card_file_box:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------------------ Cached Functions and Resources
@st.cache_data
def load_content():
    with open("content/download.yaml", "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
    return content

def checkValidDates(start_date, end_date):
    return start_date <= end_date

def checkInputs(datasetName, roi_file, start_date, end_date, data_opt): 
    issues = []
    if len(datasetName)==0:
        issues.append("Please provide a Dataset Name!")
    if not roi_file:
        issues.append("Please provide a ROI!")
    if not checkValidDates(start_date, end_date):
        issues.append("Please select valid date range!")
    if data_opt is None:
        issues.append("Please select a dataset collection!")
    return issues

# ---------------------------------- Session State
if "downloaded_started" not in st.session_state:
    st.session_state["downloaded_started"] = False

if "is_downloading" not in st.session_state:
    st.session_state["is_downloading"] = False

if "task_id" not in st.session_state:
    st.session_state["task_id"] = None

# ----------------------------------- UI Related
content = load_content()
st.markdown("<h1 style='text-align: center;'>Download Data Page</h1>", unsafe_allow_html=True)

collection_type = st.selectbox(
        label="Type of Data Collection",
        options=["Vegetation Health Assessment", "Fire Secerity Mapping"],
        accept_new_options=False,
    )
leftcol, rightcol, = st.columns([2,1.5], border=True, vertical_alignment="top")
with leftcol:
    # Dataset
    dataset_container = st.container(border=True)
    dataset_container.subheader("Dataset Options", anchor=False)
    data_opt = dataset_container.selectbox(
        label="Compatible Collections", 
        options=("Landsat 8"),
        index=None,
    )

    # Dates
    date_container = st.container(border=True)
    if collection_type == "Vegetation Health Assessment":
        date_container.subheader("Date Range", anchor=False)
        subleft, subright = date_container.columns(2)
        with subleft:
            start_date = st.date_input("Start", datetime.now().date())
        with subright:
            end_date = st.date_input("End", datetime.now().date())

        if not checkValidDates(start_date, end_date):
            date_container.error('Invalid Date Range', icon="🚨")
    else:
        date_container.subheader("Fire Event Date Range", anchor=False)
        subleft, subright = date_container.columns(2)
        with subleft:
            start_date = st.date_input("Pre Fire", datetime.now().date())
        with subright:
            end_date = st.date_input("Post Fire", datetime.now().date())
        
        if not checkValidDates(start_date, end_date):
            date_container.error('Invalid Date Range', icon="🚨")


    if not checkValidDates(start_date, end_date):
        date_container.error('Invalid Date Range', icon="🚨")

    # Select ROI
    with st.container(border=True):
        st.subheader("ROI Shapefile", anchor=False)
        roi_file = st.file_uploader(label="Choose a GeoJSON file", type=["geojson"], accept_multiple_files=False)
    
    # Select Satelitte Image Size Exports
    with st.container(border=True):
        st.subheader("Image Properties")
        pixel_size = st.slider(label="Image Size", min_value=128, max_value=512, value=256)
    
    # Dataset Name
    datasetName = st.text_input(label="Dataset Name")

with rightcol:
    m = folium.Map(location=[-37, 175], zoom_start=8)
    if roi_file:
        try:
            geojson_data = json.load(roi_file)
            folium.GeoJson(geojson_data, name="Uploaded ROI").add_to(m)

            # Get bounds from all features
            shapes = [shape(f["geometry"]) for f in geojson_data["features"]]
            collection = GeometryCollection(shapes)
            bounds = collection.bounds  # (minx, miny, maxx, maxy)

            # Fit map to bounds
            m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

            st.success("GeoJSON loaded and added to map.")
        except Exception as e:
            st.error(f"Error reading GeoJSON: {e}")
    
    ui_map = st_folium(m, height=800, width=None)

download_btn = st.button(
        label="Start Downloading",
        use_container_width=True,
        disabled=st.session_state["downloaded_started"]
    )
if download_btn:
    issues = checkInputs(datasetName, roi_file, start_date, end_date, data_opt)
    if len(issues) > 0:
        for i in issues:
            st.error(i)
    else:
        st.session_state["downloaded_started"] = True
        st.rerun()

# ----------------------------------------- Connect UI with Backend placeholder for now  
# If button pressed but API call not made
if not st.session_state["is_downloading"] and st.session_state["downloaded_started"]:
    # Backend Logic
    roi_content = roi_file.read().decode("utf-8")
    payload = {
        "Dataset_Name" : datasetName,
        "Collection_Type" : data_opt,
        "Start_Year" : start_date.year,
        "End_Year" : end_date.year,
        "ROI" :  roi_content,
        "Patch_Size" : pixel_size

    }
    response = requests.post(f"{BACKEND_API}/start-download/", json=payload)
    if response.status_code == 200:
        st.success(f"Task submitted. Task ID: {response.json()['task_id']}")
        task_id = response.json()["task_id"]
        st.session_state.task_id = task_id
        st.session_state["is_downloading"] = True
    else:
        st.error("Failed to submit task")

# If Download btn pressed and successfull API call to backend -> Show progress bar
if st.session_state["is_downloading"] and st.session_state["downloaded_started"]:
    st.success(f"Task submitted. Task ID: {st.session_state['task_id']}")
    # Connect to backend to get progress update on task
    response = requests.get(f"{BACKEND_API}/download-status/{st.session_state['task_id']}").json()
    prg_bar = st.progress(response["progress"], "Downloading...")

