<<<<<<< HEAD
import streamlit as st
import cv2
import numpy as np
import base64
import os


# =========================
# BACKGROUND LOADER
# =========================
def get_base64_image(image_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, image_filename)

    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


# =========================
# DASHBOARD
# =========================
def show_dashboard():

    # =========================
    # BACKGROUND
    # =========================
    bg_base64 = get_base64_image("background.jpg")

    if bg_base64:
        bg_style = f"""
        .stApp {{
            background: url(data:image/jpeg;base64,{bg_base64});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        """
    else:
        bg_style = """
        .stApp {
            background: radial-gradient(circle at center, #0b0b0b, #1a0006);
        }
        """

    # =========================
    # FULL CSS FIX (CENTER CARD)
    # =========================
    st.markdown(f"""
    <style>

    {bg_style}

    /* DARK OVERLAY */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.6);
        z-index: 0;
    }}

    /* CENTER PAGE */
    .stApp {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* REMOVE FULL WIDTH STREAMLIT LAYOUT */
    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
    }}

    /* MAIN CARD */
    .block-container {{
        max-width: 520px !important;
        width: 100% !important;
        margin: auto !important;

        padding: 40px !important;

        background: rgba(15, 5, 5, 0.65) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;

        border-radius: 24px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;

        box-shadow: 0 25px 60px rgba(0,0,0,0.7);

        position: relative;
        z-index: 1;
    }}

    /* TEXT STYLE */
    h1, h2, h3, p, label {{
        color: #ffd6d6 !important;
    }}

    .title {{
        font-size: 40px;
        font-weight: 800;
        text-align: center;
        color: #ff3b3b;
        letter-spacing: 2px;
    }}

    .subtitle {{
        text-align: center;
        color: #ff9a9a;
        font-size: 12px;
        letter-spacing: 3px;
        margin-bottom: 20px;
    }}

    /* BUTTON STYLE */
    .stButton > button {{
        background: linear-gradient(135deg, #7a0019, #ff1a1a);
        color: white;
        border: none;
        border-radius: 10px;
        width: 100%;
        height: 45px;
        font-weight: bold;
        transition: 0.2s;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(255,0,0,0.4);
    }}

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # HEADER
    # =========================
    st.markdown(f"""
        <div class="title">VISION LAB</div>
        <div class="subtitle">IMAGE PROCESSING PLAYGROUND</div>
        <h3 style="text-align:center;">
            Welcome, {st.session_state.get("name", "Guest")}
        </h3>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # =========================
    # INPUT MODE
    # =========================
    mode = st.radio(
        "Pilih Gambar",
        ["Upload dari Galeri", "Ambil dari Kamera"],
        horizontal=True
    )

    file = None

    if mode == "Upload dari Galeri":
        file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])
    else:
        file = st.camera_input("Ambil foto")

    # =========================
    # PREVIEW + NEXT PAGE
    # =========================
    if file is not None:

        st.image(file, caption="Preview", use_container_width=True)

        if st.button("Lanjut ke Processing"):

            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            st.session_state.image = img
            st.session_state.page = "processing"
=======
import streamlit as st
import cv2
import numpy as np
import base64
import os


# =========================
# BACKGROUND LOADER
# =========================
def get_base64_image(image_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, image_filename)

    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


# =========================
# DASHBOARD
# =========================
def show_dashboard():

    # =========================
    # BACKGROUND
    # =========================
    bg_base64 = get_base64_image("background.jpg")

    if bg_base64:
        bg_style = f"""
        .stApp {{
            background: url(data:image/jpeg;base64,{bg_base64});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        """
    else:
        bg_style = """
        .stApp {
            background: radial-gradient(circle at center, #0b0b0b, #1a0006);
        }
        """

    # =========================
    # FULL CSS FIX (CENTER CARD)
    # =========================
    st.markdown(f"""
    <style>

    {bg_style}

    /* DARK OVERLAY */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.6);
        z-index: 0;
    }}

    /* CENTER PAGE */
    .stApp {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* REMOVE FULL WIDTH STREAMLIT LAYOUT */
    [data-testid="stAppViewContainer"] {{
        padding: 0 !important;
    }}

    /* MAIN CARD */
    .block-container {{
        max-width: 520px !important;
        width: 100% !important;
        margin: auto !important;

        padding: 40px !important;

        background: rgba(15, 5, 5, 0.65) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;

        border-radius: 24px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;

        box-shadow: 0 25px 60px rgba(0,0,0,0.7);

        position: relative;
        z-index: 1;
    }}

    /* TEXT STYLE */
    h1, h2, h3, p, label {{
        color: #ffd6d6 !important;
    }}

    .title {{
        font-size: 40px;
        font-weight: 800;
        text-align: center;
        color: #ff3b3b;
        letter-spacing: 2px;
    }}

    .subtitle {{
        text-align: center;
        color: #ff9a9a;
        font-size: 12px;
        letter-spacing: 3px;
        margin-bottom: 20px;
    }}

    /* BUTTON STYLE */
    .stButton > button {{
        background: linear-gradient(135deg, #7a0019, #ff1a1a);
        color: white;
        border: none;
        border-radius: 10px;
        width: 100%;
        height: 45px;
        font-weight: bold;
        transition: 0.2s;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(255,0,0,0.4);
    }}

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # HEADER
    # =========================
    st.markdown(f"""
        <div class="title">VISION LAB</div>
        <div class="subtitle">IMAGE PROCESSING PLAYGROUND</div>
        <h3 style="text-align:center;">
            Welcome, {st.session_state.get("name", "Guest")}
        </h3>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # =========================
    # INPUT MODE
    # =========================
    mode = st.radio(
        "Pilih Gambar",
        ["Upload dari Galeri", "Ambil dari Kamera"],
        horizontal=True
    )

    file = None

    if mode == "Upload dari Galeri":
        file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])
    else:
        file = st.camera_input("Ambil foto")

    # =========================
    # PREVIEW + NEXT PAGE
    # =========================
    if file is not None:

        st.image(file, caption="Preview", use_container_width=True)

        if st.button("Lanjut ke Processing"):

            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            st.session_state.image = img
            st.session_state.page = "processing"
>>>>>>> f68c69d576fe9758cf8b8df6a3666a7087a4465d
            st.rerun()