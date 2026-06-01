import customtkinter as ctk
import yt_dlp
import threading
import os
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext


class YouTubeDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Video Downloader")
        self.geometry("600x750")
        self.minsize(500, 650)

        # Duolingo-inspired color scheme
        self.configure(fg_color="#1CB0F6")  # Duolingo blue background

        # Set appearance mode
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.download_path = os.path.expanduser("~/Downloads")
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Video Downloader",
            font=("Nunito", 32, "bold"),
            text_color="#FFFFFF"
        )
        title_label.pack(pady=(40, 20))

        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self,
            text="Download YouTube videos in your preferred format",
            font=("Nunito", 14),
            text_color="#FFFFFF"
        )
        subtitle_label.pack(pady=(0, 30))

        # Main container
        container = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=20)
        container.pack(pady=20, padx=40, fill="both", expand=True)

        # URL Input
        url_label = ctk.CTkLabel(
            container,
            text="YouTube URL",
            font=("Nunito", 14, "bold"),
            text_color="#58CC02"
        )
        url_label.pack(pady=(30, 10), anchor="w", padx=30)

        self.url_entry = ctk.CTkEntry(
            container,
            placeholder_text="Paste your YouTube URL here...",
            font=("Nunito", 12),
            height=50,
            corner_radius=12,
            border_color="#E5E5E5",
            fg_color="#F7F7F7"
        )
        self.url_entry.pack(pady=(0, 20), padx=30, fill="x")

        # Quality Selection
        quality_label = ctk.CTkLabel(
            container,
            text="Quality",
            font=("Nunito", 14, "bold"),
            text_color="#58CC02"
        )
        quality_label.pack(pady=(10, 10), anchor="w", padx=30)

        self.quality_var = ctk.StringVar(value="720p")
        self.quality_menu = ctk.CTkOptionMenu(
            container,
            values=["480p", "720p", "1080p", "HD"],
            variable=self.quality_var,
            font=("Nunito", 12),
            height=50,
            corner_radius=12,
            fg_color="#F7F7F7",
            button_color="#58CC02",
            button_hover_color="#46A302",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#F7F7F7"
        )
        self.quality_menu.pack(pady=(0, 20), padx=30, fill="x")

        # Format Selection
        format_label = ctk.CTkLabel(
            container,
            text="Format",
            font=("Nunito", 14, "bold"),
            text_color="#58CC02"
        )
        format_label.pack(pady=(10, 10), anchor="w", padx=30)

        self.format_var = ctk.StringVar(value="MP4")
        self.format_menu = ctk.CTkOptionMenu(
            container,
            values=["MP4", "MP3", "WebM", "MKV", "AVI"],
            variable=self.format_var,
            font=("Nunito", 12),
            height=50,
            corner_radius=12,
            fg_color="#F7F7F7",
            button_color="#58CC02",
            button_hover_color="#46A302",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#F7F7F7"
        )
        self.format_menu.pack(pady=(0, 20), padx=30, fill="x")

        # Download Path Selection
        path_label = ctk.CTkLabel(
            container,
            text="Save to",
            font=("Nunito", 14, "bold"),
            text_color="#58CC02"
        )
        path_label.pack(pady=(10, 10), anchor="w", padx=30)

        path_frame = ctk.CTkFrame(container, fg_color="transparent")
        path_frame.pack(pady=(0, 20), padx=30, fill="x")

        self.path_label = ctk.CTkLabel(
            path_frame,
            text=os.path.basename(self.download_path) or self.download_path,
            font=("Nunito", 12),
            text_color="#777777"
        )
        self.path_label.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.browse_button = ctk.CTkButton(
            path_frame,
            text="Browse",
            font=("Nunito", 12, "bold"),
            fg_color="#1CB0F6",
            hover_color="#15A0E6",
            text_color="#FFFFFF",
            corner_radius=12,
            height=40,
            width=80,
            command=self.select_path
        )
        self.browse_button.pack(side="right")

        # Download Button
        self.download_button = ctk.CTkButton(
            container,
            text="Download",
            font=("Nunito", 18, "bold"),
            fg_color="#58CC02",
            hover_color="#46A302",
            text_color="#FFFFFF",
            corner_radius=15,
            height=60,
            command=self.download
        )
        self.download_button.pack(pady=(20, 20), padx=30, fill="x")

        # Status Label
        status_header = ctk.CTkLabel(
            container,
            text="Status",
            font=("Nunito", 14, "bold"),
            text_color="#58CC02"
        )
        status_header.pack(pady=(10, 5), anchor="w", padx=30)

        # Log Display
        self.log_text = scrolledtext.ScrolledText(
            container,
            height=10,
            font=("Nunito", 10)
        )
        self.log_text.pack(pady=(0, 30), padx=30, fill="both", expand=True)

    def select_path(self):
        path = filedialog.askdirectory(title="Select download folder")
        if path:
            self.download_path = path
            self.path_label.configure(text=os.path.basename(path) or path)

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.update()

    def download(self):
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        self.log_text.delete("1.0", "end")
        self.log("Starting download...\n")

        # Disable button during download
        self.download_button.configure(state="disabled", text="Downloading...")

        # Run download in separate thread
        thread = threading.Thread(target=self._download_video, args=(url,))
        thread.daemon = True
        thread.start()

    def _download_video(self, url):
        try:
            import shutil
            ffmpeg_path = shutil.which('ffmpeg')
            if not ffmpeg_path:
                try:
                    from imageio_ffmpeg import get_ffmpeg_exe
                    ffmpeg_path = get_ffmpeg_exe()
                except Exception:
                    try:
                        import ffmpeg_downloader
                        ffmpeg_downloader.add_path()
                        ffmpeg_path = ffmpeg_downloader.ffmpeg_path
                    except Exception:
                        ffmpeg_path = None

            if not ffmpeg_path:
                raise RuntimeError(
                    "ffmpeg is required for merging or audio extraction. "
                    "Install ffmpeg from https://ffmpeg.org/download.html "
                    "or `pip install imageio-ffmpeg`.")

            # Quality mapping
            quality = self.quality_var.get()
            quality_limit_map = {
                "480p": "480",
                "720p": "720",
                "1080p": "1080",
                "HD": "9999",
            }
            quality_limit = quality_limit_map.get(quality, "720")
            base_format_str = f"bestvideo[height<={quality_limit}]+bestaudio/best"

            # Format selection
            output_format = self.format_var.get().lower()
            format_str = base_format_str
            postprocessors = []
            postprocessor_args = {}

            if output_format == "mp4":
                format_str = (
                    f"bestvideo[vcodec^=avc1][ext=mp4][height<={quality_limit}]"
                    f"+bestaudio[acodec^=mp4a][ext=m4a]/"
                    f"best[ext=mp4][vcodec^=avc1][acodec^=mp4a][height<={quality_limit}]"
                )
            elif output_format == "mp3":
                format_str = "bestaudio/best"
                postprocessors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                postprocessors = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': output_format,
                }]

            self.log(f"Selected quality: {quality} -> format: {format_str}")

            ydl_opts = {
                'format': format_str,
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'ffmpeg_location': ffmpeg_path,
                'progress_hooks': [self._progress_hook],
                'postprocessors': postprocessors,
                'postprocessor_args': postprocessor_args,
            }

            if output_format == "mp4":
                ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if output_format == "mp3":
                    self.log("Downloading audio...")
                else:
                    self.log("Downloading video...")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if output_format == "mp3":
                    filename = os.path.splitext(filename)[0] + ".mp3"
                self.log(f"\n✓ Download complete!")
                self.log(f"Saved as: {filename}")

            self.after(0, lambda: self.download_button.configure(state="normal", text="Download"))
            self.after(0, lambda: messagebox.showinfo("Success", f"Download completed successfully.\n\n{filename}"))

        except Exception as e:
            self.log(f"\n✗ Error: {str(e)}")
            self.after(0, lambda: self.download_button.configure(state="normal", text="Download"))
            self.after(0, lambda: messagebox.showerror("Download Error", f"Failed to download media:\n{str(e)}"))

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.log(f"Progress: {percent} | Speed: {speed}")
        elif d['status'] == 'finished':
            selected_format = self.format_var.get().lower()
            if selected_format == "mp4":
                self.log("Download finished, merging compatible H.264/AAC MP4 streams...")
            elif selected_format == "mp3":
                self.log("Download finished, extracting MP3 audio...")
            else:
                self.log("Download finished, now converting...")


if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
