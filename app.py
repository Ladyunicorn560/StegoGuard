import streamlit as st
import os
from PIL import Image

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="StegoGuard", layout="wide")

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🔐 StegoGuard")
st.subheader("Image-Based Data Exfiltration Detection System")

st.write(
    "This tool scans image files from a monitored folder and flags "
    "potential covert communication attempts where hidden data may "
    "be embedded inside images."
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------
MONITORED_FOLDER = "monitored_folder"
SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg")

# --------------------------------------------------
# Scan Button
# --------------------------------------------------
st.markdown("### 📁 Monitored Folder")
st.code(MONITORED_FOLDER)

scan_button = st.button("🔍 Scan Images")

# --------------------------------------------------
# Scan Logic
# --------------------------------------------------
if scan_button:
    if not os.path.exists(MONITORED_FOLDER):
        st.error("Monitored folder not found.")
    else:
        images = [
            f for f in os.listdir(MONITORED_FOLDER)
            if f.lower().endswith(SUPPORTED_FORMATS)
        ]

        if len(images) == 0:
            st.warning("No images found in monitored folder.")
        else:
            st.success(f"Scanned {len(images)} image(s).")

            col1, col2 = st.columns(2)

            for idx, img_name in enumerate(images):
                img_path = os.path.join(MONITORED_FOLDER, img_name)
                image = Image.open(img_path)

                # TEMP LOGIC (placeholder)
                prediction = "🟢 Clean"
                confidence = "N/A"

                with (col1 if idx % 2 == 0 else col2):
                    st.image(image, caption=img_name, use_column_width=True)
                    st.write(f"**Status:** {prediction}")
                    st.write(f"**Confidence:** {confidence}")
                    st.markdown("---")
