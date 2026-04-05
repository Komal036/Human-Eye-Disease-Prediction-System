import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input
import numpy as np
import os
import json
import random
import tempfile
from recommendation import cnv, dme, drusen, normal

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_PATH  = "Trained_Model.h5"
INDEX_PATH  = "image_index.json"
CLASS_NAMES = ['CNV', 'DME', 'DRUSEN', 'NORMAL']
IMG_SIZE    = (224, 224)

SOURCES = {
    'CNV': {
        'name': 'National Eye Institute (NEI) — U.S. National Institutes of Health',
        'url':  'https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/macular-degeneration',
    },
    'DME': {
        'name': 'National Eye Institute (NEI) — U.S. National Institutes of Health',
        'url':  'https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/diabetic-retinopathy',
    },
    'DRUSEN': {
        'name': 'American Academy of Ophthalmology (AAO)',
        'url':  'https://www.aao.org/eye-health/diseases/what-are-drusen',
    },
    'NORMAL': {
        'name': 'Mayo Clinic',
        'url':  'https://www.mayoclinic.org/diseases-conditions/diabetic-retinopathy/symptoms-causes/syc-20371611',
    },
}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OCT Retinal Analysis Platform",
    page_icon="👁️",
    layout="wide",
)

# ── Cached loaders ────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model…")
def load_model():
    return tf.keras.models.load_model(MODEL_PATH, compile=False)

@st.cache_resource(show_spinner="Loading similarity index…")
def load_index():
    if not os.path.exists(INDEX_PATH):
        return None
    with open(INDEX_PATH, 'r') as f:
        return json.load(f)

# ── Prediction ────────────────────────────────────────────────────────────────
def model_prediction(img_path):
    model = load_model()
    img   = tf.keras.utils.load_img(img_path, target_size=IMG_SIZE)
    x     = tf.keras.utils.img_to_array(img)
    x     = np.expand_dims(x, axis=0)
    x     = preprocess_input(x)
    preds = model.predict(x, verbose=0)
    return int(np.argmax(preds)), preds[0]

# ── Feature extraction for uploaded image ────────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_feature_extractor():
    model = load_model()
    return model.layers[0]   # MobilenetV3large submodel

def extract_features(img_path):
    mobilenet = get_feature_extractor()
    img = tf.keras.utils.load_img(img_path, target_size=IMG_SIZE)
    x   = tf.keras.utils.img_to_array(img)
    x   = np.expand_dims(x, axis=0)
    x   = preprocess_input(x)
    vec = mobilenet(x, training=False)
    return np.array(vec).flatten()

# ── Cosine similarity ─────────────────────────────────────────────────────────
def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

