import streamlit as st
from pdf2docx import Converter
import tempfile
import os
import pypandoc

# Automatically download pandoc if not found
try:
    pypandoc.get_pandoc_version()
except OSError:
    pypandoc.download_pandoc()

st.set_page_config(page_title="Word ↔ PDF Converter", page_icon="📄")
st.title("📄 Word ↔ PDF Converter")
st.markdown("Easily convert between **Word (.docx)** and **PDF** files.")

conversion_type = st.radio("Choose conversion direction:", ["PDF to Word", "Word to PDF"])

# PDF ➡ Word
if conversion_type == "PDF to Word":
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if pdf_file and st.button("Convert to Word"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf_file.read())
            pdf_path = tmp_pdf.name

        docx_path = pdf_path.replace(".pdf", ".docx")

        try:
            with st.spinner("Converting PDF to Word..."):
                cv = Converter(pdf_path)
                cv.convert(docx_path)
                cv.close()

            with open(docx_path, "rb") as f:
                st.success("✅ Conversion successful!")
                st.download_button(
                    label="📥 Download .docx",
                    data=f,
                    file_name="converted.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")

# Word ➡ PDF
elif conversion_type == "Word to PDF":
    docx_file = st.file_uploader("Upload a Word (.docx) file", type=["docx"])

    if docx_file and st.button("Convert to PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
            tmp_docx.write(docx_file.read())
            docx_path = tmp_docx.name

        pdf_path = docx_path.replace(".docx", ".pdf")

        try:
            with st.spinner("Converting Word to PDF..."):
                pypandoc.convert_file(
                    docx_path,
                    to='pdf',
                    outputfile=pdf_path,
                    extra_args=["--pdf-engine=xelatex"]
                )

            with open(pdf_path, "rb") as f:
                st.success("✅ Conversion successful!")
                st.download_button(
                    label="📥 Download PDF",
                    data=f,
                    file_name="converted.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
