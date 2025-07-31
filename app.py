import streamlit as st

st.set_page_config(page_title="NDVI Calculator", layout="centered")

st.title("🌱 NDVI Calculator")

st.markdown("""
This tool calculates the **Normalized Difference Vegetation Index (NDVI)** from Red and NIR band values.

**Formula:**  
📘 `NDVI = (NIR - Red) / (NIR + Red)`  
""")

red = st.number_input("Enter Red band value:", min_value=0.0, format="%.2f")
nir = st.number_input("Enter NIR band value:", min_value=0.0, format="%.2f")

if st.button("Calculate NDVI"):
    if (nir + red) == 0:
        st.warning("NIR + Red cannot be zero.")
    else:
        ndvi = (nir - red) / (nir + red)
        st.success(f"✅ NDVI: {ndvi:.3f}")

        if ndvi < 0:
            level = "Water or clouds"
        elif ndvi < 0.2:
            level = "Barren or urban area"
        elif ndvi < 0.5:
            level = "Sparse vegetation"
        else:
            level = "Healthy vegetation"

        st.markdown(f"**Vegetation health:** {level}")

st.markdown("---")
st.markdown("Made with ❤️ by Surabhi Gupta · [GitHub]https://github.com/Surabhi3011")
