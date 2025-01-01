# HTML Generator

A web application that allows users to upload MP4, JPEG, PNG, or GIF files and converts them into self-contained HTML files. The HTML files can be downloaded and viewed in any browser.

## Features

- Upload multiple files (MP4, JPEG, PNG, GIF).
- Generates HTML files with embedded media (using data URLs).
- Clean and professional UI with a progress bar.
- No file storage on the server—files are processed in memory.
- Lightweight and easy to deploy.

## How to Use

1. Upload your files using the web interface.
2. Wait for the files to be processed (a progress bar will show the status).
3. Download the generated HTML files.

## Deployment

This app is designed to be deployed on [Render](https://render.com). Follow these steps:

1. Push the code to your GitHub repository.
2. Create a new web service on Render and connect your repository.
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
4. Deploy the app.

## Technologies Used

- Python
- Flask
- HTML/CSS/JavaScript

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

By **The Gadget Aid LLC**