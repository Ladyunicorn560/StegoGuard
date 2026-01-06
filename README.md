# StegoGuard
Image-based data exfiltration detection system


StegoGuard is a security-oriented image analysis tool designed to **assess the risk of hidden data embedding inside digital images**.  
It uses **deep learning–based feature analysis**, explainable risk scoring, and a user-friendly web interface built with Streamlit.

⚠️ This project is designed as a **risk assessment and analysis sandbox**, not a payload extraction or malware execution tool.

---

## 🚀 Key Features

- 📤 **Single & Batch Image Upload**
  - Upload one or multiple images for analysis
- 🧠 **Deep Learning–Based Feature Analysis**
  - CNN feature extraction (TensorFlow backend)
- 🎚️ **Configurable Detection Sensitivity**
  - Low / Medium / High sensitivity modes
- 📊 **Risk-Based Classification**
  - Low Risk / Medium Risk / High Risk (heuristic + ML)
- 🧾 **Explainable Results**
  - Human-readable explanations for each prediction
- 📈 **Scan History & Dashboard**
  - Metrics, pie charts, and audit log of all scans
- 🔒 **Safe by Design**
  - No decoding, no payload execution, no file system monitoring

---

## 🏗️ Detection Pipeline

1. **Image Ingestion**  
   User uploads one or more images via the web interface.

2. **Preprocessing**  
   Images are normalized and resized for feature extraction.

3. **Feature Extraction**  
   Deep CNN features are extracted to capture subtle visual and statistical patterns.

4. **Risk Scoring**  
   Model confidence and heuristics are combined to estimate potential covert embedding risk.

5. **Decision & Explanation**  
   The system outputs a risk level along with a natural-language explanation.

---

## 🎚️ Detection Sensitivity

The sensitivity slider allows users to control how aggressively the system flags potential risks:

- **Low Sensitivity**  
  Conservative detection, fewer alerts (reduces false positives)

- **Medium Sensitivity**  
  Balanced detection (default)

- **High Sensitivity**  
  Aggressive detection, higher likelihood of flagging subtle anomalies

This reflects real-world security tools where alert thresholds are adjustable.

---


## 🔒 Security & Safety Considerations

- StegoGuard **does not decode, extract, or execute hidden payloads**
- All analysis is performed on pixel-level data only
- No system-level access or file monitoring is required
- Safe to use on personal machines

---

## ⚠️ Limitations

- This is a **risk assessment tool**, not a definitive steganography detector
- Does not guarantee detection of highly optimized steganographic payloads
- Intended for research, education, and demonstration purposes

---

## 🛠️ Tech Stack

- **Python**
- **TensorFlow / Keras**
- **Streamlit**
- **PIL / Matplotlib / Pandas**

---

## 📌 Future Improvements

- Side-by-side image comparison mode
- Confidence delta visualization
- Noise sensitivity heatmaps
- Video and frame-based analysis
- Model fine-tuning with labeled steganography datasets

---

