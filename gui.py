import threading
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext, Frame, Canvas
from spotify_handler import get_user_playlists, get_playlist_tracks, load_downloaded_songs
from youtube_handler import search_youtube, download_audio
import os
from config import DOWNLOADS_FOLDER

class TuneSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TuneSync - Bring Your Spotify Offline!")

        self.playlist_choices = get_user_playlists()
        self.selected_playlist = tk.StringVar(root)

        tk.Label(root, text="Select a Playlist:", font=("Arial", 12)).pack(pady=5)
        self.playlist_dropdown = tk.OptionMenu(root, self.selected_playlist, *self.playlist_choices.keys())
        self.playlist_dropdown.pack(pady=5)

        self.song_selection_window = None  
        self.song_checkboxes = {}  

        # Buttons for choosing download method
        self.download_all_button = tk.Button(root, text="Download Entire Playlist", command=self.download_entire_playlist, bg="green", fg="white")
        self.download_all_button.pack(pady=5)

        self.select_songs_button = tk.Button(root, text="Select Songs to Download", command=self.fetch_songs, bg="blue", fg="white")
        self.select_songs_button.pack(pady=5)

        # Stop Download Button
        self.stop_button = tk.Button(root, text="Stop Download", command=self.stop_download, bg="red", fg="white", state="disabled")
        self.stop_button.pack(pady=5)

        self.log_text = scrolledtext.ScrolledText(root, height=10, width=60, state="disabled")
        self.log_text.pack(pady=5)

        self.progress = ttk.Progressbar(root, length=400, mode='determinate')
        self.progress.pack(pady=5)

        self.stop_flag = False

    def log(self, message):
        """ Append messages to the log window safely in the main thread. """
        self.root.after(0, self._update_log, message)

    def _update_log(self, message):
        """ Updates the log in the main thread """
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state="disabled")
        self.log_text.yview(tk.END)

    def fetch_songs(self):
        """ Fetches the songs in the selected playlist and allows the user to select which to download. """
        playlist_name = self.selected_playlist.get()
        if not playlist_name:
            messagebox.showerror("Error", "Please select a playlist!")
            return

        playlist_id = self.playlist_choices[playlist_name]
        tracks = get_playlist_tracks(playlist_id)

        # Create a new window for song selection
        self.song_selection_window = tk.Toplevel(self.root)
        self.song_selection_window.title("Select Songs to Download")

        frame = Frame(self.song_selection_window)
        frame.pack(fill="both", expand=True)

        canvas = Canvas(frame)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        scrollable_frame = Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(scrollable_frame, text="Select Songs:", font=("Arial", 12)).pack(pady=5)

        self.song_checkboxes = {}

        for track in tracks:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(scrollable_frame, text=f"{track['name']} - {track['artist']}", variable=var)
            cb.pack(anchor="w")
            self.song_checkboxes[track["name"]] = var

        # OK Button to confirm selection
        tk.Button(scrollable_frame, text="OK", command=self.start_selected_download, bg="green", fg="white").pack(pady=10)

    def download_entire_playlist(self):
        """ Downloads all songs in the selected playlist. """
        playlist_name = self.selected_playlist.get()
        if not playlist_name:
            messagebox.showerror("Error", "Please select a playlist!")
            return

        playlist_id = self.playlist_choices[playlist_name]
        self.stop_flag = False
        self.stop_button.config(state="normal")

        threading.Thread(target=self.download_songs, args=(playlist_id, None)).start()

    def start_selected_download(self):
        """ Starts downloading only the selected songs. """
        selected_songs = [song for song, var in self.song_checkboxes.items() if var.get()]

        if not selected_songs:
            messagebox.showerror("Error", "No songs selected for download!")
            return

        #  Close the selection window immediately
        self.song_selection_window.destroy()

        #  Directly start downloading selected songs
        playlist_name = self.selected_playlist.get()
        playlist_id = self.playlist_choices[playlist_name]
        self.stop_flag = False
        self.stop_button.config(state="normal")

        threading.Thread(target=self.download_songs, args=(playlist_id, selected_songs)).start()

    def stop_download(self):
        """ Stops the download process immediately. """
        self.stop_flag = True
        self.log("❌ Download Stopped.")
        self.stop_button.config(state="disabled")

    def download_songs(self, playlist_id, selected_songs):
        """ Downloads either the entire playlist or only selected songs. """
        tracks = get_playlist_tracks(playlist_id)

        if selected_songs:
            tracks = [track for track in tracks if track["name"] in selected_songs]

        total_songs = len(tracks)

        for idx, track in enumerate(tracks):
            if self.stop_flag:
                self.log("❌ Download Stopped.")
                break

            youtube_url = search_youtube(track["name"], track["artist"])

            if youtube_url:
                self.log(f"🎵 Downloading: {track['name']} by {track['artist']}")

                self.progress["value"] = (idx + 1) / total_songs * 100
                self.root.after(0, self.progress.update_idletasks)

                download_audio(youtube_url, track["name"])

        self.log("✅ Download Complete!")
        messagebox.showinfo("Success", "Download Complete!")
        self.stop_button.config(state="disabled")

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = TuneSyncApp(root)
    root.mainloop()