# ── Get top-k similar images from index ──────────────────────────────────────
def get_similar_images(predicted_class, query_features, top_k=2):
    index = load_index()

    # Fallback: random from train folder if no index
    if index is None:
        return []

    # Filter to same class only
    candidates = [e for e in index if e['class'] == predicted_class]

    # Score by cosine similarity
    scored = []
    for entry in candidates:
        sim = cosine_similarity(query_features, entry['features'])
        scored.append((sim, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [entry for _, entry in scored[:top_k]]

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox(
    "Select Page", ["Home", "About", "Disease Identification"]
)

# ═════════════════════════════════════════════════════════════════════════════
#  HOME
# ═════════════════════════════════════════════════════════════════════════════
if app_mode == "Home":
    st.markdown("""
    ## **OCT Retinal Analysis Platform**

#### **Welcome to the Retinal OCT Analysis Platform**

**Optical Coherence Tomography (OCT)** is a powerful imaging technique that provides
high-resolution cross-sectional images of the retina, allowing for early detection and
monitoring of various retinal diseases. Each year, over 30 million OCT scans are
performed, aiding in the diagnosis and management of eye conditions that can lead to
vision loss, such as choroidal neovascularization (CNV), diabetic macular edema (DME),
and age-related macular degeneration (AMD).

---

#### **Key Features of the Platform**

- **Automated Image Analysis**: Uses MobileNetV3Large trained on 84,495 OCT images to
  classify scans into **Normal**, **CNV**, **DME**, and **Drusen**.
- **Evidence-Based Recommendations**: Each prediction is paired with clinical management
  guidelines sourced from the NEI, AAO, and Mayo Clinic.
- **Similar Case Reference**: Displays 2 matched training cases ranked by cosine
  similarity of CNN feature vectors — the most visually similar confirmed diagnoses.

---

#### **Understanding Retinal Diseases through OCT**

1. **Choroidal Neovascularization (CNV)** — Neovascular membrane with subretinal fluid
2. **Diabetic Macular Edema (DME)** — Retinal thickening with intraretinal fluid
3. **Drusen (Early AMD)** — Multiple drusen deposits in the macula
4. **Normal Retina** — Preserved foveal contour, no fluid or edema

---

#### **Get Started**
Navigate to **Disease Identification** in the sidebar to upload an OCT scan.
    """)

# ═════════════════════════════════════════════════════════════════════════════
#  ABOUT
# ═════════════════════════════════════════════════════════════════════════════
elif app_mode == "About":
    st.header("About")
    st.markdown("""
#### About Dataset
Retinal optical coherence tomography (OCT) is an imaging technique used to capture
high-resolution cross sections of the retinas of living patients. Approximately
30 million OCT scans are performed each year.

The dataset contains **84,495 OCT images** (JPEG) split into train / test / val
folders across four categories: **CNV, DME, DRUSEN, NORMAL**.

Images were collected from the Shiley Eye Institute (UCSD), California Retinal
Research Foundation, Shanghai First People's Hospital, and Beijing Tongren Eye
Center (2013–2017). Each image was verified by a tiered grading system including
senior retinal specialists with 20+ years of experience.

---

#### Model
- Architecture: **MobileNetV3Large** (pretrained on ImageNet, fine-tuned on OCT data)
- Input: 224 × 224 RGB
- Preprocessing: `tf.keras.applications.mobilenet_v3.preprocess_input`
- Similar case retrieval: Cosine similarity on CNN penultimate-layer feature vectors
    """)

# ═════════════════════════════════════════════════════════════════════════════
#  DISEASE IDENTIFICATION
# ═════════════════════════════════════════════════════════════════════════════
elif app_mode == "Disease Identification":
    st.header("👁️ Retinal OCT Disease Identification")
    st.write("Upload an OCT scan and click **Predict** to analyse it.")

    test_image = st.file_uploader("Upload your OCT Image:", type=["jpg", "jpeg", "png"])

    if test_image is not None:
        st.image(test_image, caption="Uploaded OCT Scan", use_column_width=False, width=400)

    if st.button("Predict") and test_image is not None:

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(test_image.read())
            temp_path = tmp.name

        with st.spinner("Analysing OCT scan…"):
            result_index, probs   = model_prediction(temp_path)
            query_features        = extract_features(temp_path)

        predicted_class = CLASS_NAMES[result_index]
        confidence      = float(probs[result_index]) * 100

        # ── Result banner ─────────────────────────────────────────────────────
        color_map = {'CNV': '🔴', 'DME': '🟠', 'DRUSEN': '🟡', 'NORMAL': '🟢'}
        st.success(
            f"{color_map[predicted_class]}  Model predicts: **{predicted_class}**  "
            f"— Confidence: **{confidence:.1f}%**"
        )

        # ── Class probabilities ───────────────────────────────────────────────
        st.markdown("#### Class Probabilities")
        for i, cls in enumerate(CLASS_NAMES):
            st.progress(float(probs[i]), text=f"{cls}: {probs[i]*100:.1f}%")

        st.divider()

        # ── Section 1: Clinical Recommendation ───────────────────────────────
        st.markdown("### 📋 Clinical Recommendation")

        rec_map  = {'CNV': cnv, 'DME': dme, 'DRUSEN': drusen, 'NORMAL': normal}
        desc_map = {
            'CNV':    "OCT scan showing *CNV with subretinal fluid.*",
            'DME':    "OCT scan showing *DME with retinal thickening and intraretinal fluid.*",
            'DRUSEN': "OCT scan showing *drusen deposits in early AMD.*",
            'NORMAL': "OCT scan showing a *normal retina with preserved foveal contour.*",
        }

        st.write(desc_map[predicted_class])
        st.markdown(rec_map[predicted_class])

        src = SOURCES[predicted_class]
        st.markdown(
            f"📖 **Further Reading — {src['name']}**  \n"
            f"[{src['url']}]({src['url']})"
        )

        st.divider()

        # ── Section 2: Similar Cases ──────────────────────────────────────────
        st.markdown("### 🗂️ Similar Cases from Patient Records")
        st.caption(
            f"The following OCT scans are the most visually similar confirmed "
            f"**{predicted_class}** cases from our training database, ranked by "
            f"cosine similarity of CNN feature vectors."
        )

        similar = get_similar_images(predicted_class, query_features, top_k=2)

        if similar:
            cols = st.columns(2)
            for col, entry in zip(cols, similar):
                with col:
                    img_path = entry['path']
                    pid      = entry['patient_id']
                    if os.path.exists(img_path):
                        with open(img_path, 'rb') as f:
                            img_bytes = f.read()
                        st.image(
                            img_bytes,
                            caption=f"Confirmed {predicted_class} — Patient ID: {pid}",
                            use_column_width=True,
                        )
                    else:
                        st.warning(f"Image not found: {img_path}")
        else:
            st.info(
                "Similarity index not found. Run `build_index.py` once to enable "
                "feature-based similar case retrieval."
            )

        # Cleanup
        try:
            os.remove(temp_path)
        except Exception:
            pass