import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar, Style, Button
import threading
from slide_extractor import SlideExtractor
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class SlideExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📽️ YouTube Slide Extractor")
        self.root.geometry("850x700")

        self.is_dark_mode = False
        self.light_theme = {"bg": "#ffffff", "fg": "#333", "entry_bg": "#ffffff", "entry_fg": "#000"}
        self.dark_theme = {"bg": "#1e1e1e", "fg": "#f5f5f5", "entry_bg": "#2b2b2b", "entry_fg": "#f5f5f5"}

        self.style = Style()
        self.style.theme_use('clam')
        self.style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"), padding=10, background="#1976D2", foreground="white")
        self.style.map("Accent.TButton", background=[("active", "#1565C0")])

        self.widgets = []

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.header = tk.Label(self.root, text="YouTube Slide Extractor", font=("Segoe UI", 24, "bold"))
        self.header.pack(pady=(30, 10))
        self.widgets.append(self.header)

        self.form = tk.Frame(self.root)
        self.form.pack(pady=20)
        self.widgets.append(self.form)

        def add_labeled_entry(row, text, default=""):
            label = tk.Label(self.form, text=text, font=("Segoe UI", 14))
            label.grid(row=row, column=0, padx=20, pady=15, sticky="e")
            entry = tk.Entry(self.form, font=("Segoe UI", 14), width=40)
            entry.grid(row=row, column=1, padx=10, pady=15)
            entry.insert(0, default)
            self.widgets.extend([label, entry])
            return entry

        self.url_entry = add_labeled_entry(0, "YouTube URL:")
        self.interval_entry = add_labeled_entry(1, "Frame Interval (s):", "5")
        self.threshold_entry = add_labeled_entry(2, "Similarity Threshold (0-1):", "0.9")

        self.status_label = tk.Label(self.root, text="Status: Waiting...", font=("Segoe UI", 12))
        self.status_label.pack(pady=(10, 5))
        self.widgets.append(self.status_label)

        self.progress_bar = Progressbar(self.root, orient="horizontal", length=600, mode="indeterminate")
        self.progress_bar.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.widgets.append(self.button_frame)

        self.extract_button = Button(self.button_frame, text="🎞️ Extract Slides", style="Accent.TButton", command=self.extract_slides)
        self.extract_button.grid(row=0, column=0, padx=20)

        self.pdf_button = Button(self.button_frame, text="📄 Generate PDF", style="Accent.TButton", command=self.generate_pdf)
        self.pdf_button.grid(row=0, column=1, padx=20)

        self.toggle_theme_btn = Button(self.root, text="🌓 Toggle Theme", style="Accent.TButton", command=self.toggle_theme)
        self.toggle_theme_btn.pack(pady=(10, 20))

    def apply_theme(self):
        theme = self.dark_theme if self.is_dark_mode else self.light_theme
        self.root.configure(bg=theme["bg"])

        for widget in self.widgets:
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme["bg"])

            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme["bg"], fg=theme["fg"])

            elif isinstance(widget, tk.Entry):
                widget.configure(bg=theme["entry_bg"], fg=theme["entry_fg"], insertbackground=theme["entry_fg"])

            # For Button widgets, ensure proper handling of fg/bg
            elif isinstance(widget, Button):
                widget.configure(style="Accent.TButton")

            # Progressbar styling
            elif isinstance(widget, Progressbar):
                self.style.configure("TProgressbar", thickness=25, background=theme["fg"])
                widget.configure(style="TProgressbar")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def extract_slides(self):
        url = self.url_entry.get()
        interval = int(self.interval_entry.get())
        threshold = float(self.threshold_entry.get())

        self.set_widgets_state("disabled")
        self.status_label.config(text="Status: Downloading video...")
        self.progress_bar.start()

        threading.Thread(target=self.start_slide_extraction, args=(url, interval, threshold)).start()

    def start_slide_extraction(self, url, interval, threshold):
        try:
            extractor = SlideExtractor(video_url=url, interval=interval, similarity_threshold=threshold)
            if extractor.extract_slides():
                self.update_status("Status: Extraction Complete ✅")
            else:
                self.update_status("Status: Extraction Failed ❌")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.progress_bar.stop()
            self.set_widgets_state("normal")

    def update_status(self, text):
        self.root.after(0, self.status_label.config, {"text": text})

    def set_widgets_state(self, state):
        for widget in [self.url_entry, self.interval_entry, self.threshold_entry, self.extract_button]:
            widget.config(state=state)

    def generate_pdf(self):
        slide_folder = "slides"
        pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if not pdf_filename:
            return

        try:
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setFont("Helvetica", 16)
            slide_images = sorted([f for f in os.listdir(slide_folder) if f.endswith(".png")])

            y_position = 750
            for slide in slide_images:
                slide_path = os.path.join(slide_folder, slide)
                img = Image.open(slide_path)
                img_width, img_height = img.size
                c.drawImage(slide_path, 50, y_position, width=500, height=(img_height * 500) / img_width)

                y_position -= 550
                if y_position < 100:
                    c.showPage()
                    y_position = 750

            c.save()
            messagebox.showinfo("✅ Success", f"PDF saved to: {pdf_filename}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error generating PDF: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SlideExtractorApp(root)
    root.mainloop()
