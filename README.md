# YouTube Downloader Pro

A simple and user-friendly YouTube video/audio downloader built with Python and `customtkinter`. This application allows you to download YouTube videos or extract audio in various formats (mp4, mp3, wav, mkv) and qualities.

---

## Features

- Download YouTube videos in multiple formats: `mp4`, `mkv`, `mp3`, `wav`.
- Choose video quality: `2160p`, `1440p`, `1080p`, `720p`, `480p`, `360p`, or `best`.
- Choose audio quality: `128k`, `192k`, `256k`, `320k`.
- Select a custom download folder.
- Real-time progress bar and logs.
- Dark mode and modern UI using `customtkinter`.
- Open the download folder directly from the app.
- Cancel downloads in progress.

---

## Requirements

- Python 3.7 or higher.
- Required Python libraries:
  - `customtkinter`
  - `yt-dlp`
  - `webbrowser` (built-in)
  - `os` (built-in)
  - `re` (built-in)
  - `threading` (built-in)

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/MedBakioui/downloader-youtube.git>
   cd downloader-youtube

```

1. **Install the required libraries**:
    
    ```bash
    pip install customtkinter yt-dlp
    
    ```
    
2. **Run the application**:
    
    ```bash
    python Youtube-Downloader.py
    
    ```
    

---

## Usage

1. **Enter the YouTube video URL** in the provided field.
2. **Select the desired format** (e.g., `mp4`, `mp3`).
3. **Choose the quality** (e.g., `1080p`, `192k`).
4. **Select the download folder** (default is the current working directory).
5. Click **Télécharger** (Download) to start the download.
6. Monitor the progress in the logs and progress bar.
7. Once the download is complete, you can open the folder directly using the **Ouvrir le dossier** (Open Folder) button.

---

## Notes

- The application uses `yt-dlp`, a powerful YouTube downloader library.
- For audio formats (`mp3`, `wav`), the video is first downloaded and then converted using `FFmpeg` (automatically handled by `yt-dlp`).
- The app supports canceling downloads in progress.

---

## Troubleshooting

- **Invalid URL**: Ensure the URL starts with `http` or `https`.
- **Download folder not found**: Make sure the specified folder exists.
- **Dependencies not installed**: Run `pip install -r requirements.txt` to install all required libraries.

---

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## Author

- [Med Bakioui](https://github.com/MedBakioui)

---

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for the YouTube downloader backend.
- [customtkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI.