# Image Analysis Tool

This project is a Python-based tool for analyzing images captured via a connected camera. It uses OpenAI's API to generate concise details about objects in an image and records the results in an Excel file. The tool features a simple graphical interface with the ability to select cameras, capture photos, and review analysis results.

---

## Features
1. **Camera Selection**: Select from available cameras on your device.
2. **Capture Image**: Take photos directly from the UI.
3. **AI-Powered Analysis**: Analyze the image for details such as:
   - The item in the image.
   - Its condition (e.g., brand new, worn out).
   - A suitable price for a charity store.
   - Any special features (e.g., "none").
4. **Excel Logging**: Results are stored in an Excel file (`analysis_results.xlsx`) for easy review and record-keeping.

---

## Prerequisites
Since this tool is designed for a new Windows PC, you'll need to install the following components before running the program:

1. **Python**:
   - Download and install Python (version 3.10 or later) from [https://www.python.org/downloads/](https://www.python.org/downloads/).
   - Ensure you add Python to the system PATH during installation.

2. **Required Python Libraries**:
   Install the necessary libraries using `pip` after Python is set up:
   ```bash
   pip install openai pandas openpyxl opencv-python-headless pillow ttkthemes
   ```

3. **Install OpenCV**:
   If you encounter issues with camera functionality, you may need to install the full OpenCV package:
   ```bash
   pip install opencv-python
   ```

---

## Usage Instructions
1. **Download the Script**:
   Save the provided Python script to a folder on your computer.

2. **Run the Program**:
   Open a terminal or command prompt, navigate to the folder containing the script, and run:
   ```bash
   python <script_name>.py
   ```

3. **Using the UI**:
   - Select a camera from the dropdown menu.
   - Click the "Take Photo" button to capture an image and analyze it.
   - View the analysis result in both the terminal and the application.
   - Results are automatically saved to `analysis_results.xlsx` in the working directory.

4. **Quit**:
   Click the "Quit" button to close the application.

---

## File Outputs
- **Captured Images**: Saved as `captured_image.jpg` in the working directory.
- **Analysis Results**: Stored in `analysis_results.xlsx` with the following columns:
  - `Item`
  - `Condition`
  - `Price`
  - `Special Info`

---

## Troubleshooting
- **Missing Libraries**:
  If you encounter a `ModuleNotFoundError`, ensure all required libraries are installed by running:
  ```bash
  pip install -r requirements.txt
  ```
  (Create a `requirements.txt` file with the library names listed above.)

- **Camera Not Detected**:
  Ensure your camera is properly connected and try restarting the program.

- **Excel File Issues**:
  Verify that `openpyxl` is installed to allow writing to Excel files.

---

## License
This project is open-source and available for modification and redistribution.

