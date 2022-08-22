import os
import sys

import numpy as np
import pandas as pd
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon

from designs.mainWindow import Ui_MainWindow
import info.transform as tnsf

try:
    from ctypes import windll
    myappid = 'mycompany.myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

basedir = os.path.dirname(__file__)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("EPH")

        self.table = pd.read_csv(
            os.path.join(basedir, "info", "table_month.csv"), index_col=0
        )
        self.input_Button.clicked.connect(self.push_button)

        self.output_Label1.setStyleSheet("color: red")
        self.output_Label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_Label1.setText("")

    @Slot()
    def push_button(self):
        temp_max = self.input_Line1.text()
        temp_mean = self.input_Line2.text()
        temp_min = self.input_Line3.text()

        if not (temp_min and temp_mean and temp_max):
            self.output_Label1.setText("Faltan introducir una o más temperaturas")
            return

        try:
            temp_min = float(temp_min)
            temp_mean = float(temp_mean)
            temp_max = float(temp_max)
        except:
            self.output_Label1.setText("Una o más temperaturas son inválidas")
            return

        row = tnsf.LAT[self.input_Combo3.currentText()]
        column = (
            tnsf.MONTH[self.input_Combo2.currentText()]
            + "."
            + tnsf.HEM[self.input_Combo1.currentText()]
        )

        r0 = self.table[column][row]
        kt = tnsf.KT[self.input_Combo4.currentText()]

        rs = round(r0 * kt * ((temp_max - temp_min) ** 0.5), 3)
        et0 = round(0.0135 * (temp_mean + 17.78) * rs, 3)

        if type(rs) == np.complex128:
            self.output_Label1.setText(
                "Las temperaturas son incorrectas (Posiblemente Tmax mayor a Tmin)"
            )
            return
        self.output_Label1.setText("")
        self.output_Line1.setText(str(rs))
        self.output_Line2.setText(str(et0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir,"resources", 'icon.ico')))
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
