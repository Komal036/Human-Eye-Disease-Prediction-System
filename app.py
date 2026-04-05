import streamlit as st
import tensorflow as tf
import numpy as np
from recommendation import cnv, dme, drusen, normal
import tempfile
import os


# ── Model Prediction ──────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("new_trained_eye_cnn.keras")
    return model

def model_prediction(test_image_path):
    model = load_model()
    img = tf.keras.utils.load_img(test_image_path, target_size=(128, 128))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 255.0  # CNN uses simple normalization
    predictions = model.predict(x)
    return np.argmax(predictions)


# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retinal OCT Analysis",
    page_icon="👁️",
    layout="wide"
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Identification"])


# ── Home Page ─────────────────────────────────────────────────────────────────
if app_mode == "Home":
    st.markdown("""
    ## 👁️ OCT Retinal Analysis Platform

    #### Welcome to the Retinal OCT Analysis Platform

    **Optical Coherence Tomography (OCT)** is a powerful imaging technique that provides
    high-resolution cross-sectional images of the retina, allowing for early detection and
    monitoring of various retinal diseases. Each year, over **30 million OCT scans** are
    performed, aiding in the diagnosis and management of eye conditions that can lead to
    vision loss.

    ---

    #### Key Features of the Platform

    - 🤖 **Automated Image Analysis** — Custom CNN model classifies OCT images into:
      **Normal**, **CNV**, **DME**, and **Drusen**
    - 🖼️ **Cross-Sectional Retinal Imaging** — Examine high-quality images showcasing
      both normal retinas and various pathologies
    - ⚡ **Streamlined Workflow** — Upload, analyze, and review OCT scans in a few easy steps

    ---

    #### Model Performance

    | Class | Precision | Recall | F1-Score |
    |-------|-----------|--------|----------|
    | CNV | 0.97 | 0.97 | 0.97 |
    | DME | 0.93 | 0.96 | 0.94 |
    | DRUSEN | 0.87 | 0.79 | 0.83 |
    | NORMAL | 0.98 | 0.99 | 0.98 |
    | **Overall** | **0.96** | **0.96** | **0.96** |

    ---

    #### Understanding Retinal Diseases through OCT

    | Disease | Description |
    |---------|-------------|
    | **CNV** | Choroidal Neovascularization — neovascular membrane with subretinal fluid |
    | **DME** | Diabetic Macular Edema — retinal thickening with intraretinal fluid |
    | **Drusen** | Early AMD — presence of multiple drusen deposits |
    | **Normal** | Preserved foveal contour, absence of fluid or edema |

    ---

    #### Get Started
    👉 Navigate to **Disease Identification** in the sidebar to upload your OCT scan.
    """)


# ── About Page ────────────────────────────────────────────────────────────────
elif app_mode == "About":
    st.header("About")
    st.markdown("""
    #### About Dataset

    Retinal optical coherence tomography (OCT) is an imaging technique used to capture
    high-resolution cross sections of the retinas of living patients. Approximately
    **30 million OCT scans** are performed each year, and the analysis and interpretation
    of these images takes up a significant amount of time.

    - **(Far left)** Choroidal neovascularization (CNV) with neovascular membrane and
      associated subretinal fluid
    - **(Middle left)** Diabetic macular edema (DME) with retinal-thickening-associated
      intraretinal fluid
    - **(Middle right)** Multiple drusen present in early AMD
    - **(Far right)** Normal retina with preserved foveal contour and absence of any
      retinal fluid/edema

    ---

    #### Dataset Details

    - **84,495** X-Ray images (JPEG format)
    - **4 categories** — NORMAL, CNV, DME, DRUSEN
    - Images sourced from: UC San Diego, California Retinal Research Foundation,
      Shanghai First People's Hospital, Beijing Tongren Eye Center (2013–2017)

    ---

    #### Model

    This platform uses a **custom CNN** trained from scratch on the OCT dataset,
    achieving **96% test accuracy** across all four retinal disease categories.

    ---

    #### Disclaimer
    > ⚠️ This tool is for **educational and research purposes only**. It is not a
    > substitute for professional medical diagnosis. Always consult a qualified
    > ophthalmologist for clinical decisions.
    """)


# ── Disease Identification Page ───────────────────────────────────────────────
elif app_mode == "Disease Identification":
    st.header("👁️ Retinal OCT Disease Identification")
    st.markdown("Upload an OCT retinal scan image and click **Predict** to identify the condition.")

    test_image = st.file_uploader("Upload OCT Image (JPG/PNG):", type=["jpg", "jpeg", "png"])

    if test_image is not None:
        st.image(test_image, caption="Uploaded OCT Scan", use_column_width=False, width=400)

    if st.button("🔍 Predict") and test_image is not None:
        with st.spinner("Analyzing OCT scan... Please wait ⏳"):
            suffix = os.path.splitext(test_image.name)[-1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                tmp_file.write(test_image.read())
                temp_file_path = tmp_file.name

            result_index = model_prediction(temp_file_path)
            os.unlink(temp_file_path)

        class_name = ['CNV', 'DME', 'DRUSEN', 'NORMAL']
        result = class_name[result_index]

        color_map = {"CNV": "🔴", "DME": "🟠", "DRUSEN": "🟡", "NORMAL": "🟢"}
        st.success(f"{color_map[result]} **Prediction: {result}**")

        with st.expander("📋 Learn More & Recommendations", expanded=True):
            if result_index == 0:
                st.write("*OCT scan showing CNV with subretinal fluid.*")
                st.markdown(cnv)
            elif result_index == 1:
                st.write("*OCT scan showing DME with retinal thickening and intraretinal fluid.*")
                st.markdown(dme)
            elif result_index == 2:
                st.write("*OCT scan showing drusen deposits in early AMD.*")
                st.markdown(drusen)
            elif result_index == 3:
                st.write("*OCT scan showing a normal retina with preserved foveal contour.*")
                st.markdown(normal)

    elif st.button("🔍 Predict") and test_image is None:
        st.warning("⚠️ Please upload an OCT image first!")