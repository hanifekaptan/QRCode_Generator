import streamlit as st
import barcode
import segno
import io

class QRCodeGenerator:
    """
    QRCodeGenerator class generates different types of QR codes and barcodes.
    """

    def __init__(self):
        """
        Constructor of the class. Sets the title of the Streamlit application and creates interactive buttons.
        """
        st.title("QR Code Generator")

        # Button labels and functions
        button_labels = ["Text", "Link", "VCard", "Wifi", "Email", "Geo", "Micro", "Barcode"]
        button_job = [self.text_exp, self.link_exp, self.vcard_exp, self.wifi_exp,
                      self.email_exp, self.geo_exp, self.micro_exp, self.barcode_exp]

        # Check state variables
        if 'active_expander' not in st.session_state:
            st.session_state.active_expander = None  # No expander is open initially

        # Create buttons
        cols = st.columns(4)
        for i, label in enumerate(button_labels):
            with cols[i % 4]:
                if st.button(label):
                    st.session_state.active_expander = label  # Keep the clicked button's expander open
                    # Close other expanders
                    for lbl in button_labels:
                        if lbl != label:
                            st.session_state[f'show_{lbl.lower()}'] = False

        # Show expanders
        for label in button_labels:
            if st.session_state.active_expander == label:
                button_job[button_labels.index(label)]()

    def generate(self, qr_type: str, input_data: dict):
        """
        Generates a QR code or barcode of the given type.

        Args:
            qr_type (str): The type of code to generate (Text, Link, vCard, Wifi, Email, Geo, Micro, Barcode).
            input_data (dict): The content of the code.

        Returns:
            QRCode or barcode object.
        """
        try:
            if qr_type == "Text":
                data = self.text_link_qr(input_data)
            elif qr_type == "Link":
                data = self.text_link_qr(input_data)
            elif qr_type == "VCard":
                data = self.vcard_qr(input_data)
            elif qr_type == "Wifi":
                data = self.wifi_qr(input_data)
            elif qr_type == "Email":
                data = self.email_qr(input_data)
            elif qr_type == "Geo":
                data = self.geo_qr(input_data)
            elif qr_type == "Micro":
                data = self.micro_qr(input_data)
            elif qr_type == "Barcode":
                data = self.barcode_(input_data)
            return data
        except Exception as e:
            st.write("An error occurred while generating the QR code:", e)
        
    def display(self, qr_code):
        """
        Displays the generated QR code or barcode.

        Args:
            qr_code: QR code or barcode object.
        """
        buffer = io.BytesIO()
        if type(qr_code) == segno.QRCode:
            qr_code.save(buffer, kind="png", scale=50)  # Save QR code in PNG format
        else:
            qr_code.write(buffer)  # Save barcode
        buffer.seek(0)
        st.image(buffer, caption="Generated Code", use_column_width=True)  # Show the image
    
    def download(self, data):
        """
        Makes the generated QR code or barcode available for download.

        Args:
            data: QR code or barcode object to download.
        """
        try:
            buffer = io.BytesIO()
            if type(data) == segno.QRCode:
                data.save(buffer, kind="png", scale=40)  # Save QR code as PNG
            else:
                data.write(buffer)  # Save barcode
            buffer.seek(0)
            st.download_button("Download", buffer, file_name="code.png", mime="image/png")  # Download button
        except Exception as e:
            st.write("An error occurred while downloading the QR code:", e)

    def text_exp(self):
        """
        Interface for creating text QR code.
        """
        with st.expander("Text", expanded=True):
            content = st.text_area("Enter your text here", placeholder="Enter text here", key='text_area')
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_text = True
                input_data = {"Content": content}
                qr_code = self.generate("Text", input_data)
                self.display(qr_code)
            if col2.button("Download"):
                input_data = {"Content": content}
                data = self.generate("Text", input_data)
                self.download(data)

    def link_exp(self):
        """
        Interface for creating link QR code.
        """
        with st.expander("Link", expanded=True):
            content = st.text_input("Enter your link here", placeholder="Enter link here")
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_link = True  # Update state
                input_data = {"Content": content}
                qr_code = self.generate("Text", input_data)
                self.display(qr_code)
            if col2.button("Download"):
                input_data = {"Content": content}
                data = self.generate("Link", input_data)
                self.download(data)

    def vcard_exp(self):
        """
        Interface for creating VCard QR code.
        """
        with st.expander("VCard", expanded=True):
            name = st.text_input("Name*", placeholder="Enter name here")
            displayname = st.text_input("Display Name*", placeholder="Enter display name here")
            email = st.text_input("Email (optional)", placeholder="Enter email here")
            phone = st.text_input("Phone (optional)", placeholder="Enter phone number here")
            memo = st.text_input("Note (optional)", placeholder="Enter notes here")
            birthday = st.date_input("Birthday (optional)")
            url = st.text_input("URL (optional)", placeholder="Enter URL here")
            pobox = st.text_input("Post Box (optional)", placeholder="Enter Post Box here")
            street = st.text_input("Street (optional)", placeholder="Enter street here")
            city = st.text_input("City (optional)", placeholder="Enter city here")
            region = st.text_input("Region (optional)", placeholder="Enter region here")
            zipcode = st.text_input("Zip Code (optional)", placeholder="Enter zip code here")
            country = st.text_input("Country (optional)", placeholder="Enter country here")
            org = st.text_input("Organization (optional)", placeholder="Enter organization here")
            title = st.text_input("Title (optional)", placeholder="Enter title here")
            photo_uri = st.text_input("Photo URI (optional)", placeholder="Enter photo URI here")
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_vcard = True  # Update state
                input_data = {
                    "Name": name, "Displayname": displayname, "Email": email,
                    "Phone": phone, "Memo": memo, "Birthday": birthday,
                    "URL": url, "Pobox": pobox, "Street": street, "City": city,
                    "Region": region, "Zipcode": zipcode, "Country": country, 
                    "Org": org, "Title": title, "Photo_Uri": photo_uri
                }
                qr_code = self.generate("VCard", input_data)
                self.display(qr_code)
            if col2.button("Download"):
                input_data = {
                    "Name": name, "Displayname": displayname, "Email": email,
                    "Phone": phone, "Memo": memo, "Birthday": birthday,
                    "URL": url, "Pobox": pobox, "Street": street, "City": city,
                    "Region": region, "Zipcode": zipcode, "Country": country, 
                    "Org": org, "Title": title, "Photo_Uri": photo_uri
                }
                data = self.generate("VCard", input_data)
                self.download(data)

    def wifi_exp(self):
        """
        Interface for creating Wifi QR code.
        """
        with st.expander("Wifi", expanded=True):
            ssid = st.text_input("SSID", placeholder="Enter SSID here")
            password = st.text_input("Password", placeholder="Enter password here")
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_wifi = True  # Update state
                input_data = {"SSID": ssid, "Password": password}
                qr_code = self.generate("Wifi", input_data)
                self.display(qr_code)
            if col2.button("Download"):
                input_data = {"SSID": ssid, "Password": password}
                data = self.generate("Wifi", input_data)
                self.download(data)

    def email_exp(self):
        """
        Interface for creating Email QR code.
        """
        with st.expander("Email", expanded=True):
            subject = st.text_input("Subject", placeholder="Enter subject here")
            body = st.text_area("Body", placeholder="Enter body here")
            to = st.text_input("To", placeholder="Enter to here")
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_email = True  # Update state
                input_data = {"Subject": subject, "Body": body, "To": to}
                qr_code = self.generate("Email", input_data)
                self.display(qr_code)
            if col2.button("Download"):
                input_data = {"Subject": subject, "Body": body, "To": to}
                data = self.generate("Email", input_data)
                self.download(data)

    def geo_exp(self):
        """
        Interface for creating Geo QR code.
        """
        with st.expander("Geo", expanded=True):
            lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, format="%.4f", placeholder="Enter latitude here")
            lng = st.number_input("Longitude", min_value=-180.0, max_value=180.0, format="%.4f", placeholder="Enter longitude here")
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_geo = True  # Update state
                input_data = {"Latitude": lat, "Longitude": lng}
                qr_code = self.generate("Geo", input_data)
                self.display(qr_code)
            if col2.button("Download"):
                input_data = {"Latitude": lat, "Longitude": lng}
                data = self.generate("Geo", input_data)
                self.download(data)       

    def micro_exp(self):
        """
        Interface for creating Micro QR code.
        """
        with st.expander("Micro", expanded=True):
            text = st.text_area("Enter your text here", placeholder="Enter text here")
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_micro = True  # Update state
                input_data = {"Text": text}
                qr_code = self.generate("Micro", input_data)
                self.display(qr_code)
            if col2.button("Download"):
                input_data = {"Text": text}
                data = self.generate("Micro", input_data)
                self.download(data)

    def barcode_exp(self):
        """
        Interface for creating Barcode.
        """
        with st.expander("Barcode", expanded=True):
            type = st.selectbox("Select a type", ["code128", "ean13", "ean8", "upc", "isbn10", "isbn13", "pzn", "itf", "codabar", "qr"])
            number = st.text_input("Enter a number", placeholder="Enter a number here")
            col1, col2 = st.columns(2)
            if col1.button("Show"):
                st.session_state.show_barcode = True  # Update state
                input_data = {"Type": type, "Number": number}
                brcd = self.generate("Barcode", input_data)
                self.display(brcd)
            if col2.button("Download"):
                input_data = {"Type": type, "Number": number}
                data = self.generate("Barcode", input_data)
                self.download(data)
    
    def text_link_qr(self, content: dict):
        """
        Creates a QR code for text or link.

        Args:
            content (dict): QR code content.

        Returns:
            segno.QRCode: The created QR code object.
        """
        qr = segno.make_qr(content["Content"])
        return qr

    def vcard_qr(self, vcard: dict):
        """
        Creates a QR code for VCard information.

        Args:
            vcard (dict): VCard information.

        Returns:
            segno.QRCode: The created QR code object.
        """
        qr = segno.helpers.make_vcard(
            name=vcard["Name"],
            displayname=vcard["Displayname"],
            email=vcard["Email"],
            phone=vcard["Phone"],
            memo=vcard["Memo"],
            birthday=vcard["Birthday"],
            url=vcard["URL"],
            pobox=vcard["Pobox"],
            street=vcard["Street"],
            city=vcard["City"],
            region=vcard["Region"],
            zipcode=vcard["Zipcode"],
            country=vcard["Country"],
            org=vcard["Org"],
            title=vcard["Title"],
            photo_uri=vcard["Photo_Uri"]
        )
        return qr

    def wifi_qr(self, wifi: dict):
        """
        Creates a QR code for Wifi network.

        Args:
            wifi (dict): Wifi information.

        Returns:
            segno.QRCode: The created QR code object.
        """
        qr = segno.helpers.make_wifi(ssid=wifi["SSID"], password=wifi["Password"])
        return qr
        
    def email_qr(self, email: dict):
        """
        Creates a QR code for Email information.

        Args:
            email (dict): Email information.

        Returns:
            segno.QRCode: The created QR code object.
        """
        qr = segno.helpers.make_email(email["Subject"], email["Body"], email["To"])
        return qr
        
    def geo_qr(self, geo: dict):
        """
        Creates a QR code for geographical location.

        Args:
            geo (dict): Geographical location information.

        Returns:
            segno.QRCode: The created QR code object.
        """
        qr = segno.helpers.make_geo(geo["Latitude"], geo["Longitude"])
        return qr

    def micro_qr(self, content: dict):
        """
        Creates a Micro QR code.

        Args:
            content (dict): Micro QR code content.

        Returns:
            segno.QRCode: The created micro QR code object.
        """
        qr = segno.make_micro(content["Text"])
        return qr

    def barcode_(self, brcode: dict):
        """
        Creates a barcode.

        Args:
            brcode (dict): Barcode information.

        Returns:
            barcode.barcode.Barcode: The created barcode object.
        """
        brcd = barcode.get_barcode(name=brcode["Type"], code=brcode["Number"], writer=barcode.writer.ImageWriter())
        return brcd

# Start QRCodeGenerator class
QRCodeGenerator()