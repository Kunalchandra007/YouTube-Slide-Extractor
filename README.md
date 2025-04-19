# 🎞️ YouTube Slide Extractor

A Python desktop application that extracts slide-like frames from educational YouTube videos and compiles them into a downloadable PDF.

## ✨ Features

- Download YouTube videos using `yt-dlp`
- Extract keyframes based on:
  - Time interval
  - Visual similarity
  - OCR-based text difference
- Generate a PDF of all extracted slides
- Toggle between Light and Dark themes
- Beautiful GUI built with `Tkinter`

## 📦 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```
Required packages:

opencv-python

pytesseract

Pillow

yt-dlp

scikit-image

tk

reportlab
🚀 How to Run
```bash
python main.py
```
🛠️ How It Works
Paste a YouTube video URL.

Choose:

Frame interval in seconds

Similarity threshold (0–1)

Click "🎞️ Extract Slides"

Click "📄 Generate PDF" to save the extracted slides.

📁 Output
Extracted slides saved as .png files in the slides/ directory

PDF file created at your selected location

📸 Screenshot
Add a screenshot here if needed.

👨‍💻 Author
Made with ❤️ by Kunal Chandra




