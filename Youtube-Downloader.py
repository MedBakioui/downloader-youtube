import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import yt_dlp as youtube_dl
import os
import webbrowser
import re  # Pour nettoyer les codes ANSI

# Configuration de l'apparence
ctk.set_appearance_mode("Dark")  # Mode sombre par défaut
ctk.set_default_color_theme("green")  # Thème: "blue" (default), "green", "dark-blue"

def clean_ansi_codes(text):
    """Supprime les codes ANSI d'une chaîne de caractères."""
    ansi_escape = re.compile(r'\x1b\[([0-9;]*[mGKH])')
    return ansi_escape.sub('', text)

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("900x700")  # Taille initiale de la fenêtre
        self.root.minsize(800, 600)  # Taille minimale de la fenêtre
        self.root.resizable(True, True)  # Permettre le redimensionnement

        # Variables
        self.url = ctk.StringVar()
        self.download_folder = ctk.StringVar(value=os.getcwd())
        self.downloading = False

        # Interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=15, fg_color="#2E2E2E")
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        # Configuration des poids des lignes et colonnes
        for i in range(8):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)

        # Titre de l'application
        ctk.CTkLabel(main_frame, text="YouTube Downloader Pro", font=("Arial", 28, "bold"), text_color="#3498DB").grid(
            row=0, column=0, columnspan=3, pady=(20, 30), sticky="nsew"
        )

        # Widgets d'entrée et de sélection
        self.create_inputs(main_frame)

        # Zone de logs avec barre de défilement
        self.log_area = ctk.CTkTextbox(main_frame, wrap=ctk.WORD, font=("Arial", 12), fg_color="#1E1E1E", text_color="#EAECEE")
        self.log_area.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Barre de progression
        self.progress_bar = ctk.CTkProgressBar(main_frame, orientation="horizontal", mode="determinate", fg_color="#1E1E1E", progress_color="#3498DB")
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.progress_bar.set(0)

        # Boutons de contrôle
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=7, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Bouton Télécharger
        ctk.CTkButton(button_frame, text="Télécharger", command=self.start_download, font=("Arial", 16, "bold"), fg_color="#27AE60", hover_color="#229954").pack(
            side="left", expand=True, padx=5, pady=5
        )

        # Bouton Annuler
        ctk.CTkButton(button_frame, text="Annuler", command=self.cancel_download, font=("Arial", 16, "bold"), fg_color="#E74C3C", hover_color="#C0392B").pack(
            side="left", expand=True, padx=5, pady=5
        )

        # Boutons supplémentaires
        ctk.CTkButton(main_frame, text="Ouvrir le dossier", command=self.open_download_folder, fg_color="#3498DB", hover_color="#2980B9", font=("Arial", 14)).grid(
            row=8, column=1, pady=10, padx=5, sticky="ew"
        )
        ctk.CTkButton(main_frame, text="Aide", command=self.open_help, fg_color="#3498DB", hover_color="#2980B9", font=("Arial", 14)).grid(
            row=8, column=2, pady=10, padx=5, sticky="ew"
        )

    def create_inputs(self, frame):
        """Créer les champs d'entrée et de sélection."""
        ctk.CTkLabel(frame, text="URL de la vidéo YouTube :", font=("Arial", 16), text_color="#EAECEE").grid(
            row=1, column=0, sticky="w", padx=10, pady=10
        )
        ctk.CTkEntry(frame, textvariable=self.url, font=("Arial", 14), fg_color="#1E1E1E", border_color="#3498DB", text_color="#EAECEE").grid(
            row=1, column=1, columnspan=2, sticky="ew", padx=10, pady=10
        )

        ctk.CTkLabel(frame, text="Format :", font=("Arial", 16), text_color="#EAECEE").grid(
            row=2, column=0, sticky="w", padx=10, pady=10
        )
        self.format_combobox = ctk.CTkComboBox(
            frame,
            values=["mp4", "mp3", "wav", "mkv"],
            font=("Arial", 14),
            fg_color="#1E1E1E",
            button_color="#3498DB",
            dropdown_fg_color="#1E1E1E",
            text_color="#EAECEE",
            command=self.update_quality_options  # Mettre à jour les options de qualité
        )
        self.format_combobox.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
        self.format_combobox.set("mp4")

        ctk.CTkLabel(frame, text="Qualité :", font=("Arial", 16), text_color="#EAECEE").grid(
            row=3, column=0, sticky="w", padx=10, pady=10
        )
        self.quality_combobox = ctk.CTkComboBox(
            frame,
            values=[],  # Les options seront mises à jour dynamiquement
            font=("Arial", 14),
            fg_color="#1E1E1E",
            button_color="#3498DB",
            dropdown_fg_color="#1E1E1E",
            text_color="#EAECEE"
        )
        self.quality_combobox.grid(row=3, column=1, sticky="ew", padx=10, pady=10)
        self.update_quality_options()  # Initialiser les options de qualité

        ctk.CTkLabel(frame, text="Dossier de téléchargement :", font=("Arial", 16), text_color="#EAECEE").grid(
            row=4, column=0, sticky="w", padx=10, pady=10
        )
        ctk.CTkEntry(frame, textvariable=self.download_folder, font=("Arial", 14), fg_color="#1E1E1E", border_color="#3498DB", text_color="#EAECEE").grid(
            row=4, column=1, sticky="ew", padx=10, pady=10
        )
        ctk.CTkButton(frame, text="Parcourir", command=self.browse_folder, font=("Arial", 14), fg_color="#3498DB", hover_color="#2980B9").grid(
            row=4, column=2, padx=10, pady=10, sticky="ew"
        )

    def update_quality_options(self, event=None):
        """Met à jour les options de qualité en fonction du format sélectionné."""
        format_selected = self.format_combobox.get()
        if format_selected in ["mp3", "wav"]:
            # Options de qualité audio
            self.quality_combobox.configure(values=["128k", "192k", "256k", "320k"])
            self.quality_combobox.set("192k")  # Qualité par défaut pour l'audio
        else:
            # Options de qualité vidéo
            self.quality_combobox.configure(values=["best", "2160p", "1440p", "1080p", "720p", "480p", "360p"])
            self.quality_combobox.set("best")  # Qualité par défaut pour la vidéo

    def browse_folder(self):
        """Ouvrir une boîte de dialogue pour sélectionner un dossier."""
        folder = filedialog.askdirectory()
        if folder:
            self.download_folder.set(folder)

    def open_download_folder(self):
        """Ouvrir le dossier de téléchargement dans l'explorateur de fichiers."""
        if os.path.exists(self.download_folder.get()):
            os.startfile(self.download_folder.get())
        else:
            messagebox.showwarning("Dossier introuvable", "Le dossier de téléchargement spécifié n'existe pas.")

    def open_help(self):
        """Ouvrir une page d'aide ou un guide utilisateur."""
        webbrowser.open("https://github.com/yt-dlp/yt-dlp")

    def start_download(self):
        """Démarrer le téléchargement de la vidéo."""
        if self.downloading:
            messagebox.showwarning("Attention", "Un téléchargement est déjà en cours.")
            return

        url = self.url.get()
        if not url or not url.startswith("http"):
            messagebox.showerror("Erreur", "Veuillez entrer une URL valide.")
            return

        self.downloading = True
        self.log_area.insert(ctk.END, "Début du téléchargement...\n")

        format_selected = self.format_combobox.get()
        quality_selected = self.quality_combobox.get()
        ydl_opts = {
            'format': self.get_format_string(format_selected, quality_selected),
            'outtmpl': os.path.join(self.download_folder.get(), '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
        }

        if format_selected in ["mp3", "wav"]:
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': format_selected, 'preferredquality': quality_selected.strip('k')}]

        threading.Thread(target=self.download_video, args=(url, ydl_opts), daemon=True).start()

    def get_format_string(self, format_selected, quality_selected):
        """Retourne la chaîne de format pour yt-dlp en fonction de la qualité sélectionnée."""
        if format_selected in ["mp3", "wav"]:
            return "bestaudio/best"  # Télécharger le meilleur format audio
        else:
            format_map = {
                "2160p": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",  # 4K
                "1440p": "bestvideo[height<=1440]+bestaudio/best[height<=1440]",  # 1440p
                "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
                "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                "best": "best",
            }
            return format_map.get(quality_selected, "best")

    def download_video(self, url, ydl_opts):
        """Télécharger la vidéo avec yt-dlp."""
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.log_area.insert(ctk.END, "Téléchargement terminé avec succès !\n")
        except Exception as e:
            self.log_area.insert(ctk.END, f"Erreur : {str(e)}\n")
        finally:
            self.downloading = False
            self.progress_bar.set(0)

    def progress_hook(self, d):
        """Mettre à jour les logs et la barre de progression pendant le téléchargement."""
        if d['status'] == 'downloading':
            # Nettoyer les codes ANSI de la chaîne de pourcentage
            percent_str = clean_ansi_codes(d['_percent_str'])
            try:
                percent = float(percent_str.strip('%')) / 100
                self.progress_bar.set(percent)
                self.log_area.insert(ctk.END, f"Téléchargement : {percent_str} - {d['_speed_str']}\n")
            except ValueError:
                self.log_area.insert(ctk.END, f"Erreur de conversion du pourcentage : {percent_str}\n")
        elif d['status'] == 'finished':
            self.log_area.insert(ctk.END, "Conversion en cours...\n")

    def cancel_download(self):
        """Annuler le téléchargement en cours."""
        if self.downloading:
            self.downloading = False
            self.log_area.insert(ctk.END, "Téléchargement annulé.\n")
            self.progress_bar.set(0)
        else:
            messagebox.showinfo("Info", "Aucun téléchargement en cours.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()