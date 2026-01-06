import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
from utils.predictor import predict_image, explain_prediction
from datetime import datetime
import pandas as pd

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="StegoGuard", layout="wide")

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🔐 StegoGuard")
st.subheader("Detects Hidden Data Inside Images to Prevent Data Leaks")

st.write(
    "StegoGuard is a security-oriented image analysis tool designed to "
    "detect potential covert data embedding using deep learning–based "
    "feature analysis and risk scoring."
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
        <div style="text-align:center; padding:12px; border-radius:12px;
                    background-color:#1f2933;">
            <h2>{icon}</h2>
            <p style="font-size:14px;">{label}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# LAYER 2: Detection Sensitivity
# --------------------------------------------------
st.markdown("## 🎚️ Detection Sensitivity")

sensitivity = st.slider(
    "Adjust detection sensitivity (higher = more aggressive)",
    min_value=1,
    max_value=3,
    value=2
)

if sensitivity == 1:
    st.caption("🔵 Low sensitivity: Conservative alerts")
elif sensitivity == 2:
    st.caption("🟡 Medium sensitivity: Balanced detection")
else:
    st.caption("🔴 High sensitivity: Aggressive risk detection")

# --------------------------------------------------
# LAYER 3: Upload & Scan Images (MULTI-FILE)
# --------------------------------------------------
st.markdown("## 🧪 Upload Images for Analysis")

uploaded_files = st.file_uploader(
    "Upload one or more images (PNG / JPG / JPEG)",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.markdown("### 🔎 Detection Results")

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)

        st.image(image, caption=uploaded_file.name, width=300)

        # ---- Prediction ----
        status, confidence = predict_image(image)

        # ---- Sensitivity Adjustment ----
        if sensitivity == 1 and "Medium" in status:
            status = "🟢 Low Risk"
        elif sensitivity == 3 and "Low" in status:
            status = "🟠 Medium Risk"

        explanation = explain_prediction(status, confidence)

        st.write(f"**Status:** {status}")
        st.write(f"**Confidence:** {confidence:.2f}%")
        st.caption(f"🧠 {explanation}")

        # ---- Log to history ----
        st.session_state.scan_history.append({
            "Image": uploaded_file.name,
            "Status": status,
            "Confidence (%)": round(confidence, 2),
            "Explanation": explanation,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Source": "Upload"
        })

        st.markdown("---")

# --------------------------------------------------
# LAYER 4: Scan History Dashboard
# --------------------------------------------------
st.markdown("## 🧾 Scan History")

if len(st.session_state.scan_history) == 0:
    st.info("No scans performed yet.")
else:
    df = pd.DataFrame(st.session_state.scan_history)

    total = len(df)
    clean = df["Status"].str.contains("Low").sum()
    risky = total - clean

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scans", total)
    col2.metric("🟢 Low Risk", clean)
    col3.metric("⚠️ Risky", risky)

    fig, ax = plt.subplots()
    ax.pie(
        [clean, risky],
        labels=["Low Risk", "Risky"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

    st.markdown("### 📋 Detailed Scan Log")
    st.dataframe(df, use_container_width=True)
