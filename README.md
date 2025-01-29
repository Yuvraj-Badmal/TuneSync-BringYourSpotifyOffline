# 🎵 TuneSync – Bring Your Spotify Offline!
Easily **download your Spotify playlists as MP3 files** using **Python, Tkinter (GUI), Spotify API, YouTube API (yt-dlp), and FFmpeg** for seamless music conversion and offline listening anytime, anywhere!  

---

## 📌 **Features**
✅ **Download Entire Playlists or Select Specific Songs**  
✅ **Simple, User-Friendly GUI – No command-line needed**  
✅ **Smart Syncing – No Duplicate Downloads**  
✅ **Fast & High-Quality MP3 Conversion (192kbps)**  
✅ **Progress Bar & Log Window – Real-time download tracking**  
✅ **Stop Downloads Anytime**  

---

## 📸 **Screenshots**
 
![image](https://github.com/user-attachments/assets/b9fb75ae-d633-438f-97ce-9f4962e9b463)

---

## 📥 **Installation Guide**
### **1️⃣ Install Dependencies**
Ensure you have **Python 3.8+** installed, then run:
```bash
pip install -r requirements.txt
```
### **2️⃣ Set Up Spotify API**
 - Go to Spotify Developer Dashboard
 - Create a new application & get Client ID & Secret
 - Update your .env file:

### **3️⃣ Set Up YouTube API (yt-dlp) & FFmpeg**
 - Install yt-dlp:
    ```bash
    pip install yt-dlp
    ```
 - Install FFmpeg (for MP3 conversion)
   https://ffmpeg.org/download.html (Windows)
   https://github.com/yt-dlp/yt-dlp/wiki/Installation (Mac/Linux)
   
### **4️⃣ Run TuneSync**
```bash
python main.py
```
--- 

### **⚙️ Usage Guide**

1️⃣ Log in with your Spotify account
2️⃣ Choose a Playlist from your library
3️⃣ Select "Download Entire Playlist" or "Select Songs to Download"
4️⃣ Wait for downloads to complete & enjoy offline!

---

### **🛠️ Tech Stack & Libraries Used**

✔ Python – Core logic & scripting
✔ Spotipy – Connects to Spotify API
✔ yt-dlp – Downloads audio from YouTube
✔ Tkinter – GUI interface
✔ FFmpeg – Converts audio to MP3
✔ Mutagen – Adds metadata to MP3 files

---

### **🚀 Future Enhancements (Next Steps)**

🔹 Web Version – Convert into a Flask/Django app for remote access
🔹 Mobile App – Build an Android/iOS version with Flutter
🔹 Cloud Storage – Save downloaded MP3s to Google Drive or Dropbox
🔹 More UI Enhancements – Dark mode, improved UX

---

### **🤝 Contributing**

Contributions are welcome! 
To contribute:
  1️⃣ Fork the repository
  2️⃣ Create a new branch (feature-new)
  3️⃣ Commit changes & open a pull request

---

### **📢 Contact & Support**

💬 Have questions or feature requests? Open an issue!
📧 Email: your.email@example.com

---
