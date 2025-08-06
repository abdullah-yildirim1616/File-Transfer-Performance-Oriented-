from flask import Flask, render_template, send_from_directory, request, url_for
import os
from PIL import Image

app = Flask(__name__)

BASE_DIR = os.path.expanduser("C:\\Users\\abdus\\OneDrive\\Masaüstü")
THUMBNAIL_DIR = os.path.join(BASE_DIR, ".thumbnails")

# Thumbnail klasörü yoksa oluştur
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

def create_thumbnail(image_path, thumb_path, size=(120, 100)):
    try:
        img = Image.open(image_path)
        img.thumbnail(size)
        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
        img.save(thumb_path)
        return True
    except Exception as e:
        print(f"Thumbnail error: {e}")
        return False

def get_thumbnail(file_path):
    relative_path = os.path.relpath(file_path, BASE_DIR)
    thumb_path = os.path.join(THUMBNAIL_DIR, relative_path)

    if not os.path.exists(thumb_path):
        create_thumbnail(file_path, thumb_path)

    return url_for('thumbnail', path=relative_path.replace("\\", "/"))

@app.route("/")
def index():
    folders = []
    files = []
    thumbnails = {}

    current_path = request.args.get("path", BASE_DIR)

    try:
        for entry in os.listdir(current_path):
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                folders.append(entry)
            elif os.path.isfile(full_path):
                files.append(entry)
                # Eğer görselse thumbnail üret
                if entry.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    thumbnails[entry] = get_thumbnail(full_path)
    except Exception as e:
        print("HATA:", e)

    return render_template(
        "index.html",
        folders=folders,
        files=files,
        current_path=current_path,
        thumbnails=thumbnails
    )

@app.route("/download")
def download():
    path = request.args.get("path")
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route("/thumbnail/<path:path>")
def thumbnail(path):
    thumb_path = os.path.join(THUMBNAIL_DIR, path)
    thumb_dir = os.path.dirname(thumb_path)
    thumb_file = os.path.basename(thumb_path)
    return send_from_directory(thumb_dir, thumb_file)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
