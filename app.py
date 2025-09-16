import streamlit as st
from PIL import Image, ImageOps
from io import BytesIO
import requests

st.set_page_config(page_title="Conversor a escala de grises", layout="centered")

st.title("Imagen a escala de grises con deslizador")
st.write("Sube una imagen o indica una URL, y ajusta la intensidad de gris.")

with st.sidebar:
    st.header("Entrada")
    uploaded_file = st.file_uploader("Sube una imagen", type=["png","jpg","jpeg","tif","tiff","bmp","webp"])
    url = st.text_input("…o pega la URL de una imagen (http/https)")
    intensity = st.slider("Intensidad de gris (%)", 0, 100, 100,
                          help="0% = imagen original en color; 100% = 100% en gris")

def load_image(uploaded_file, url):
    if uploaded_file is not None:
        img = Image.open(uploaded_file).convert("RGB")
        return img
    if url:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img
    return None

img = load_image(uploaded_file, url)

if img is None:
    st.info("Cargue una imagen desde el panel lateral o indique una URL.")
    st.stop()

gray = ImageOps.grayscale(img).convert("RGB")
alpha = intensity / 100.0  # 0.0 = color, 1.0 = gris
blended = Image.blend(img, gray, alpha)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader("Original")
    st.image(img, use_container_width=True)
with col2:
    st.subheader(f"Procesada ({intensity}%)")
    st.image(blended, use_container_width=True)

# Descargar resultado
buf = BytesIO()
blended.save(buf, format="PNG")
st.download_button(
    "Descargar imagen procesada (PNG)",
    data=buf.getvalue(),
    file_name="imagen_grises.png",
    mime="image/png"
)

st.caption("© App de demostración — escala de grises con mezcla lineal.")
