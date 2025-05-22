import streamlit as st
from pdf2docx import Converter
from docx2pdf import convert as docx_to_pdf_convert
import os
import tempfile

st.set_page_config(page_title="PDF ↔ Word Converter", page_icon="📝")

st.title("📄 PDF ↔ Word Converter")
st.write("Easily convert between PDF and Word formats.")

option = st.radio("Choose conversion type:", ("PDF to Word", "Word to PDF"))

if option == "PDF to Word":
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if pdf_file and st.button("Convert to Word"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf_file.read())
            tmp_pdf_path = tmp_pdf.name

        docx_output = tmp_pdf_path.replace(".pdf", ".docx")
        try:
            with st.spinner("Converting PDF to Word..."):
                cv = Converter(tmp_pdf_path)
                cv.convert(docx_output, start=0, end=None)
                cv.close()
            with open(docx_output, "rb") as f:
                st.download_button("📥 Download Word File", f, file_name="converted.docx")
        except Exception as e:
            st.error(f"Conversion failed: {e}")

elif option == "Word to PDF":
    docx_file = st.file_uploader("Upload a Word (.docx) file", type=["docx"])
    if docx_file and st.button("Convert to PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            tmp_docx.write(docx_file.read())
            tmp_docx_path = tmp_docx.name

        pdf_output = tmp_docx_path.replace(".docx", ".pdf")
        try:
            with st.spinner("Converting Word to PDF..."):
                docx_to_pdf_convert(tmp_docx_path, pdf_output)
            with open(pdf_output, "rb") as f:
                st.download_button("📥 Download PDF File", f, file_name="converted.pdf")
        except Exception as e:
            st.error(f"Conversion failed: {e}")
