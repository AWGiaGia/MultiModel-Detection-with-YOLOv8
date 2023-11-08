import os
import subprocess
from PyQt5 import QtGui, QtCore
from PyQt5.Qt import *
import sys
from Window.home_page import Ui_MainWindow
from Window import window1
from Window import window2
from Window import window3
from Night_DenseFuse.inference_new_pth import image_fusion
from PyQt5.QtMultimedia import QVideoSurfaceFormat
import cv2
import yaml

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Window/窗口.png"))
        self.setFixedSize(500, 400)
        self.process = QProcess(self)
        self.window1 = Window1(self)
        self.window2 = Window2(self)
        self.window3 = Window3(self)

    @pyqtSlot()
    def on_image_annotation_pushButton_clicked(self):
        if self.process.start() == QProcess.Running:
            return
        labelimg_path = "labelImg.exe"
        self.process.start(labelimg_path)

    @pyqtSlot()
    def on_modal_fusion_pushButton_clicked(self):
        self.close()
        self.window1.show()
        self.window1.start_play()
        self.window1.raise_()

    @pyqtSlot()
    def on_data_processing_pushButton_clicked(self):
        self.close()
        self.window2.show()
        self.window2.raise_()

    @pyqtSlot()
    def on_target_detection_pushButton_clicked(self):
        self.close()
        self.window3.show()
        self.window3.raise_()


