import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import base64
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Image Processing", layout="wide")

# =========================
# BACKGROUND FUNCTION
# =========================
def get_base64_image(image_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, image_filename)

    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# =========================
# GET IMAGE
# =========================
def get_image():
    if "image" not in st.session_state:
        st.error("Belum ada gambar dari dashboard")
        st.stop()
    return st.session_state.image

# =========================
# CONVERTER
# =========================
def to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def to_cv(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# =========================
# HISTOGRAM
# =========================
def show_histogram(img, title):
    fig, ax = plt.subplots(figsize=(4, 2))
    colors = ("b", "g", "r")

    for i, c in enumerate(colors):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        ax.plot(hist, color=c, linewidth=1)

    ax.set_title(title, fontsize=9, color="#ffd6d6")
    ax.set_xlim([0, 256])

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.tick_params(axis="both", length=0, labelsize=7, colors="#ffd6d6")

    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

# =========================
# PROCESSING PAGE
# =========================
def show_processing():
    # BACKGROUND STYLE
    bg_base64 = get_base64_image("background.jpg")

    if bg_base64:
        bg_style = f"""
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.65)),
                        url(data:image/jpeg;base64,{bg_base64}) !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        """
    else:
        bg_style = """
        .stApp {
            background: radial-gradient(circle at 50% 30%, #200202 0%, #050000 100%) !important;
        }
        """

    # CSS
    st.markdown(f"""
    <style>
    {bg_style}
    .glass {{
        background: rgba(25, 3, 3, 0.55);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border-radius: 18px;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }}
    h1, h2, h3, label {{ color: #ffd6d6 !important; }}
    section[data-testid="stSidebar"] {{ background: rgba(10,0,0,0.88); }}
    [data-testid="column"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
    *::before, *::after {{ content: none !important; }}
    </style>
    """, unsafe_allow_html=True)

    img_original = get_image()
    pil_img = to_pil(img_original)

    # SIDEBAR
    st.sidebar.title("CONTROL PANEL")
    if st.sidebar.button("Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()

    # OPENCV BUTTONS
    st.sidebar.subheader("OpenCV Features")
    if "opencv_choice" not in st.session_state:
        st.session_state.opencv_choice = "None"

    def set_effect(val):
        st.session_state.opencv_choice = val

    opencv_choice = st.session_state.opencv_choice
    for effect in ["None", "Grayscale", "Blur", "Edge"]:
        st.sidebar.button(effect, use_container_width=True,
            type="primary" if opencv_choice == effect else "secondary",
            on_click=set_effect, args=(effect,))

    # PILLOW SETTINGS
    st.sidebar.subheader("Pillow Features")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
    color = st.sidebar.slider("Color", 0.5, 2.0, 1.0)
    sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0)
    rotate = st.sidebar.selectbox("Rotate", [0, 90, 180, 270])
    resize = st.sidebar.slider("Resize %", 50, 150, 100)
    download_format = st.sidebar.selectbox("Download", ["JPG", "PNG"])

    # PROCESS IMAGE
    img = pil_img
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(color)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = img.rotate(rotate, expand=True)
    if resize != 100:
        w, h = img.size
        img = img.resize((int(w * resize / 100), int(h * resize / 100)))

    img_edit = to_cv(img)

    # OPENCV EFFECTS
    if opencv_choice == "Grayscale":
        img_edit = cv2.cvtColor(img_edit, cv2.COLOR_BGR2GRAY)
        img_edit = cv2.cvtColor(img_edit, cv2.COLOR_GRAY2BGR)
    elif opencv_choice == "Blur":
        img_edit = cv2.GaussianBlur(img_edit, (11, 11), 0)
    elif opencv_choice == "Edge":
        gray = cv2.cvtColor(img_edit, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        img_edit = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # TITLE
    st.markdown("<h1 style='text-align:center;'>IMAGE PROCESSING</h1>", unsafe_allow_html=True)

    # DISPLAY
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Original Image")
        st.image(img_original, use_container_width=True)
        show_histogram(img_original, "Original")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Processed Image")
        st.image(img_edit, use_container_width=True)
        show_histogram(img_edit, "Processed")
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # DOWNLOAD
    # =========================
    ext = ".jpg" if download_format == "JPG" else ".png"
    success, buffer = cv2.imencode(ext, img_edit)
    
    if success:
        st.sidebar.markdown("---")
        
        # 1. Tombol Download
        st.sidebar.download_button(
            "Download Image",
            data=buffer.tobytes(),
            file_name=f"result{ext}",
            mime="image/jpeg" if download_format == "JPG" else "image/png",
            use_container_width=True
        )
        
        # 2. Tombol Selesai (Logout dan Bersihkan State)
        if st.sidebar.button("Selesai", use_container_width=True, key="done_btn"):
            # Hapus data gambar dari memori
            if "image" in st.session_state:
                del st.session_state.image
            
            # Reset status login
            st.session_state.logged_in = False
            
            # Arahkan ke halaman login
            st.session_state.page = "login"
            
            # Refresh aplikasi
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import base64
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Image Processing", layout="wide")

# =========================
# BACKGROUND FUNCTION
# =========================
def get_base64_image(image_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, image_filename)

    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# =========================
# GET IMAGE
# =========================
def get_image():
    if "image" not in st.session_state:
        st.error("Belum ada gambar dari dashboard")
        st.stop()
    return st.session_state.image

# =========================
# CONVERTER
# =========================
def to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def to_cv(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# =========================
# HISTOGRAM
# =========================
def show_histogram(img, title):
    fig, ax = plt.subplots(figsize=(4, 2))
    colors = ("b", "g", "r")

    for i, c in enumerate(colors):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        ax.plot(hist, color=c, linewidth=1)

    ax.set_title(title, fontsize=9, color="#ffd6d6")
    ax.set_xlim([0, 256])

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_facecolor("none")
    fig.patch.set_alpha(0)
    ax.tick_params(axis="both", length=0, labelsize=7, colors="#ffd6d6")

    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

# =========================
# PROCESSING PAGE
# =========================
def show_processing():
    # BACKGROUND STYLE
    bg_base64 = get_base64_image("background.jpg")

    if bg_base64:
        bg_style = f"""
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.65)),
                        url(data:image/jpeg;base64,{bg_base64}) !important;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
        """
    else:
        bg_style = """
        .stApp {
            background: radial-gradient(circle at 50% 30%, #200202 0%, #050000 100%) !important;
        }
        """

    # CSS
    st.markdown(f"""
    <style>
    {bg_style}
    .glass {{
        background: rgba(25, 3, 3, 0.55);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border-radius: 18px;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }}
    h1, h2, h3, label {{ color: #ffd6d6 !important; }}
    section[data-testid="stSidebar"] {{ background: rgba(10,0,0,0.88); }}
    [data-testid="column"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
    *::before, *::after {{ content: none !important; }}
    </style>
    """, unsafe_allow_html=True)

    img_original = get_image()
    pil_img = to_pil(img_original)

    # SIDEBAR
    st.sidebar.title("CONTROL PANEL")
    if st.sidebar.button("Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()

    # OPENCV BUTTONS
    st.sidebar.subheader("OpenCV Features")
    if "opencv_choice" not in st.session_state:
        st.session_state.opencv_choice = "None"

    def set_effect(val):
        st.session_state.opencv_choice = val

    opencv_choice = st.session_state.opencv_choice
    for effect in ["None", "Grayscale", "Blur", "Edge"]:
        st.sidebar.button(effect, use_container_width=True,
            type="primary" if opencv_choice == effect else "secondary",
            on_click=set_effect, args=(effect,))

    # PILLOW SETTINGS
    st.sidebar.subheader("Pillow Features")
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
    color = st.sidebar.slider("Color", 0.5, 2.0, 1.0)
    sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0)
    rotate = st.sidebar.selectbox("Rotate", [0, 90, 180, 270])
    resize = st.sidebar.slider("Resize %", 50, 150, 100)
    download_format = st.sidebar.selectbox("Download", ["JPG", "PNG"])

    # PROCESS IMAGE
    img = pil_img
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(color)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = img.rotate(rotate, expand=True)
    if resize != 100:
        w, h = img.size
        img = img.resize((int(w * resize / 100), int(h * resize / 100)))

    img_edit = to_cv(img)

    # OPENCV EFFECTS
    if opencv_choice == "Grayscale":
        img_edit = cv2.cvtColor(img_edit, cv2.COLOR_BGR2GRAY)
        img_edit = cv2.cvtColor(img_edit, cv2.COLOR_GRAY2BGR)
    elif opencv_choice == "Blur":
        img_edit = cv2.GaussianBlur(img_edit, (11, 11), 0)
    elif opencv_choice == "Edge":
        gray = cv2.cvtColor(img_edit, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        img_edit = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # TITLE
    st.markdown("<h1 style='text-align:center;'>IMAGE PROCESSING</h1>", unsafe_allow_html=True)

    # DISPLAY
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Original Image")
        st.image(img_original, use_container_width=True)
        show_histogram(img_original, "Original")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("### Processed Image")
        st.image(img_edit, use_container_width=True)
        show_histogram(img_edit, "Processed")
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # DOWNLOAD
    # =========================
    ext = ".jpg" if download_format == "JPG" else ".png"
    success, buffer = cv2.imencode(ext, img_edit)
    
    if success:
        st.sidebar.markdown("---")
        
        # 1. Tombol Download
        st.sidebar.download_button(
            "Download Image",
            data=buffer.tobytes(),
            file_name=f"result{ext}",
            mime="image/jpeg" if download_format == "JPG" else "image/png",
            use_container_width=True
        )
        
        # 2. Tombol Selesai (Logout dan Bersihkan State)
        if st.sidebar.button("Selesai", use_container_width=True, key="done_btn"):
            # Hapus data gambar dari memori
            if "image" in st.session_state:
                del st.session_state.image
            
            # Reset status login
            st.session_state.logged_in = False
            
            # Arahkan ke halaman login
            st.session_state.page = "login"
            
            # Refresh aplikasi
            st.rerun()