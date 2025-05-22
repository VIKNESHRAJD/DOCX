import streamlit as st
from pdf2docx import Converter
import tempfile
import os
import pypandoc
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Ensure pandoc installed
try:
    pypandoc.get_pandoc_version()
except OSError:
    pypandoc.download_pandoc()

st.set_page_config(page_title="Document & PDF Toolkit", page_icon="📄", layout="wide")

st.title("📄 Document & PDF Toolkit")
st.markdown("Convert Word ↔ PDF, Images to PDF, split & merge PDFs — all in one app!")

# Sidebar navigation
option = st.sidebar.selectbox(
    "Choose an operation",
    [
        "Word ↔ PDF Converter",
        "Images to PDF",
        "PDF Splitter",
        "PDF Merger"
    ]
)

##########################
# WORD <-> PDF CONVERTER ##
##########################
if option == "Word ↔ PDF Converter":
    st.header("Word ↔ PDF Converter")
    conv_type = st.radio("Choose conversion direction:", ["PDF to Word", "Word to PDF"])

    if conv_type == "PDF to Word":
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

    elif conv_type == "Word to PDF":
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

##########################
# IMAGES TO PDF          ##
##########################
elif option == "Images to PDF":
    st.header("Convert Images to PDF")
    uploaded_images = st.file_uploader("Upload one or more images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    pdf_name = st.text_input("Output PDF file name (without extension):", "output")

    if uploaded_images and st.button("Convert Images to PDF"):
        images = []
        try:
            for img_file in uploaded_images:
                img = Image.open(img_file).convert("RGB")
                images.append(img)

            pdf_bytes = BytesIO()
            images[0].save(pdf_bytes, format="PDF", save_all=True, append_images=images[1:])
            pdf_bytes.seek(0)

            st.success(f"✅ Converted {len(images)} image(s) to PDF!")
            st.download_button(
                label="📥 Download PDF",
                data=pdf_bytes,
                file_name=f"{pdf_name}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")

##########################
# PDF SPLITTER           ##
##########################
elif option == "PDF Splitter":
    st.header("Split PDF into Single Pages")
    pdf_file = st.file_uploader("Upload a PDF file to split", type=["pdf"])

    if pdf_file:
        try:
            pdf_reader = PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            st.write(f"PDF has {num_pages} pages.")
            split_option = st.radio("Split Options:", ["All pages as separate PDFs", "Extract specific pages"])

            if split_option == "Extract specific pages":
                pages_input = st.text_input("Enter page numbers (comma separated, 1-based):", "1")
                pages_to_extract = [int(p.strip()) - 1 for p in pages_input.split(",") if p.strip().isdigit()]
            else:
                pages_to_extract = list(range(num_pages))

            if st.button("Split PDF"):
                output_files = []
                for i in pages_to_extract:
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[i])
                    output_pdf = BytesIO()
                    pdf_writer.write(output_pdf)
                    output_pdf.seek(0)
                    output_files.append((f"page_{i+1}.pdf", output_pdf.read()))

                st.success(f"✅ Split {len(output_files)} pages!")

                for fname, data in output_files:
                    st.download_button(
                        label=f"Download {fname}",
                        data=data,
                        file_name=fname,
                        mime="application/pdf"
                    )
        except Exception as e:
            st.error(f"❌ Failed to split PDF: {e}")

##########################
# PDF MERGER             ##
##########################
elif option == "PDF Merger":
    st.header("Merge Multiple PDFs")
    uploaded_pdfs = st.file_uploader("Upload PDF files to merge", type=["pdf"], accept_multiple_files=True)
    output_name = st.text_input("Output PDF file name (without extension):", "merged")

    if uploaded_pdfs and len(uploaded_pdfs) > 1 and st.button("Merge PDFs"):
        try:
            pdf_writer = PdfWriter()

            for pdf_file in uploaded_pdfs:
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

            output_pdf = BytesIO()
            pdf_writer.write(output_pdf)
            output_pdf.seek(0)

            st.success(f"✅ Merged {len(uploaded_pdfs)} PDFs!")

            st.download_button(
                label="📥 Download Merged PDF",
                data=output_pdf,
                file_name=f"{output_name}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"❌ Failed to merge PDFs: {e}")
    elif uploaded_pdfs and len(uploaded_pdfs) < 2:
        st.warning("Please upload at least two PDF files to merge.")

