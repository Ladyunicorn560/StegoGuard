import streamlit as st
import os
from PIL import Image
import matplotlib.pyplot as plt

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
            clean_count = 0
            suspicious_count = 0

            results = []

            for img_name in images:
                img_path = os.path.join(MONITORED_FOLDER, img_name)
                image = Image.open(img_path)
                width, height = image.size

                # ------------------------------------------
                # TEMP SECURITY HEURISTIC (Placeholder)
                # ------------------------------------------
                if width * height > 2_000_000:  # very large image
                    status = "⚠️ Suspicious"
                    suspicious_count += 1
                else:
                    status = "🟢 Clean"
                    clean_count += 1

                results.append((img_name, image, status))

            # --------------------------------------------------
            # DASHBOARD METRICS
            # --------------------------------------------------
            st.markdown("## 📊 Scan Summary")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Images", len(images))
            col2.metric("🟢 Clean", clean_count)
            col3.metric("⚠️ Suspicious", suspicious_count)

            # --------------------------------------------------
            # PIE CHART
            # --------------------------------------------------
            fig, ax = plt.subplots()
            ax.pie(
                [clean_count, suspicious_count],
                labels=["Clean", "Suspicious"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax.axis("equal")
            st.pyplot(fig)

            st.markdown("---")

            # --------------------------------------------------
            # IMAGE RESULTS
            # --------------------------------------------------
            st.markdown("## 🖼️ Image Analysis Results")

            colA, colB = st.columns(2)

            for idx, (name, image, status) in enumerate(results):
                with (colA if idx % 2 == 0 else colB):
                    st.image(image, caption=name, width=400)
                    st.write(f"**Status:** {status}")
                    st.markdown("---")
