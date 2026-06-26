# 🔥 Wildfire Detection App  
A Streamlit application for detecting wildfire burn severity using **Landsat 9**, **Earth Engine**, and **dNBR (Differenced Normalized Burn Ratio)**.  
Users can **draw an Area of Interest (AOI)** directly on an interactive map using **st-folium**, select **pre-fire and post-fire date ranges**, and visualize burn severity results.

---

## 🚀 Features

### 🗺️ Draw AOI on the Map
- Uses **st-folium** with the **Draw plugin**  
- Supports polygons and rectangles  
- AOI is automatically captured as GeoJSON  

### 📅 Flexible Date Selection
- Choose **pre-fire** and **post-fire** date ranges  
- Landsat 9 imagery is filtered accordingly  

### 🔥 Wildfire Detection (dNBR)
The app computes:
- **NBR (Normalized Burn Ratio)** for pre-fire and post-fire images  
- **dNBR = NBR_before − NBR_after**  
- Burn severity classification based on USGS thresholds  

### 🛰️ Earth Engine Integration
- Uses **LANDSAT_LC09_C02_T1_L2**  
- Cloud masking and band selection handled automatically  
- Burn severity map rendered using **geemap**  

### 🌈 Burn Severity Visualization
- Color-coded dNBR map  
- AOI overlay  
- Interactive map inside Streamlit  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/jeggino/wildfire.git
cd wildfire