class Window1(QMainWindow, window1.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window1, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Window/窗口.png"))
        self.setFixedSize(940, 500)
        self.parent = parent

    @pyqtSlot()
    def on_pushButton_clicked(self):
        video_file_path, _ = QFileDialog.getOpenFileName(self,
                                                         "选择视频文件",
                                                         "",
                                                         "mp4 File(*.mp4)")
        if video_file_path != "":
            self.video_widget.load_file(video_file_path)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        video_file_path, _ = QFileDialog.getOpenFileName(self,
                                                         "选择视频文件",
                                                         "",
                                                         "mp4 File(*.mp4)")
        if video_file_path != "":
            self.video_widget_2.load_file(video_file_path)

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        # self.video_widget.save_pix(r"Cache\images\channel1\video1.png")
        # self.video_widget_2.save_pix(r"Cache\images\channel2\video2.png")
        from Night_DenseFuse.inference_new_pth import image_fusion
        output_path = image_fusion(r"Cache\images\channel1\video1.jpg", r"Cache\images\channel2\video2.jpg")
        pix = QPixmap(output_path)
        self.video_widget_3.setPixmap(pix.scaled(self.video_widget_3.size(), Qt.KeepAspectRatio))

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        self.video_widget_3.clear()
        self.video_widget_3.load_file(file_path="下载.mp4")

    def start_play(self):
        self.video_widget.start()
        self.video_widget_2.start()
        self.video_widget_3.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.video_widget.stop()
        self.video_widget_2.stop()
        self.video_widget_3.stop()
        self.close()
        self.parent.show()


class MyCVVideo(QThread):
    def __init__(self, video_path):
        super(MyCVVideo, self).__init__()
        self.video_path = video_path
        self.paused = False
        self.frame = None

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while True:
            if not self.paused:
                ret, frame = cap.read()
                if not ret:
                    break
                self.frame = frame
        cap.release()


class Window2(QMainWindow, window2.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window2, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Window/窗口.png"))
        self.parent = parent
        self.original_voc_path = None
        self.txtpath = None
        self.data_path = None
        self.original_data_path = None
        self.enhance_data_path = None
        self.current_count = None
        self.pix_list = []
        self.setFixedSize(700, 600)
        self.label_9.setFixedSize(500, 300)
        self.pushButton_2.setHidden(True)
        for label in [self.label_5, self.label_6, self.label_7]:
            label.setFixedWidth(100)
        for lineedit in [self.lineEdit_3, self.lineEdit_4, self.lineEdit_5, self.lineEdit_7]:
            lineedit.setValidator(QIntValidator(0, 100))
        for lineedit in [self.lineEdit_8]:
            lineedit.setValidator(QDoubleValidator(0.00, 1.00, 2))
        for key, value in {self.pushButton_6: "Window/左.png", self.pushButton_7: "Window/右.png"}.items():
            key.setIcon(QIcon(value))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        original_voc_path = QFileDialog.getExistingDirectory(self, "原始VOC格式文件夹地址")
        if original_voc_path != "":
            self.original_voc_path = original_voc_path

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        txtpath = QFileDialog.getExistingDirectory(self, "转换数据保存地址")
        if txtpath != "":
            self.txtpath = txtpath

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        if self.original_voc_path is None:
            QMessageBox.warning(self, "Warning", "请选择原始VOC格式文件夹地址!", QMessageBox.Ok)
            return
        from dataset.xml2txt import xml_to_txt
        xml_to_txt(self.original_voc_path)
        QMessageBox.information(self, "Succeed", "数据格式转换成功", QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        data_path = QFileDialog.getExistingDirectory(self, "数据文件夹地址")
        if data_path != "":
            self.data_path = data_path

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        proportion_list = []
        for key, value in {self.lineEdit_3: "请输入训练集比例", self.lineEdit_4: "请输入测试集比例",
                           self.lineEdit_5: "请输入验证集比例"}.items():
            if key.text().strip() == "":
                QMessageBox.warning(self, "Warning", value, QMessageBox.Ok)
                return
            proportion_list.append(float(int(key.text()) / 100))
        if self.data_path is None:
            QMessageBox.warning(self, "Warning", "请选择数据文件夹地址", QMessageBox.Ok)
            return
        from dataset.split_data import split_data
        split_data(proportion_list[0], proportion_list[1], proportion_list[2], self.data_path)
        QMessageBox.information(self, "Succeed", "数据划分转换成功", QMessageBox.Ok)

    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        original_data_path = QFileDialog.getExistingDirectory(self, "原始数据文件夹地址")
        if original_data_path != "":
            self.original_data_path = original_data_path

    @pyqtSlot()
    def on_pushButton_10_clicked(self):
        enhance_data_path = QFileDialog.getExistingDirectory(self, "增强数据保存地址")
        if enhance_data_path != "":
            self.enhance_data_path = enhance_data_path

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        if self.current_count is None:
            return
        if len(self.pix_list) == 0:
            return
        if self.current_count <= 0:
            self.current_count = len(self.pix_list) - 1
        else:
            self.current_count -= 1
        self.label_9.clear()
        pix = QPixmap(self.pix_list[self.current_count])
        self.label_9.setPixmap(pix.scaled(self.label_9.size(), Qt.KeepAspectRatio))
        print(self.pix_list[self.current_count])

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        if self.current_count is None:
            return
        if len(self.pix_list) == 0:
            return
        if self.current_count >= len(self.pix_list) - 1:
            self.current_count = 0
        else:
            self.current_count += 1
        self.label_9.clear()
        pix = QPixmap(self.pix_list[self.current_count])
        self.label_9.setPixmap(pix.scaled(self.label_9.size(), Qt.KeepAspectRatio))
        print(self.pix_list[self.current_count])

    @pyqtSlot()
    def on_pushButton_11_clicked(self):
        for key, value in {self.original_data_path: "请选择原始数据文件夹地址",
                           self.enhance_data_path: "请选择增强数据保存地址",
                           self.lineEdit_7.text().strip(): "请输入增强倍率",
                           self.lineEdit_8.text().strip(): "请输入增强概率"}.items():
            if key is None or key == "":
                QMessageBox.warning(self, "Warning", value, QMessageBox.Ok)
                return
        from dataset.augmentation import data_enhancement
        AUG_IMG_DIR = data_enhancement(self.original_data_path, self.enhance_data_path,
                                       int(self.lineEdit_7.text().strip()),
                                       float(self.lineEdit_8.text().strip()))
        for file_name in os.listdir(AUG_IMG_DIR):
            absolute_path = os.path.join(AUG_IMG_DIR, file_name)
            if os.path.isfile(absolute_path):
                self.pix_list.append(absolute_path)
        if len(self.pix_list) != 0:
            self.current_count = 0
            pix = QPixmap(self.pix_list[self.current_count])
            self.label_9.setPixmap(pix.scaled(self.label_9.size(), Qt.KeepAspectRatio))

    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        if self.current_count is None:
            return
        if len(self.pix_list) == 0:
            return
        remove_path = self.pix_list[self.current_count]
        del self.pix_list[self.current_count]
        if self.current_count != 0:
            self.current_count -= 1
        else:
            self.current_count = len(self.pix_list) - 1
        pix = QPixmap(self.pix_list[self.current_count])
        self.label_9.setPixmap(pix.scaled(self.label_9.size(), Qt.KeepAspectRatio))
        os.remove(remove_path)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close()
        self.parent.show()


class Window3(QMainWindow, window3.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window3, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Window/窗口.png"))
        self.parent = parent
        self.train_data = None
        self.train_result_save = None
        self.reasoning_data = None
        self.model_select = None
        self.reasoning_result_save = None
        self.pix_list = []
        self.current_count = None
        self.setFixedSize(700, 400)
        self.pushButton_5.setText("开始推理")
        self.label_10.setAlignment(Qt.AlignCenter)
        self.label_7.fps_signal.connect(self.change_fps)
        for key, value in {self.pushButton_7: "Window/左.png", self.pushButton_8: "Window/右.png"}.items():
            key.setIcon(QIcon(value))

    def change_fps(self, fps):
        self.label_10.setText(fps)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        train_data = QFileDialog.getExistingDirectory(self, "训练数据地址")
        if train_data != "":
            self.train_data = train_data

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        result_save = QFileDialog.getExistingDirectory(self, "结果保存地址")
        if result_save != "":
            self.train_result_save = result_save

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        reasoning_data = QFileDialog.getExistingDirectory(self, "推理数据地址")
        if reasoning_data != "":
            self.reasoning_data = reasoning_data

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        model_select, _ = QFileDialog.getOpenFileName(self,
                                                      "模型选择地址",
                                                      "")
        if model_select != "":
            self.model_select = model_select

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        for key, value in {self.reasoning_result_save: "请选择结果保存地址",
                           self.model_select: "请选择模型数据地址"}.items():
            if key is None:
                QMessageBox.warning(self, "Warning", value, QMessageBox.Ok)
                return
        with open("detect.yaml", "r") as fp:
            result = yaml.safe_load(fp)
        result["model"] = self.model_select
        result["source"] = self.reasoning_data
        with open("default.yaml", "w") as fp:
            yaml.dump(result, fp)
        result = subprocess.run("yolo cfg=detect.yaml", capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
        print(output)
        print(error)

    @pyqtSlot()
    def on_run_pushbutton_clicked(self):
        for key, value in {self.train_data: "请选择训练数据地址", self.train_result_save: "请选择结果保存地址",
                           self.lineEdit.text(): "请输入epochs", self.lineEdit_2.text(): "请输入seed",
                           self.lineEdit_3.text(): "请输入nc", self.lineEdit_4.text(): "请输入names"}.items():
            if key is None or key == "":
                QMessageBox.warning(self, "Warning", value, QMessageBox.Ok)
                return
        with open("default.yaml", "r") as fp:
            result = yaml.safe_load(fp)
        result["epochs"] = int(self.lineEdit.text())
        result["project"] = self.train_result_save
        result["optimizer"] = self.comboBox.currentText()
        current_file = os.path.abspath(__file__)
        result["data"] = os.path.join(os.path.dirname(current_file), "my_own_data.yaml")
        result["seed"] = int(self.lineEdit_2.text())
        with open("default.yaml", "w") as fp:
            yaml.dump(result, fp)
        with open("my_own_data.yaml", "r") as fp:
            result = yaml.safe_load(fp)
        result["train"] = os.path.join(self.train_data, 'images\\train')
        result["val"] = os.path.join(self.train_data, 'images\\val')
        result["test"] = os.path.join(self.train_data, 'images\\test')
        result["nc"] = int(self.lineEdit_3.text())
        result["names"] = list(self.lineEdit_4.text().split(","))
        """
        F:/RSEdge/yolo_source_data
        F:/RSEdge/yolo_target_file
        people,people1,people2,people3
        """
        with open("my_own_data.yaml", "w") as fp:
            yaml.safe_dump(result, fp, default_flow_style=False)
        # working_directory = os.path.join(os.path.dirname(current_file), "default.yaml")  # 指定正确的工作目录
        working_directory = os.path.dirname(current_file) # 指定正确的工作目录
        result = subprocess.run("yolo cfg=default.yaml", capture_output=True, text=True, cwd=working_directory)
        output = result.stdout
        error = result.stderr
        print("正确输出", output)
        print("异常输出", error)
        # print(self.train_data)
        # print(self.train_result_save)
        QMessageBox.information(self, "成功", "训练结束")

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        video_file_path, _ = QFileDialog.getOpenFileName(self,
                                                         "选择视频文件",
                                                         "",
                                                         "mp4 File(*.mp4)")
        if video_file_path != "":
            self.label_7.load_file(video_file_path, state=0)

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        self.label_7.previous_frame()

    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        self.label_7.next_frame()

    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        video_file_path, _ = QFileDialog.getOpenFileName(self,
                                                         "选择视频文件",
                                                         "",
                                                         "mp4 File(*.mp4)")
        if video_file_path != "":
            self.label_7.load_file(video_file_path, state=1)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.label_7.stop()
        self.close()
        self.parent.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
