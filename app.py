import streamlit as st
import os
from PIL import Image
import matplotlib.pyplot as plt
from utils.predictor import predict_image, explain_prediction
from datetime import datetime

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="StegoGuard", layout="wide")

# --------------------------------------------------
# Session state (MUST be at top)
# --------------------------------------------------
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🔐 StegoGuard")
st.subheader("Detects Hidden Data Inside Images to Prevent Data Leaks")

st.write(
    "This tool scans image files from a monitored folder and flags "
    "potential covert communication attempts where hidden data may "
    "be embedded inside images."
)

# --------------------------------------------------
# LAYER 1: Detection Pipeline
# --------------------------------------------------
st.markdown("## 🔍 Detection Pipeline")

pipeline_cols = st.columns(5)

steps = [
    ("📥", "Image Ingestion"),
    ("🧹", "Preprocessing"),
    ("🧠", "Feature Extraction"),
    ("📊", "Risk Scoring"),
    ("🚨", "Decision")
]

for col, (icon, label) in zip(pipeline_cols, steps):
    col.markdown(
        f"""
        <div style="text-align:center; padding:10px; border-radius:10px;
                    background-color:#1f2933;">
            <h2>{icon}</h2>
            <p style="font-size:14px;">{label}</p>
        </div>
        """,
        unsafe_allow_html=True
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

                status, confidence = predict_image(image)
                explanation = explain_prediction(status, confidence)


                if "High" in status or "Medium" in status:
                    suspicious_count += 1
                else:
                    clean_count += 1

                results.append({
                "image": img_name,
                "status": status,
                "confidence": confidence,
                "explanation": explanation,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
})


            # --------------------------------------------------
            # Dashboard Metrics
            # --------------------------------------------------
            st.markdown("## 📊 Scan Summary")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Images", len(images))
            col2.metric("🟢 Clean", clean_count)
            col3.metric("⚠️ Risky", suspicious_count)

            # --------------------------------------------------
            # Pie Chart
            # --------------------------------------------------
            fig, ax = plt.subplots()
            ax.pie(
                [clean_count, suspicious_count],
                labels=["Clean", "Risky"],
                autopct="%1.1f%%",
                startangle=90
            )
            ax.axis("equal")
            st.pyplot(fig)

            st.markdown("---")

            # --------------------------------------------------
            # Image Results
            # --------------------------------------------------
            st.markdown("## 🖼️ Image Analysis Results")

            colA, colB = st.columns(2)

            for idx, r in enumerate(results):
                with (colA if idx % 2 == 0 else colB):
                    img = Image.open(os.path.join(MONITORED_FOLDER, r["image"]))
                    st.image(img, caption=r["image"], width=400)
                    st.write(f"**Status:** {r['status']}")
                    st.write(f"**Confidence:** {r['confidence']:.2f}%")
                    st.caption(f"🧠 {r['explanation']}")

                    st.markdown("---")

            # --------------------------------------------------
            # LAYER 2: Scan History Logging
            # --------------------------------------------------
            st.session_state.scan_history.extend(results)

# --------------------------------------------------
# LAYER 2: Scan History Table
# --------------------------------------------------
st.markdown("## 🧾 Scan History")

if len(st.session_state.scan_history) == 0:
    st.info("No scans performed yet.")
else:
    st.dataframe(
        st.session_state.scan_history,
        use_container_width=True
    )
