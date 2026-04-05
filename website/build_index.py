"""
build_index.py
--------------
Run ONCE to build the similarity index.
Picks 20 images per class from the train folder, extracts feature vectors
using the trained model's penultimate layer, and saves to image_index.json.

Run from your website folder:
    py -3.10 build_index.py

Output: image_index.json  (place this in the website folder)
"""

import os
import json
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_PATH  = "Trained_Model.h5"
TRAIN_DIR   = r"C:\Users\HP\Downloads\ML\eye_disease\train"
OUTPUT_JSON = "image_index.json"
IMAGES_PER_CLASS = 20
CLASS_NAMES = ['CNV', 'DME', 'DRUSEN', 'NORMAL']
IMG_SIZE    = (224, 224)

# ── Load model and build feature extractor ────────────────────────────────────
print("Loading model...")
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# model.layers[0] = MobilenetV3large (outputs 1000-dim vector)
# model.layers[1] = Dense(4)
# We use MobilenetV3large output directly as our feature vector
mobilenet_submodel = model.layers[0]
print(f"Feature extractor: {mobilenet_submodel.name} → output {mobilenet_submodel.output_shape}")

# ── Helper: extract feature vector from image path ────────────────────────────
def extract_features(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=IMG_SIZE)
    x   = tf.keras.utils.img_to_array(img)
    x   = np.expand_dims(x, axis=0)
    x   = preprocess_input(x)
    vec = mobilenet_submodel(x, training=False)
    return np.array(vec).flatten().tolist()

# ── Build index ───────────────────────────────────────────────────────────────
index = []

for cls in CLASS_NAMES:
    folder = os.path.join(TRAIN_DIR, cls)
    all_files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ]
    sampled = random.sample(all_files, min(IMAGES_PER_CLASS, len(all_files)))

    print(f"\nProcessing {cls} ({len(sampled)} images)...")
    for i, fname in enumerate(sampled):
        img_path = os.path.join(folder, fname)
        try:
            features = extract_features(img_path)
            parts    = fname.replace('.jpeg','').replace('.jpg','').split('-')
            patient_id = parts[1] if len(parts) > 1 else fname

            index.append({
                "class":      cls,
                "path":       img_path,
                "patient_id": patient_id,
                "features":   features,
            })
            print(f"  [{i+1}/{len(sampled)}] {fname} ✓")
        except Exception as e:
            print(f"  [{i+1}/{len(sampled)}] {fname} ✗ — {e}")

# ── Save ──────────────────────────────────────────────────────────────────────
with open(OUTPUT_JSON, 'w') as f:
    json.dump(index, f)

print(f"\n✅ Done! Saved {len(index)} entries to {OUTPUT_JSON}")
print("   Place image_index.json in your website/ folder and restart the app.")