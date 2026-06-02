# Video Downloader

A modern YouTube video downloader with a Duolingo-inspired interface.
## Features

- **Quality Selection**: Choose from 1080p, 720p, 480p, or HD
- **Format Options**: Download as MP4, MP3, WebM, AVI, or MKV
- **Automatic Conversion**: Converts videos to your desired format using FFmpeg
- **Modern UI**: Clean, Duolingo-inspired design with rounded buttons and smooth animations
- **Progress Tracking**: Real-time download progress bar

## Installation

### 1. Install Python Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- `customtkinter` - Modern UI framework
- `yt-dlp` - YouTube downloader
- `pillow` - Image processing library

### 2. Install FFmpeg (Required for conversion)

FFmpeg is required to convert videos to MP4/MP3 format. Here's how to install it:

#### Windows (Easiest Method):

1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
2. Extract the downloaded file
3. Move the extracted folder to `C:\ffmpeg`
4. Add FFmpeg to your system PATH:
   - Press `Win + R`, type `sysdm.cpl`, and press Enter
   - Go to the "Advanced" tab and click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ffmpeg\bin`
   - Click OK on all windows
5. Restart your terminal/command prompt
6. Verify installation by running: `ffmpeg -version`

#### Alternative Windows Method (Using Chocolatey):

If you have Chocolatey package manager installed:

```bash
choco install ffmpeg
```

#### macOS:

```bash
brew install ffmpeg
```

#### Linux:

```bash
sudo apt update
sudo apt install ffmpeg
```

## Usage

1. Run the application:
   ```bash
   python downloader.py
   ```

2. Paste a YouTube URL in the input field

3. Select your preferred format

4. Choose the quality you want

5. Click "Download" and select where to save the file

6. Wait for the download to complete!

## Requirements

- Python 3.7 or higher
- FFmpeg (must be installed and added to system PATH)
- Internet connection

## Troubleshooting

**"FFmpeg not found" error:**
- Make sure FFmpeg is installed and added to your system PATH
- Restart your terminal/command prompt after installing FFmpeg
- Run `ffmpeg -version` to verify installation

**Download fails:**
- Check that the YouTube URL is valid
- Some videos may be region-locked or age-restricted
- Ensure you have a stable internet connection
- Try using a cookie file if you're getting authentication errors

## License

This project is for educational purposes only. Please respect YouTube's Terms of Service and copyright laws when downloading content.
