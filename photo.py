import streamlit as st
from PIL import Image
import tempfile
import os

st.set_page_config(page_title="Image to PDF Converter", page_icon="🖼️")

st.title("🖼️ Convert Images to PDF")
st.write("Upload one or more images and convert them into a single PDF file.")

# Upload multiple images
uploaded_files = st.file_uploader("Upload image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files and st.button("Convert to PDF"):
    images = []

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        images.append(image)

    if images:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            images[0].save(tmp_pdf.name, save_all=True, append_images=images[1:])
            st.success("✅ PDF Created Successfully!")
            with open(tmp_pdf.name, "rb") as f:
                st.download_button(
                    label="📥 Download PDF",
                    data=f,
                    file_name="converted_images.pdf",
                    mime="application/pdf"
                )
    else:
        st.error("❌ No valid images uploaded.")
