import streamlit as st
from pdf2docx import Converter
import tempfile
import os
import pypandoc

# Automatically download Pandoc if not found
try:
    pypandoc.get_pandoc_version()
except OSError:
    pypandoc.download_pandoc()

st.set_page_config(page_title="Word ↔ PDF Converter", page_icon="📝")
st.title("📄 Word ↔ PDF Converter")
st.write("Convert between Word (.docx) and PDF files (cross-platform)")

option = st.radio("Select conversion type:", ["PDF to Word", "Word to PDF"])

if option == "PDF to Word":
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_pdf and st.button("Convert to Word"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(uploaded_pdf.read())
            tmp_pdf_path = tmp_pdf.name

        docx_output = tmp_pdf_path.replace(".pdf", ".docx")

        try:
            with st.spinner("Converting PDF to Word..."):
                cv = Converter(tmp_pdf_path)
                cv.convert(docx_output, start=0, end=None)
                cv.close()

            with open(docx_output, "rb") as f:
                st.download_button(
                    label="📥 Download Word File",
                    data=f,
                    file_name="converted.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")

elif option == "Word to PDF":
    uploaded_docx = st.file_uploader("Upload a Word file", type=["docx"])
    if uploaded_docx and st.button("Convert to PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            tmp_docx.write(uploaded_docx.read())
            tmp_docx_path = tmp_docx.name

        pdf_output = tmp_docx_path.replace(".docx", ".pdf")

        try:
            with st.spinner("Converting Word to PDF..."):
                pypandoc.convert_file(tmp_docx_path, 'pdf', outputfile=pdf_output)

            with open(pdf_output, "rb") as f:
                st.download_button(
                    label="📥 Download PDF File",
                    data=f,
                    file_name="converted.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
