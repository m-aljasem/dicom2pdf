# DICOM to PDF Converter

[![Streamlit](https://img.shields.io/badge/streamlit-powered-orange)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/yourusername/dicom-to-pdf)](LICENSE)

---

## Overview

The **DICOM to PDF Converter** is a powerful and user-friendly web application built with [Streamlit](https://streamlit.io/) that enables healthcare professionals, radiologists, and researchers to quickly convert entire collections of DICOM medical images into high-quality, square-format PDF documents. This tool simplifies reviewing and sharing MRI, CT, and other medical imaging scans by generating visually enhanced PDFs with a sleek black background and clear, white text annotations.

Designed with both usability and professionalism in mind, the application supports bulk uploads of zipped DICOM folders, automatically processes the images on the backend, and delivers a downloadable PDF with patient and scan metadata elegantly displayed on each page.

---

## Features

* **Easy Upload:** Upload zipped folders containing your DICOM files directly through the web interface. No need for complex software or command-line usage.
* **Automatic Extraction:** The app unzips and processes all included DICOM files seamlessly in a temporary backend environment.
* **High-Quality PDF Generation:** Generates square pages optimized for display and printing with a stylish black background and white text for easy viewing in dark environments.
* **Contrast Enhancement:** Advanced image normalization enhances scan visibility for better diagnostic review.
* **Metadata Display:** Each page displays relevant patient and scan metadata (e.g., patient name, series description) for quick identification.
* **Professional Branding:** Each PDF page footer includes custom branding: `DICOM2PDF - By Mohmad AlJasem https://aljasem.eu.org`.
* **Interactive Web Interface:** Powered by Streamlit, offering a responsive, modern, and intuitive user experience.
* **Google Analytics Ready:** Includes an easy way to insert Google Analytics tracking code for monitoring site usage and visitor behavior.
* **Downloadable Output:** Users receive a direct download link for their generated PDF after processing completes.

---

## Why Use This Tool?

DICOM (Digital Imaging and Communications in Medicine) files are the standard format for medical imaging. However, viewing or sharing these files often requires specialized software, which can be cumbersome or unavailable on some devices.

This tool provides a universal, portable format by converting DICOM scans into PDFs that:

* Can be opened easily on virtually any device.
* Are ideal for archiving, sharing with colleagues or patients, and inclusion in reports.
* Provide clear, enhanced visualization without sacrificing image quality.
* Include important metadata for context and documentation.

Whether you’re a medical professional needing to compile imaging data or a researcher archiving scans, this converter streamlines your workflow.

---

## Installation & Setup

To run the app locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/dicom-to-pdf.git
   cd dicom-to-pdf
   ```

2. **Create and activate a Python environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

5. **Open your browser at:**

   ```
   http://localhost:8501
   ```

---

## Usage Instructions

1. **Prepare your DICOM folder:**

   * Collect all your DICOM files into a single folder.
   * Zip the folder into a `.zip` archive.

2. **Upload your zipped folder:**

   * Use the "Upload zipped DICOM folder" button on the app page.

3. **Wait for processing:**

   * The app will extract, read, and convert the scans.
   * Progress is displayed with a spinner.

4. **Download your PDF:**

   * Once complete, click the download button to save your PDF file.

---

## Customization & Configuration

* **Google Analytics:** Replace the placeholder tracking ID (`G-XXXXXXX`) in the app code with your own to start tracking.
* **PDF Styling:** You can customize figure size, DPI, colors, fonts, and footer text within the `convert_to_pdf` function.
* **Supported DICOM Variants:** The app reads common DICOM formats but might require additional plugins like `pylibjpeg` for JPEG compressed images.

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request on GitHub.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## About the Author

Mohmad AlJasem is a medical professional and developer passionate about bridging healthcare and technology. Visit [https://aljasem.eu.org](https://aljasem.eu.org) for more projects and contact info.

---

## Acknowledgments

* [Streamlit](https://streamlit.io/) for making web app development easy and accessible.
* [pydicom](https://pydicom.github.io/) for handling complex DICOM file operations.
* [Matplotlib](https://matplotlib.org/) for powerful visualization capabilities.

---

**Feel free to star the repo ⭐ if you find it useful!**

---

If you want, I can generate a `requirements.txt` file or help you prepare a LICENSE file too. Just ask!
