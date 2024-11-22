import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFileDialog,
                           QComboBox, QSpinBox, QDialog, QDialogButtonBox,
                           QFormLayout, QMessageBox)
from PyQt6.QtGui import QPixmap, QImage, QColor, QGuiApplication
from PyQt6.QtCore import Qt, QPoint
from PIL import Image

class GenerateColorImageDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('生成纯色图片')
        layout = QFormLayout(self)
        
        # 预设比例选择
        self.ratio_combo = QComboBox()
        self.ratio_combo.addItems(['自定义', '16:9', '4:3', '1:1', '3:2', '9:16'])
        self.ratio_combo.currentTextChanged.connect(self.onRatioChanged)
        layout.addRow('图片比例:', self.ratio_combo)
        
        # 宽度输入
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 7680)  # 支持到8K分辨率
        self.width_spin.setValue(1920)
        self.width_spin.valueChanged.connect(self.onWidthChanged)
        layout.addRow('宽度 (像素):', self.width_spin)
        
        # 高度输入
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 4320)  # 支持到8K分辨率
        self.height_spin.setValue(1080)
        layout.addRow('高度 (像素):', self.height_spin)
        
        # 确定和取消按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
        
    def onRatioChanged(self, ratio):
        if ratio != '自定义':
            width = self.width_spin.value()
            if ratio == '16:9':
                self.height_spin.setValue(width * 9 // 16)
            elif ratio == '4:3':
                self.height_spin.setValue(width * 3 // 4)
            elif ratio == '1:1':
                self.height_spin.setValue(width)
            elif ratio == '3:2':
                self.height_spin.setValue(width * 2 // 3)
            elif ratio == '9:16':
                self.height_spin.setValue(width * 16 // 9)
                
    def onWidthChanged(self, width):
        ratio = self.ratio_combo.currentText()
        if ratio != '自定义':
            self.onRatioChanged(ratio)
            
    def getValues(self):
        return self.width_spin.value(), self.height_spin.value()

class ColorPicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None
        self.pixmap = None
        self.current_rgb = None
        self.current_hex = None
        self.current_color = None
        
    def initUI(self):
        self.setWindowTitle('颜色选择器')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建顶部按钮
        btn_layout = QHBoxLayout()
        self.open_btn = QPushButton('打开图片', self)
        self.open_btn.clicked.connect(self.openImage)
        btn_layout.addWidget(self.open_btn)
        layout.addLayout(btn_layout)
        
        # 创建图片显示区域
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        layout.addWidget(self.image_label)
        
        # 创建颜色信息显示区域
        color_info_layout = QHBoxLayout()
        
        # 颜色预览
        self.color_preview = QLabel(self)
        self.color_preview.setFixedSize(50, 50)
        self.color_preview.setStyleSheet("background-color: white; border: 1px solid black;")
        color_info_layout.addWidget(self.color_preview)
        
        # 颜色信息和复制按钮的垂直布局
        color_info_buttons_layout = QVBoxLayout()
        
        # RGB信息和复制按钮
        rgb_layout = QHBoxLayout()
        self.rgb_label = QLabel('RGB: -')
        rgb_layout.addWidget(self.rgb_label)
        self.copy_rgb_btn = QPushButton('复制RGB', self)
        self.copy_rgb_btn.clicked.connect(self.copyRGB)
        self.copy_rgb_btn.setEnabled(False)
        rgb_layout.addWidget(self.copy_rgb_btn)
        color_info_buttons_layout.addLayout(rgb_layout)
        
        # HEX信息和复制按钮
        hex_layout = QHBoxLayout()
        self.hex_label = QLabel('HEX: -')
        hex_layout.addWidget(self.hex_label)
        self.copy_hex_btn = QPushButton('复制HEX', self)
        self.copy_hex_btn.clicked.connect(self.copyHEX)
        self.copy_hex_btn.setEnabled(False)
        hex_layout.addWidget(self.copy_hex_btn)
        color_info_buttons_layout.addLayout(hex_layout)
        
        # 添加生成纯色图片按钮
        generate_layout = QHBoxLayout()
        self.generate_btn = QPushButton('生成纯色图片', self)
        self.generate_btn.clicked.connect(self.generateColorImage)
        self.generate_btn.setEnabled(False)
        generate_layout.addWidget(self.generate_btn)
        color_info_buttons_layout.addLayout(generate_layout)
        
        color_info_layout.addLayout(color_info_buttons_layout)
        layout.addLayout(color_info_layout)
        
        # 鼠标位置显示
        self.pos_label = QLabel('位置: x: - y: -')
        layout.addWidget(self.pos_label)
        
        # 设置鼠标追踪
        self.image_label.setMouseTracking(True)
        self.image_label.mouseMoveEvent = self.onMouseMove
        self.image_label.mousePressEvent = self.onMouseClick
        
    def copyToClipboard(self, text):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(text)
        
    def copyRGB(self):
        if self.current_rgb:
            self.copyToClipboard(self.current_rgb)
            
    def copyHEX(self):
        if self.current_hex:
            self.copyToClipboard(self.current_hex)
            
    def openImage(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_name:
            self.image = Image.open(file_name)
            pixmap = QPixmap(file_name)
            
            # 调整图片大小以适应窗口
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.image_label.setPixmap(scaled_pixmap)
            self.pixmap = scaled_pixmap
            
    def getColorAtPosition(self, pos):
        if not self.pixmap:
            return None
            
        # 获取图片在Label中的实际位置和大小
        img_rect = self.image_label.pixmap().rect()
        label_rect = self.image_label.rect()
        
        # 计算图片在Label中的偏移量（居中显示）
        x_offset = (label_rect.width() - img_rect.width()) // 2
        y_offset = (label_rect.height() - img_rect.height()) // 2
        
        # 调整鼠标位置
        adjusted_x = pos.x() - x_offset
        adjusted_y = pos.y() - y_offset
        
        # 检查是否在图片范围内
        if (0 <= adjusted_x < img_rect.width() and 
            0 <= adjusted_y < img_rect.height()):
            # 将QPixmap转换为QImage以获取颜色
            image = self.pixmap.toImage()
            color = QColor(image.pixel(adjusted_x, adjusted_y))
            return color
        return None
            
    def onMouseMove(self, event):
        if not self.pixmap:
            return
            
        pos = event.pos()
        self.pos_label.setText(f'位置: x: {pos.x()} y: {pos.y()}')
        
        color = self.getColorAtPosition(pos)
        if color:
            self.updateColorInfo(color)
            
    def onMouseClick(self, event):
        if not self.pixmap:
            return
            
        pos = event.pos()
        color = self.getColorAtPosition(pos)
        if color:
            self.updateColorInfo(color)
            
    def updateColorInfo(self, color):
        # 更新颜色预览
        self.color_preview.setStyleSheet(
            f"background-color: rgb({color.red()}, {color.green()}, {color.blue()}); "
            "border: 1px solid black;"
        )
        
        # 保存当前颜色
        self.current_color = color
        
        # 更新颜色信息文本
        self.current_rgb = f"rgb({color.red()}, {color.green()}, {color.blue()})"
        self.current_hex = f"#{color.red():02x}{color.green():02x}{color.blue():02x}".upper()
        
        self.rgb_label.setText(f'RGB: {self.current_rgb}')
        self.hex_label.setText(f'HEX: {self.current_hex}')
        
        # 启用所有按钮
        self.copy_rgb_btn.setEnabled(True)
        self.copy_hex_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        
    def generateColorImage(self):
        if not self.current_color:
            return
            
        dialog = GenerateColorImageDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            width, height = dialog.getValues()
            
            # 创建纯色图片
            img = Image.new('RGB', (width, height), 
                          (self.current_color.red(),
                           self.current_color.green(),
                           self.current_color.blue()))
            
            # 保存图片
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "保存纯色图片",
                os.path.expanduser("~/Desktop/color.png"),
                "PNG图片 (*.png);;JPEG图片 (*.jpg *.jpeg);;所有文件 (*.*)"
            )
            
            if file_name:
                img.save(file_name)
                QMessageBox.information(self, "成功", "纯色图片已保存！")
                
def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格，在macOS上看起来更原生
    window = ColorPicker()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
