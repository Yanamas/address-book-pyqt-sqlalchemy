import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

from addressBkSqlConn import *


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
        self.lname_entry = qtw.QLineEdit(self)
        self.email_entry = qtw.QLineEdit(self)
        self.phone_entry = qtw.QLineEdit(self)

        self.entries_list = [self.fname_entry, self.lname_entry, self.email_entry, self.phone_entry]

        # Create a combobox for contact categories
        self.category_combobox = qtw.QComboBox()
        self.populate_category_combobox()  # Populate the combobox with categories from the database

        # Create btn with function calls outside
        button = qtw.QPushButton("Add")
        button.clicked.connect(self.add_pressed)

        # Put everything on screen
        # Add rows to app
        form_layout.addRow("First name", self.fname_entry)
        form_layout.addRow("Last name", self.lname_entry)
        form_layout.addRow("Email", self.email_entry)
        form_layout.addRow("Phone number", self.phone_entry)
        form_layout.addRow("Category", self.category_combobox)
        form_layout.addRow(button)
        form_layout.addRow(self.label_2)

        # show the app
        self.show()


    def add_pressed(self):
        p = Contact(self.fname_entry.text(), self.lname_entry.text(), self.email_entry.text(), self.phone_entry.text())
        person_exists = session.query(Contact).filter_by(first_name=p.first_name, last_name=p.last_name).first()
        if person_exists:
            self.label_2.setText(f"'{p.first_name} {p.last_name}' already exists in Address Book.")
        else:
            session.add(p)
            selected_category_name = self.category_combobox.currentText()
            category = session.query(Category).filter_by(cat_name=selected_category_name).first()
            if category:
                self.add_category(p.id, category.id)
            session.commit()
            self.label_2.setText(f"{p.first_name} {p.last_name} saved to Db!")
            # Clear the entry box
            for e in self.entries_list:
                e.setText("")


    def add_category(self, contact_id, category_id):
        contact_category = ContactCategory(contact_id=contact_id, category_id=category_id)
        session.add(contact_category)


    def populate_category_combobox(self):
        # Query the database to get category names using SQLAlchemy
        categories = session.query(Category).all()
        category_names = [category.cat_name for category in categories]
        self.category_combobox.addItems(category_names)


        


app = qtw.QApplication([])

window = MainWindow()

# run the app
app.exec_()