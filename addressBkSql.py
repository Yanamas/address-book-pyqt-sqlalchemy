import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

from addressBkSqlConn import *
from addressBkQueries import *


class MainWindow(qtw.QWidget):
    def __init__(self) -> None:
        super().__init__()
        # Add a title
        self.setWindowTitle("Address Book")

        # Set form Layout
        form_layout = qtw.QFormLayout()
        self.setLayout(form_layout)      

        label_1 = qtw.QLabel("Address Book")
        self.layout().addWidget(label_1)
        self.label_2 = qtw.QLabel("")


        # Create entry boxes
        self.fname_entry = qtw.QLineEdit(self)
        lname_entry = qtw.QLineEdit(self)
        email_entry = qtw.QLineEdit(self)
        phone_entry = qtw.QLineEdit(self)

        entries_list = [self.fname_entry, lname_entry, email_entry, phone_entry]

        # Create btn with function calls outside
        button = qtw.QPushButton("Second button")
        button.setCheckable(True)
        button.clicked.connect(self.check_for_db)
        button.clicked.connect(self.the_button_was_toggled)

        # Put everything on screen
        # Add rows to app
        form_layout.addRow("First name", self.fname_entry)
        form_layout.addRow("Last name", lname_entry)
        form_layout.addRow("Email", email_entry)
        form_layout.addRow("Phone number", phone_entry)
        form_layout.addRow(qtw.QPushButton("Lambda btn",
                                    clicked = lambda: press_it()))
        form_layout.addRow(button)
        form_layout.addRow(self.label_2)

        # show the app
        self.show()

        def press_it():
            p = Contact(self.fname_entry.text(), lname_entry.text(), email_entry.text(), phone_entry.text())
            existing_person = session.query(Contact).filter_by(first_name=p.first_name, last_name=p.last_name).first()
            if existing_person:
                self.label_2.setText(f"'{p.first_name} {p.last_name}' already exists in Address Book.")
            else:
                session.add(p)
                session.commit()
                self.label_2.setText(f"{p.first_name} {p.last_name} saved to Db!")
                # Clear the entry box
                for e in entries_list:
                    e.setText("")

    def check_for_db(self):
        self.label_2.setText(f"{self.fname_entry.text()} - it worked!")
        self.fname_entry.setText("")
        print("Clicked!")

    def the_button_was_toggled(self, checked):
        print("Checked?", checked)

        


app = qtw.QApplication([])

window = MainWindow()

# run the app
app.exec_()