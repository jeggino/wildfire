import streamlit as st
import ee
import folium
from folium.plugins import Draw
import json
import st_folium


# Initialize Earth Engine
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()

st.title("🔥 Wildfire Detection (Draw AOI + Date Range)")

# --- Step 1: Create Folium map with Draw tool ---
m = folium.Map(location=[52.37, 4.90], zoom_start=8)

draw = Draw(
    draw_options={
        "polygon": True,
        "rectangle": True,
        "circle": False,
        "marker": False,
        "polyline": False,
    },
    edit_options={"edit": True, "remove": True},
)

draw.add_to(m)

# Display map and capture drawn shapes
output = st_folium.folium_static(m, width=700, height=500)

# --- Step 2: Extract GeoJSON from st.folium ---
geometry = None

if output and "last_active_drawing" in output and output["last_active_drawing"]:
    geometry = output["last_active_drawing"]["geometry"]
    st.success("AOI captured from map.")
else:
    st.info("Draw a polygon or rectangle on the map to define your AOI.")

# --- Step 3: Date range selection ---
st.subheader("Select date ranges")

pre_start = st.date_input("Pre-fire start date")
pre_end = st.date_input("Pre-fire end date")
post_start = st.date_input("Post-fire start date")
post_end = st.date_input("Post-fire end date")

# --- Helper functions ---
def landsat_sr(start, end, aoi):
    return (
        ee.ImageCollection("LANDSAT_LC09_C02_T1_L2")
        .filterDate(str(start), str(end))
        .filterBounds(aoi)
        .median()
    )

def add_nbr(img):
    nir = img.select("SR_B5")
    swir2 = img.select("SR_B7")
    nbr = nir.subtract(swir2).divide(nir.add(swir2)).rename("NBR")
    return img.addBands(nbr)

# --- Step 4: Run wildfire detection ---
if st.button("Run Wildfire Detection"):
    if geometry is None:
        st.error("Please draw an AOI on the map first.")
    else:
        try:
            aoi = ee.Geometry(geometry)

            st.write("Processing Landsat 9 images...")

            pre = add_nbr(landsat_sr(pre_start, pre_end, aoi)).select("NBR")
            post = add_nbr(landsat_sr(post_start, post_end, aoi)).select("NBR")

            dnbr = pre.subtract(post).rename("dNBR")

            wildfire_mask = dnbr.gt(0.1)

            detected = wildfire_mask.reduceRegion(
                reducer=ee.Reducer.anyNonZero(),
                geometry=aoi,
                scale=30
            ).getInfo()

            # --- Wildfire result ---
            if detected["dNBR"]:
                st.error("🔥 Wildfire detected in this area")
            else:
                st.success("✅ No wildfire detected")

            # --- Map visualization ---
            st.subheader("Burn Severity Map")

            vis = {
                "min": 0,
                "max": 0.8,
                "palette": ["white", "yellow", "orange", "red", "black"],
            }

            map2 = geemap.Map(center=[52.37, 4.90], zoom=8)
            map2.addLayer(dnbr, vis, "dNBR Burn Severity")
            map2.addLayer(aoi, {}, "AOI")

            map2.to_streamlit(height=600)

        except Exception as e:
            st.error(f"Error processing AOI: {e}")
