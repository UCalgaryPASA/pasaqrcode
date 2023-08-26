#!/usr/bin/python

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

import pyqrcode
from PIL import Image


class AppWidget(QtWidgets.QWidget):

    TEMP_FILE = "temp_qr_code.png"
    LOGO_FILE = "pasa_logo.png"
    DISPLAY_SIZE = 512

    DEFAULT_URL = "https://www.pasa.website/index.html"
    DEFAULT_COMPENSATION = 11
    DEFAULT_SCALE = 50
    DEFAULT_PADDING = 43

    def __init__(self) -> None:

        prefix = os.path.dirname(__file__)+os.sep
        self.TEMP_FILE = prefix + self.TEMP_FILE
        self.LOGO_FILE = prefix + self.LOGO_FILE

        super().__init__()
        self.setWindowTitle("PASA QR Code Generator")

        self.img: Image = None

        self.url_control = QtWidgets.QLineEdit()
        self.url_control.setText(self.DEFAULT_URL)

        self.compensation_control = QtWidgets.QSpinBox()
        self.compensation_control.setValue(self.DEFAULT_COMPENSATION)
        compensation_layout = QtWidgets.QHBoxLayout()
        compensation_layout.addWidget(QtWidgets.QLabel("Additional Complexity"))
        compensation_layout.addWidget(self.compensation_control)

        self.scale_control = QtWidgets.QSpinBox()
        self.scale_control.setValue(self.DEFAULT_SCALE)
        scale_layout = QtWidgets.QHBoxLayout()
        scale_layout.addWidget(QtWidgets.QLabel("Scale Factor"))
        scale_layout.addWidget(self.scale_control)

        self.padding_control = QtWidgets.QSpinBox()
        self.padding_control.setValue(self.DEFAULT_PADDING)
        padding_layout = QtWidgets.QHBoxLayout()
        padding_layout.addWidget(QtWidgets.QLabel("Logo Vertical Padding (px)"))
        padding_layout.addWidget(self.padding_control)

        control_layout = QtWidgets.QVBoxLayout()
        control_layout.addWidget(self.url_control)
        control_layout.addLayout(compensation_layout)
        control_layout.addLayout(scale_layout)
        control_layout.addLayout(padding_layout)

        self.image_display = QtWidgets.QLabel()
        self.resolution_display = QtWidgets.QLabel()
        self.resolution_display.setAlignment(QtCore.Qt.AlignCenter)

        display_layout = QtWidgets.QVBoxLayout()
        display_layout.addWidget(self.image_display)
        display_layout.addWidget(self.resolution_display)

        self.generate_button = QtWidgets.QPushButton()
        self.generate_button.setText("Generate QR Code")
        self.generate_button.clicked.connect(self.generate)

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setText("Save Image")
        self.save_button.clicked.connect(self.save)

        main_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(control_layout, 0, 0)
        main_layout.addLayout(display_layout, 0, 1)
        main_layout.addWidget(self.generate_button, 1, 0)
        main_layout.addWidget(self.save_button, 1, 1)
        self.setLayout(main_layout)
    

    def generate(self) -> None:

        self.generate_button.setDisabled(True)

        url = pyqrcode.QRCode(self.url_control.text()+" "*self.compensation_control.value(), error = "H")
        url.png(self.TEMP_FILE, scale=self.scale_control.value())

        im = Image.open(self.TEMP_FILE)
        im = im.convert("RGBA")
        logo = Image.open(self.LOGO_FILE)
        x = im.width//2 - logo.width//2
        y = im.height//2 - logo.height//2
        box = (x,y,x+logo.width,y+logo.height)
        im.crop(box)
        region = logo
        region = region.resize((box[2] - box[0], box[3] - box[1]))

        offset = self.padding_control.value()
        back = Image.new(im.mode, (im.width, logo.height+offset*2), (255,255,255))
        im.paste(back,(0,y-offset))
        
        im.paste(region,box)
        
        self.img = im
        im.save(self.TEMP_FILE)
        qim = QtGui.QPixmap(self.TEMP_FILE).scaled(self.DISPLAY_SIZE, self.DISPLAY_SIZE, QtCore.Qt.KeepAspectRatio)
        self.image_display.setPixmap(qim)
        self.resolution_display.setText(f"{im.width} x {im.height}")
        os.remove(self.TEMP_FILE)
        
        self.generate_button.setEnabled(True)
    

    def save(self) -> None:

        if self.img is not None:

            name = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", ".", "*.png")[0]
            if name != "":

                if not name.endswith(".png"):
                    name += ".png"
                self.img.save(name)


def main():
    app = QtWidgets.QApplication([])
    widget = AppWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
