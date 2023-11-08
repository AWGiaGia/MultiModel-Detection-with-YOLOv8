import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class VideoPlayerWindow(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.current_frame = 0
        # 打开视频文件
        self.video = cv2.VideoCapture(self.video_path)
        # 检查视频是否成功打开
        if not self.video.isOpened():
            print("无法打开视频文件")
            return
        # 读取第一帧图像
        self.ret, self.frame = self.video.read()
        # 设置窗口标题和大小
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, self.frame.shape[1], self.frame.shape[0])
        # 创建帧标签并设置位置
        self.frame_label = QLabel(self)
        self.frame_label.setGeometry(0, 0, self.frame.shape[1], self.frame.shape[0])
        # 创建上一帧和下一帧按钮
        previous_button = QPushButton("Previous", self)
        previous_button.setGeometry(20, 20, 100, 30)
        previous_button.clicked.connect(self.previous_frame)
        next_button = QPushButton("Next", self)
        next_button.setGeometry(130, 20, 100, 30)
        next_button.clicked.connect(self.next_frame)
        # 显示第一帧图像
        self.show_frame()

    def show_frame(self):
        # 将OpenCV图像转换为Qt图像并显示到帧标签中
        rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_image.shape
        q_image = QImage(rgb_image.data, w, h, c * w, QImage.Format_RGB888)
        self.frame_label.setPixmap(QPixmap.fromImage(q_image))

    def previous_frame(self):
        if self.current_frame > 10:
            self.current_frame -= 10
        elif 0 < self.current_frame <= 10:
            self.current_frame = 0
        else:
            self.current_frame = 0
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        self.ret, self.frame = self.video.read()
        self.show_frame()
        print("上一帧")

    def next_frame(self):
        self.current_frame += 10
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        self.ret, self.frame = self.video.read()
        self.show_frame()
        print("下一帧")

    def closeEvent(self, event):
        # 释放资源
        self.video.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 实例化视频播放窗口并播放视频
    player_window = VideoPlayerWindow("下载.mp4")
    player_window.show()

    sys.exit(app.exec_())
