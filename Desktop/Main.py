# Author: Hanife Kaptan

# Description: Application that converts data from various configurations to Qr Code form.

# Version: segno (1.6.0), PyQt5 (5.15.10), PyQt5Designer (5.14.1), pyhon-barcode (0.15.1), python (3.11.2)

from PyQt5.QtWidgets import QApplication
from App import App

app = QApplication([])
window = App()
window.show()
app.exec_()
