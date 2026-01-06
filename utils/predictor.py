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
    Returns: (label, confidence)
    """

    image = image.convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    features = model.predict(img_array, verbose=0)

    # --------------------------------------------------
    # TEMP SIMULATION LOGIC
    # (until stego-trained model is plugged in)
    # --------------------------------------------------
    score = float(np.mean(features))

    if score > 0.35:
        return "⚠️ Suspicious", round(score * 100, 2)
    else:
        return "🟢 Clean", round((1 - score) * 100, 2)
