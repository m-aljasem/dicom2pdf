import os
import zipfile
import tempfile
import random
import shutil
import subprocess
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

def normalize_image(image_array: np.ndarray, contrast_factor=0.9) -> np.ndarray:
    image_array = image_array.astype(np.float64)
    p2, p98 = np.percentile(image_array, [2, 98])
    image_array = np.clip(image_array, p2, p98)
    img_min = np.min(image_array)
    img_max = np.max(image_array)
    if img_max > img_min:
        image_array = (image_array - img_min) / (img_max - img_min)
    return np.power(image_array, contrast_factor)

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

def convert_to_pdf(dicom_folder: str, output_pdf: str, contrast_factor: float = 0.9, dpi: int = 200):
    dicom_files = find_dicom_files(dicom_folder)
    if not dicom_files:
        return None

    with PdfPages(output_pdf) as pdf:
        for i, file_path in enumerate(dicom_files):
            image_array, metadata = read_dicom_image(file_path)
            if image_array is None:
                continue

            norm_img = normalize_image(image_array, contrast_factor)

            fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
            ax.imshow(norm_img, cmap='gray', vmin=0, vmax=1)
            ax.set_facecolor('black')
            ax.axis('off')

            title = f"{metadata.get('patient_name', '')} | {metadata.get('series_description', '')}"
            fig.suptitle(title, fontsize=12, y=0.95, color='white')

            fig.text(0.5, 0.02, 'DICOM2PDF - By Mohmad AlJasem https://aljasem.eu.org', 
                     ha='center', va='bottom', fontsize=10, color='white')

            pdf.savefig(fig, bbox_inches='tight', pad_inches=0.1, facecolor=fig.get_facecolor(), dpi=dpi)
            plt.close(fig)

    return output_pdf

def extract_archive(archive_path: str, extract_to: str):
    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif archive_path.endswith(".rar"):
        subprocess.run(["unrar", "x", "-y", archive_path, extract_to], check=False)
    elif archive_path.endswith(".iso"):
        subprocess.run(["7z", "x", archive_path, f"-o{extract_to}"], check=False)

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
st.write("Upload a **.zip**, **.rar**, or **.iso** file containing your DICOM images. We'll generate a high-quality PDF scan for you.")

uploaded_archive = st.file_uploader("Upload compressed DICOM archive", type=["zip", "rar", "iso"])

contrast_factor = st.slider("Adjust Contrast", 0.5, 1.5, 0.9, step=0.05)
dpi = st.slider("Set PDF Resolution (DPI)", 100, 300, 200, step=10)

if uploaded_archive:
    with st.spinner("Processing your DICOM files..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, uploaded_archive.name)
            with open(archive_path, "wb") as f:
                f.write(uploaded_archive.read())

            extract_archive(archive_path, temp_dir)
            dicom_files = find_dicom_files(temp_dir)
            if dicom_files:
                st.subheader("📸 Image Preview")
                preview_files = random.sample(dicom_files, min(10, len(dicom_files)))
                for file in preview_files:
                    image_array, metadata = read_dicom_image(file)
                    if image_array is not None:
                        norm_img = normalize_image(image_array, contrast_factor)
                        st.image(norm_img, caption=str(file), use_column_width=True, clamp=True)

            output_pdf_path = os.path.join(temp_dir, "output.pdf")
            result = convert_to_pdf(temp_dir, output_pdf_path, contrast_factor=contrast_factor, dpi=dpi)

            if result and os.path.exists(output_pdf_path):
                with open(output_pdf_path, "rb") as f:
                    st.success("✅ PDF successfully created!")
                    st.download_button("📥 Download PDF", f, file_name="dicom_scan.pdf", mime="application/pdf")
            else:
                st.error("Failed to generate PDF. Please check your files.")
else:
    st.info("Please upload a compressed folder containing DICOM files.")

st.markdown("""
    <div class="custom-footer">
        Developed By <a href="https://aljasem.eu.org" target="_blank">Mohamad AlJasem</a>
    </div>
""", unsafe_allow_html=True)
