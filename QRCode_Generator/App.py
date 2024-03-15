import datetime
import segno
from segno import helpers
from barcode import isxn, ean, get_barcode
from barcode.writer import ImageWriter
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QDialog
from QrCodeWindow import Ui_MainWindow
from OutputWindow import Ui_Dialog


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.output = Output()

        self.prev_button = self.ui.text_button
        self.ui.create_button.clicked.connect(self.create_qr)
        self.ui.text_button.clicked.connect(self.text)
        self.ui.link_button.clicked.connect(self.link)
        self.ui.vcard_button.clicked.connect(self.vcard)
        self.ui.wifi_button.clicked.connect(self.wifi)
        self.ui.email_button.clicked.connect(self.email)
        self.ui.geo_button.clicked.connect(self.geo)
        self.ui.micro_button.clicked.connect(self.micro)
        self.ui.barcode_button.clicked.connect(self.barcode)

    def create_qr(self):
        """
        Method that generates QR Code.
        """
        button = self.prev_button
        if button == self.ui.text_button:
            self.text_qr()
        elif button == self.ui.link_button:
            self.link_qr()
        elif button == self.ui.vcard_button:
            self.vcard_qr()
        elif button == self.ui.wifi_button:
            self.wifi_qr()
        elif button == self.ui.email_button:
            self.email_qr()
        elif button == self.ui.geo_button:
            self.geo_qr()
        elif button == self.ui.micro_button:
            self.micro_qr()
        elif button == self.ui.barcode_button:
            self.barcode_2d()

    def text(self):
        """
        Method that opens the text_page when the text_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.text_page)
    
    def text_data(self) -> str:
        """
        Method that returns the content of text in text_page.
        """
        text = self.ui.text_content.toPlainText()
        return text

    def text_qr(self):
        """
        Method that generates a QR Code or throws error box.
        """
        try:
            text = self.text_data()
            qr = segno.make_qr(text)
            qr.save("output.png", scale=15)
            self.show_output()
        except(segno.DataOverflowError, ValueError):
            self.error_msg()

    def link(self):
        """
        Method that opens the link_page when the link_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.link_page)

    def link_data(self) -> str:
        """
        Method that returns the content of link in link_page.
        """
        link = self.ui.link_content.toPlainText()
        return link

    def link_qr(self):
        """
        Method that generates a QR Code or throws error box.
        """
        try:
            link = self.link_data()
            qr = segno.make_qr(link)
            qr.save("output.png", scale=15)
            self.show_output()
        except(segno.DataOverflowError, ValueError):
            self.error_msg()

    def vcard(self):
        """
        Method that opens the vcard_page when the vcard_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.vcard_page)

    def vcard_data(self) -> dict:
        """
        Method that returns the content of vcard in vcard_page.
        vcard_page contains: name, displayname, email, phone, url, city,
        zipcode, country, org, title, cellphone, homephone and workphone variables.
        """
        vcard = {
            "name": self.ui.name_content.text(),
            "displayname": self.ui.display_name_content.text(),
            "email": self.ui.email_content.text(),
            "phone": self.ui.phone_content.text(),
            "url": self.ui.url_content.text(),
            "city": self.ui.city_content.text(),
            "zipcode": self.ui.zipcode_content.text(),
            "country": self.ui.country_content.text(),
            "org": self.ui.org_content.text(),
            "title": self.ui.title_content.text(),
            "cellphone": self.ui.cellphone_content.text(),
            "homephone": self.ui.homephone_content.text(),
            "workphone": self.ui.workphone_content.text()
                }
        for i in vcard.keys():
            if vcard.get(i).replace(" ","") == "":
                vcard.update({i: None})
        return vcard
    
    def get_birthday(self) -> datetime.date | None:
        """
        Method that returns birthday value required for vcard.
        """
        birthday = self.ui.birthday_content.text()
        if birthday.replace(" ","") == "":
            birthday = None
        else:
            for i in [".", ":", "-","/"]:
                if i in birthday:
                    birthday = birthday.split(i)
                    break
            birthday = datetime.date(year= int(birthday[2]), month= int(birthday[1]), day= int(birthday[0]))
        return birthday

    def vcard_qr(self):
        """
        Method that generates a QR Code which encodes a vCard (version 3.0.) or throws error box.
        """
        try:
            vcard = self.vcard_data()
            qr = helpers.make_vcard(name= vcard["name"],
                                displayname= vcard["displayname"],
                                email= vcard["email"],
                                phone= vcard["phone"],
                                birthday= self.get_birthday(),
                                url= vcard["url"],
                                city= vcard["city"],
                                zipcode= vcard["zipcode"],
                                country= vcard["country"],
                                org= vcard["org"],
                                title= vcard["title"],
                                cellphone= vcard["cellphone"],
                                homephone= vcard["homephone"],
                                workphone= vcard["workphone"]
                                )
            qr.save("output.png", scale=15)
            self.show_output()
        except(segno.DataOverflowError, ValueError):
            self.error_msg()

    def wifi(self):
        """
        Method that opens the wifi_page when the wifi_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.wifi_page)

    def wifi_data(self) -> dict:
        """
        Method that returns the content of wifi in wifi_page.
        wifi_page contains: ssid, password an security variables.
        """
        wifi = {
            "ssid": self.ui.ssid_content.text(),
            "password": self.ui.password_content.text(),
            "security": self.ui.security_content.currentText()
                }
        if wifi.get("security") == "None":
                wifi.update({"security": None})
        return wifi

    def wifi_qr(self):
        """
        Method that generates a QR Code from wifi configuration or throws error box.
        """
        try:
            wifi = self.wifi_data()
            qr = helpers.make_wifi(ssid= wifi["ssid"],
                                password= wifi["password"],
                                security= wifi["security"]
                                )
            qr.save("output.png", scale=15)
            self.show_output()
        except(segno.DataOverflowError, ValueError):
            self.error_msg()

    def email(self):
        """
        Method that opens the email_page when the email_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.email_page)

    def email_data(self) -> dict:
        """
        Method that returns the content of email in email_page.
        email_page contains: to, subject and body variables.
        """
        email = {
            "to": self.ui.to_content.text(),
            "subject": self.ui.subject_content.text(),
            "body":self.ui.body_content.toPlainText()
                }
        for i in email.keys():
            if email.get(i) == "":
                email.update({i:None})
        return email

    def email_qr(self):
        """
        Method that generates a QR Code to send email or throws error box.
        """
        try:
            email = self.email_data()
            qr = helpers.make_email(to= email["to"],
                                subject= email["subject"],
                                body= email["body"])
            qr.save("output.png", scale=15)
            self.show_output()
        except(segno.DataOverflowError, ValueError):
            self.error_msg()

    def geo(self):
        """
        Method that opens the geo_page when the geo_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.geo_page)

    def geo_data(self) -> dict:
        """
        Method that returns the content of geo location in geo_page.
        geo_page contains: latitude and longitude variables.
        Type of these variables are float.
        -90 < latitude value < +90
        -180 < longitude value < +180
        """
        geo = {
            "latitude": float(self.ui.latitude_content.text()),
            "longitude": float(self.ui.longitude_content.text())
                }
        return geo
        
    def geo_qr(self):
        """
        Method that generates a QR Code which encodes geographic location or throws error box.
        """
        try:
            geo = self.geo_data()
            qr = helpers.make_geo(lat= geo["latitude"],
                                lng= geo["longitude"])
            qr.save("output.png", scale=15)
            self.show_output()
        except(segno.DataOverflowError, ValueError):
            self.error_msg()

    def micro(self):
        """
        Method that opens the micro_page when the micro_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.micro_page)

    def micro_data(self) -> str:
        """
        Method that returns the content of micro in micro_page.
        """
        micro = self.ui.micro_content.toPlainText()
        return micro

    def micro_qr(self):
        """
        Method that generates a micro QR Code or throws error box.
        """
        try:
            micro = self.micro_data()
            qr = segno.make_micro(micro)
            qr.save("output.png", scale=10)
            self.show_output()
        except(segno.DataOverflowError, ValueError):
            self.error_msg()

    def barcode(self):
        """
        Method that opens the barcode_page when the barcode_button is clicked.
        """
        self.prev_button = self.sender()
        self.ui.input.setCurrentWidget(self.ui.barcode_page)

    def barcode_data(self) -> dict:
        """
        Method that returns the content of barcode in barcode_page.
        barcode_page contains: type of barcode and barcode number.
        """
        barcode = {
            "type" : self.ui.type_content.currentText(),
            "number": self.ui.number_content.text()
                }
        return barcode
    
    def barcode_2d(self):
        """
        Method that generates a 2D Barcode or throws error box.
        """
        try:
            brcd = self.barcode_data()
            bc = get_barcode(name= brcd["type"],
                            code= brcd["number"],
                            writer= ImageWriter())
            bc.save("output")
            self.show_output()
        except(ValueError, isxn.WrongCountryCodeError, isxn.BarcodeError,
               ean.NumberOfDigitsError, ean.WrongCountryCodeError):
            self.error_msg()

    def show_output(self):
        """
        Method that shows Output Window and the generated output and calls the clear_all method.
        """
        self.output.show()
        self.output.show_output()
        self.clear_all()

    def clear_all(self):
        """
        Method that clears input after QR Code is generated.
        """
        text_line_edits = self.ui.input.findChildren((QtWidgets.QLineEdit, QtWidgets.QTextEdit))
        for i in text_line_edits:
            i.clear()
        combo_boxs = self.ui.input.findChildren(QtWidgets.QComboBox)
        for i in combo_boxs:
            i.setCurrentIndex(0)

    def error_msg(self):
        """
        If invalid data has been entered, method that returns an error message box.
        """
        text = """Make sure that the data you entered is in the appropriate
format and the data is not too large or too small. Then try again.
        """
        QMessageBox.warning(self, "Data error", text, QMessageBox.Ok)



class Output(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def show_output(self):
        """
        Method that displays the generated output.
        """
        image_path=("output.png")
        image_profile= QtGui.QImage(image_path)
        image_profile= image_profile.scaled(450, 420, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.ui.output.setPixmap(QtGui.QPixmap.fromImage(image_profile))