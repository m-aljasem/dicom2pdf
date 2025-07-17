import os
import zipfile
import tempfile
from pathlib import Path

import numpy as np
import pydicom
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from typing import Tuple

def read_dicom_image(file_path: str) -> Tuple[np.ndarray, dict]:
    try:
        dicom_data = pydicom.dcmread(file_path)
        try:
            image_array = dicom_data.pixel_array
        except Exception as e:
            return None, None

        metadata = {
            'patient_name': getattr(dicom_data, 'PatientName', 'Unknown'),
            'series_description': getattr(dicom_data, 'SeriesDescription', 'Unknown'),
            'instance_number': getattr(dicom_data, 'InstanceNumber', 'Unknown'),
            'slice_location': getattr(dicom_data, 'SliceLocation', 'Unknown'),
            'study_date': getattr(dicom_data, 'StudyDate', 'Unknown'),
            'modality': getattr(dicom_data, 'Modality', 'Unknown'),
            'rows': getattr(dicom_data, 'Rows', 0),
            'columns': getattr(dicom_data, 'Columns', 0),
        }

        return image_array, metadata
    except:
        return None, None

def normalize_image(image_array: np.ndarray) -> np.ndarray:
    image_array = image_array.astype(np.float64)
    p2, p98 = np.percentile(image_array, [2, 98])
    image_array = np.clip(image_array, p2, p98)
    img_min = np.min(image_array)
    img_max = np.max(image_array)
    if img_max > img_min:
        image_array = (image_array - img_min) / (img_max - img_min)
    return np.power(image_array, 0.9)  # Slight gamma correction for contrast

def find_dicom_files(folder_path: str):
    extensions = ['.dcm', '.dicom']
    dicom_files = []
    for path in Path(folder_path).rglob('*'):
        if path.is_file():
            if path.suffix.lower() in extensions or not path.suffix:
                try:
                    pydicom.dcmread(str(path), stop_before_pixels=True)
                    dicom_files.append(str(path))
                except:
                    pass
    return dicom_files

def convert_to_pdf(dicom_folder: str, output_pdf: str):
    dicom_files = find_dicom_files(dicom_folder)
    if not dicom_files:
        return None

    with PdfPages(output_pdf) as pdf:
        for i, file_path in enumerate(dicom_files):
            image_array, metadata = read_dicom_image(file_path)
            if image_array is None:
                continue

            norm_img = normalize_image(image_array)

            fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')  # Square page, black background
            ax.imshow(norm_img, cmap='gray', vmin=0, vmax=1)
            ax.set_facecolor('black')
            ax.axis('off')

            title = f"{metadata.get('patient_name', '')} | {metadata.get('series_description', '')}"
            fig.suptitle(title, fontsize=12, y=0.95, color='white')  # White title text

            # Add custom footer text
            fig.text(0.5, 0.02, 'DICOM2PDF - By Mohmad AlJasem https://aljasem.eu.org', 
                     ha='center', va='bottom', fontsize=10, color='white')

            pdf.savefig(fig, bbox_inches='tight', pad_inches=0.1, facecolor=fig.get_facecolor())
            plt.close(fig)

    return output_pdf

# Streamlit app
st.set_page_config(page_title="DICOM to PDF Converter", page_icon="🧠", layout="centered")
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        footer {visibility: hidden;}
        .custom-footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            font-size: 14px;
            color: #888;
            padding: 10px;
            background-color: #ffffff;
        }
    </style>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-XXXXXXX');
    </script>
""", unsafe_allow_html=True)

st.title("🧠 DICOM to PDF Converter")
st.write("Upload a **.zip** file containing your DICOM images. We'll generate a high-quality PDF scan for you.")

uploaded_zip = st.file_uploader("Upload zipped DICOM folder", type=["zip"])

if uploaded_zip:
    with st.spinner("Processing your DICOM files..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "dicom.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_zip.read())

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            output_pdf_path = os.path.join(temp_dir, "output.pdf")
            result = convert_to_pdf(temp_dir, output_pdf_path)

            if result and os.path.exists(output_pdf_path):
                with open(output_pdf_path, "rb") as f:
                    st.success("✅ PDF successfully created!")
                    st.download_button("📥 Download PDF", f, file_name="dicom_scan.pdf", mime="application/pdf")
            else:
                st.error("Failed to generate PDF. Please check your files.")
else:
    st.info("Please upload a zipped folder containing DICOM files.")

st.markdown("""
    <div class="custom-footer">
        Developed By <a href="https://aljasem.eu.org" target="_blank">Mohamad AlJasem</a>
    </div>
""", unsafe_allow_html=True)
