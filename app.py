import streamlit as st
import pandas as pd

st.set_page_config(page_title="NDVI Calculator by Surabhi", layout="centered")

st.title("🌿 NDVI Calculator")
st.markdown("Analyze vegetation health from Red and NIR band values.")

st.markdown("### 🧮 Single NDVI Value")
st.info("Use this for quick checks using individual Red and NIR values.")

col1, col2 = st.columns(2)
with col1:
    red = st.number_input("🔴 Red band value", min_value=0.0, format="%.2f", key="red_input")
with col2:
    nir = st.number_input("🌕 NIR band value", min_value=0.0, format="%.2f", key="nir_input")

def interpret_ndvi(ndvi):
    if ndvi < 0:
        return "Water or Cloud"
    elif ndvi < 0.1:
        return "Built-up or Snow"
    elif ndvi < 0.2:
        return "Bare Soil"
    elif ndvi < 0.3:
        return "Shrubs"
    elif ndvi < 0.5:
        return "Grassland or Sparse Vegetation"
    elif ndvi < 0.7:
        return "Forest or Dense Vegetation"
    else:
        return "Tropical Dense Forest"

if st.button("📊 Calculate NDVI", key="manual_calc"):
    if red + nir == 0:
        st.warning("Red + NIR cannot be zero.")
    else:
        ndvi = (nir - red) / (nir + red)
        result = interpret_ndvi(ndvi)
        st.success(f"NDVI: **{ndvi:.3f}**")
        st.markdown(f"**Vegetation Health:** {result}")

# Divider
st.markdown("---")

st.markdown("### 📂 Upload CSV File (Batch NDVI)")
st.info("Upload a CSV file with two columns: `red` and `nir` (case-insensitive).")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.lower()

        if 'red' in df.columns and 'nir' in df.columns:
            df = df[['red', 'nir']].copy()
            df['NDVI'] = (df['nir'] - df['red']) / (df['nir'] + df['red'])
            df['NDVI'] = df['NDVI'].round(3)
            df['Vegetation Class'] = df['NDVI'].apply(interpret_ndvi)

            st.success(f"✅ Processed {len(df)} records.")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Result CSV", csv, "ndvi_output.csv", "text/csv")
        else:
            st.error("CSV must contain columns named 'red' and 'nir'.")
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Footer
st.markdown("---")
st.markdown("""
Made with ❤️ by **Surabhi Gupta**  
📍 [LinkedIn](https://www.linkedin.com/in/surabhiguptageo/) · 📰 [Substack](https://geocloudinsights.substack.com)
""", unsafe_allow_html=True)
