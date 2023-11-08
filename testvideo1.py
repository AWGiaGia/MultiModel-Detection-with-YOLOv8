import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer


class VideoScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("视频截图应用")
        self.setGeometry(100, 100, 500, 400)

        self.video_label = QLabel(self)
        self.screenshot_button = QPushButton("截图", self)
        self.screenshot_button.clicked.connect(self.capture_screenshot)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.screenshot_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.video_capture = cv2.VideoCapture("下载.mp4")  # 替换为你的视频文件路径

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio)
            self.video_label.setPixmap(scaled_pixmap)

    def capture_screenshot(self):
        ret, frame = self.video_capture.read()
        if ret:
            cv2.imwrite("screenshot.png", frame)  # 替换为你想要保存截图的路径
            print("截图已保存！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoScreenshotApp()
    window.show()
    app.exec_()
