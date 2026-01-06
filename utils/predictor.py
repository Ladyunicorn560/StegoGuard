import tensorflow as tf
import numpy as np
from PIL import Image

# --------------------------------------------------
# Load pretrained model (for now, generic CNN)
# --------------------------------------------------
model = tf.keras.applications.EfficientNetB0(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    input_shape=(224, 224, 3)
)

# --------------------------------------------------
# Simple classification head (simulated)
# --------------------------------------------------
def predict_image(image: Image.Image):
    """
    Takes PIL Image
    Returns: (label, confidence_percentage)
    """

    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    features = model.predict(img_array, verbose=0)

    # Normalize feature score to 0–1 range
    raw_score = float(np.mean(features))

    # Sigmoid-style normalization (simple & safe)
    normalized_score = 1 / (1 + np.exp(-raw_score))

    confidence = normalized_score * 100

    if confidence >= 75:
        return "🔴 High Risk", round(confidence, 2)
    elif confidence >= 60:
        return "🟠 Medium Risk", round(confidence, 2)
    else:
        return "🟢 Low Risk", round(100 - confidence, 2)


