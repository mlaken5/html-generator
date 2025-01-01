import os
from pathlib import Path
from flask import Flask, render_template, request, send_file, redirect, url_for
from io import BytesIO
import base64

app = Flask(__name__)

# Allowed file types
ALLOWED_EXTENSIONS = {".mp4", ".jpg", ".jpeg", ".png", ".gif"}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def create_html_file(file, filename):
    """Create an HTML file for the given media file."""
    # Get the file name and extension
    file_name = Path(filename).stem
    file_extension = Path(filename).suffix.lower()

    # Read the file content and encode it as a data URL
    file_content = file.read()
    file_base64 = base64.b64encode(file_content).decode("utf-8")
    mime_type = {
        ".mp4": "video/mp4",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
    }.get(file_extension)

    if not mime_type:
        return None

    data_url = f"data:{mime_type};base64,{file_base64}"

    # Create HTML content based on file type
    if file_extension == ".mp4":
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{file_name}</title>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: black;
                }}
                video {{
                    max-width: 100%;
                    max-height: 100%;
                }}
            </style>
        </head>
        <body>
            <video controls autoplay loop muted playsinline>
                <source src="{data_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </body>
        </html>
        """
    elif file_extension in [".jpeg", ".jpg", ".png", ".gif"]:
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{file_name}</title>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    height: 100%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background-color: black;
                }}
                img {{
                    max-width: 100%;
                    max-height: 100%;
                }}
            </style>
        </head>
        <body>
            <img src="{data_url}" alt="{file_name}">
        </body>
        </html>
        """
    else:
        return None

    # Debug: Print the HTML content
    print("Generated HTML Content:")
    print(html_content)

    # Return the HTML content as a BytesIO object
    return BytesIO(html_content.encode("utf-8"))

# Store HTML files in memory
html_files_storage = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if files were uploaded
        if "files" not in request.files:
            return redirect(request.url)

        files = request.files.getlist("files")
        html_files = []

        # Process each uploaded file
        for file in files:
            if file and allowed_file(file.filename):
                # Create the HTML file in memory
                html_file = create_html_file(file, file.filename)
                if html_file:
                    # Store the clean file name and the HTML file
                    clean_name = f"{Path(file.filename).stem}.html"
                    html_files_storage[clean_name] = html_file
                    html_files.append(clean_name)

        # Store the HTML files in the session for download
        if html_files:
            return render_template("download.html", files=html_files)

    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    # Retrieve the HTML file from memory
    html_file = html_files_storage.get(filename)
    if html_file:
        # Debug: Print the file being served
        print(f"Serving file: {filename}")
        return send_file(
            html_file,
            as_attachment=True,
            download_name=filename,  # Use the clean file name
            mimetype="text/html",
        )
    return "File not found.", 404

if __name__ == "__main__":
    app.run(debug=True)