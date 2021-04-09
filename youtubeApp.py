from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pytube import YouTube, Playlist
import os
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUI()

    def setUI(self):
        self.setSetting()
        self.mainMenu()
        self.show()

    def mainMenu(self):
        widget = QWidget()
        h_box = QHBoxLayout()
        self.cb = QComboBox(self)
        text = QLabel("<b> Youtube URL: </b>")
        self.link = QLineEdit()
        self.link.setPlaceholderText('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        self.button = QPushButton(QIcon('./icons/download.png'), "Download", enabled=False)
        self.link.textChanged[str].connect(lambda: self.button.setEnabled(self.link.text().startswith("https://www.youtube.com/")))
        self.link.textChanged[str].connect(self.selectionchange)
        self.button.clicked.connect(self.download)
        self.cb.currentIndexChanged.connect(self.cb.currentText)
        h_box.addWidget(text)
        h_box.addWidget(self.link)
        h_box.addWidget(self.button)
        h_box.addWidget(self.cb)
        widget.setLayout(h_box)
        self.setCentralWidget(widget)

    def selectionchange(self):
        if self.link.text().startswith("https://www.youtube.com/playlist"):
            self.cb.clear()
            self.cb.addItems([".mp3"])
        elif self.link.text() == '':
            self.cb.clear()
        elif self.link.text().startswith("https://www.youtube.com/watch"):
            self.cb.clear()
            self.cb.addItems([".mp3", ".mp4 (1080p)", ".mp4 (720p)", ".mp4 (480p)", ".mp4 (360p)"])

    
    def download(self):
        path = QFileDialog.getExistingDirectory()
        selection = self.cb.currentText()
        url = self.link.text()
        widget = QWidget()
        h_box = QHBoxLayout()

        if 'playlist' in self.link.text():
            try:
                liste = Playlist(self.link.text())
                for videos in liste.videos:
                    if selection == '.mp3':
                        out_file = videos.streams.filter(only_audio=True).first().download(output_path=path + '/' + liste.title)
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.mp3'
                        os.rename(out_file, new_file)
                text = QLabel("<b> Playlist download successful! </b>")
                button = QPushButton(QIcon('./icons/success.png'), "Refresh App")
                h_box.addWidget(button)
                h_box.addWidget(text)

            except:
                text2 = QLabel("<b> Playlist could not be downloaded! </b>")
                button = QPushButton(QIcon('./icons/decline.jpg'), "Refresh App")
                h_box.addWidget(button)
                h_box.addWidget(text2)

            button.clicked.connect(self.mainMenu)
            widget.setLayout(h_box)
            self.setCentralWidget(widget)

        else:
            try:
                if selection == '.mp3':
                    out_file = YouTube(url).streams.filter(only_audio=True).first().download(output_path=path)
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                elif selection == '.mp4 (1080p)':
                    video = YouTube(url).streams.filter(resolution='1080p').first()
                    video.download(filename=video.title + '_' + video.resolution, output_path=path)
                elif selection == '.mp4 (720p)':
                    video = YouTube(url).streams.filter(resolution='720p').first()
                    video.download(filename=video.title + '_' + video.resolution, output_path=path)
                elif selection == '.mp4 (480p)':
                    video = YouTube(url).streams.filter(resolution='480p').first()
                    video.download(filename=video.title + '_' + video.resolution, output_path=path)
                elif selection == '.mp4 (360p)':
                    video = YouTube(url).streams.filter(progressive=True, resolution='360p').first()
                    video.download(filename=video.title + '_' + video.resolution, output_path=path)
                text = QLabel("<b> Download successful! </b>")
                button = QPushButton(QIcon('./icons/success.png'), "Refresh App")
                h_box.addWidget(button)
                h_box.addWidget(text)
            except:
                text2 = QLabel("<b> Video could not be downloaded! </b>")
                button = QPushButton(QIcon('./icons/decline.jpg'), "Refresh App")
                h_box.addWidget(button)
                h_box.addWidget(text2)
            button.clicked.connect(self.mainMenu)
            widget.setLayout(h_box)
            self.setCentralWidget(widget)

    
    def setSetting(self):
        self.setWindowTitle('Video Downloader')
        self.setWindowIcon(QIcon('./icons/icon.png'))
        self.setGeometry(250, 250, 600, 80)
        self.setMaximumSize(1000, 100)
        self.setMinimumSize(600, 80)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
