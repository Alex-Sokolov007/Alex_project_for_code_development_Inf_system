from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from db_Sqlalchemy import *
import hashlib

def hash_password(pas):
    return hashlib.sha256(pas.encode()).hexdigest()
    pass

class Style():
    def __init__(self):
        self.Buttons_Width = 70
        self.Buttons_Height = 30

        self.Input_Width = 140
        self.Input_Height = 30

        self.Input_Error_style = """ border: 1px solid red; """

        self.Label_Width = 140
        self.Label_Height = 30

        self.H1 = 'font: 75 15pt "MS Shell Dlg 2";'

style = Style()

class Book_Info_form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('')
        self.setGeometry(80, 80, 700, 700)

        self.image = QLabel("", parent=self)
        self.image.setGeometry(20, 20, 250, 370)
        self.image.setPixmap(QPixmap())
        self.image.setScaledContents(True)

        self.H1 = QLabel("", parent=self)
        self.H1.setGeometry(300, 20, 350, 250)
        self.H1.setWordWrap(True)
        self.H1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.H1.setStyleSheet(style.H1)

        self.label_info_title_book = QLabel("Изменить название", parent=self)
        self.label_info_title_book.setGeometry(300, 100, style.Label_Width, style.Label_Height)

        self.Input_info_titile_book = QLineEdit(parent=self)
        self.Input_info_titile_book.setGeometry(300, 130, style.Input_Width + 150, style.Input_Height)
        
        self.label_info_date = QLabel("Изменить дату выпуска", parent=self)
        self.label_info_date.setGeometry(300, 170, style.Label_Width, style.Label_Height)

        self.Input_info_date = QDateEdit(parent=self)
        self.Input_info_date.setGeometry(300, 200, style.Input_Width + 150, style.Input_Height)

        self.label_info_is_stok = QLabel("Изменить количество", parent=self)
        self.label_info_is_stok.setGeometry(300, 240, style.Label_Width, style.Label_Height)

        self.Input_info_in_stock = QSpinBox(parent=self)
        self.Input_info_in_stock.setGeometry(300, 270, style.Input_Width + 50, style.Input_Height)

        self.button_select_image = QPushButton("Выбрать изображение", parent=self)
        self.button_select_image.setGeometry(20, 410, 250, 40)
        self.button_select_image.clicked.connect(self.select_new_image)

        self.table = QTableWidget(1, 2, parent=self)
        self.table.setHorizontalHeaderLabels(['Имя', "Фамилия"])
        self.table.setGeometry(300, 320, 220, 130)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)#Read only
        self.table.setSelectionMode(QAbstractItemView.NoSelection)#No select element

        self.seve_button = QPushButton("Сохранить", parent=self)
        self.seve_button.setGeometry(300, 500, 200, 40)

    def select_new_image(self):
        file_path = QFileDialog.getOpenFileName(self, "Выберите файл", '', "Изображения (*.png *.jpeg *.jpg);;Все файлы (*.*)")
        print(file_path[0])
        self.image.setPixmap(QPixmap(file_path[0]))

class Catalog_books_form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Каталог книг')
        self.setGeometry(80, 80, 800, 800)

        self.table = QTableWidget(1, 4, parent=self)
        self.table.setHorizontalHeaderLabels(['Название книги', 'Дата выпуска', "В наличии шт.", "Подробная информация"])
        self.table.setGeometry(100, 100, 600, 600)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)#Read only
        self.table.setSelectionMode(QAbstractItemView.NoSelection)#No select element
        # self.catalog_books.setGeometry(20, 50, style.Buttons_Width, style.Buttons_Height)

        self.prev_window = None

    def showEvent(self, event):
        super().showEvent(event)
        books = session.query(Book).all()
        self.table.setRowCount(session.query(Book).count())
        row = self.table.rowCount()
        column = self.table.columnCount()
        for r in range(row):
            for c in range(column):
                match c:
                    # case 0:
                        # self.table.setItem(r, c, QTableWidgetItem(str(books[r].id_book)))
                    case 0:
                        self.table.setItem(r, c, QTableWidgetItem(books[r].book_title))
                    case 1:
                        self.table.setItem(r, c, QTableWidgetItem(str(books[r].publication_date)))
                    case 2:
                        self.table.setItem(r, c, QTableWidgetItem(str(books[r].in_stock)))
                    case 3:
                        self.Info = QPushButton('Подробнее', parent=self)
                        self.Info.clicked.connect(lambda checked, book = books[r]: self.book_info(book))
                        # self.Info.row, self.Info.col = r, c
                        self.table.setCellWidget(r, c, self.Info)
    
    def book_info(self, book):
        self.work_window = Book_Info_form()
        self.work_window.image.setPixmap(QPixmap(book.pictcher))
        self.work_window.H1.setText(f"Информация о книге: {book.book_title}")
        self.work_window.Input_info_titile_book.setText(book.book_title)
        self.work_window.Input_info_date.setDate(book.publication_date)
        self.work_window.Input_info_in_stock.setValue(book.in_stock)
        self.work_window.table.setRowCount(len(book.authors_book))
        authors = book.authors_book
        for row in range(len(authors)):
            for col in range(self.work_window.table.columnCount()):
                match col:
                    # case 0:
                        # self.work_window.table.setItem(row, col, QTableWidgetItem(str(authors[row].author.id_author)))
                    case 0:
                        self.work_window.table.setItem(row, col, QTableWidgetItem(str(authors[row].author.name)))
                    case 1:
                        self.work_window.table.setItem(row, col, QTableWidgetItem(str(authors[row].author.sure_name)))


        self.work_window.show()
        self.work_window.setWindowTitle(f"Информация о книге {book.book_title}")

    def closeEvent(self, ivent):
        self.prev_window.show()
        ivent.accept()

class librarian_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добро пожаловать в Афину')
        self.setGeometry(80, 80, 800, 800)

        self.label1 = QLabel("Каталог книг", parent=self)
        self.label1.setGeometry(20, 20, style.Label_Width, style.Label_Height)

        self.catalog_books = QPushButton('Каталог', parent=self)
        self.catalog_books.setGeometry(20, 50, style.Buttons_Width, style.Buttons_Height)
        self.catalog_books.clicked.connect(self.catalog_books_form_show)

        self.exitButton = QPushButton("Выйти", parent=self)
        self.exitButton.setGeometry(100, 50, style.Buttons_Width, style.Buttons_Height)
        self.exitButton.clicked.connect(self.closeEvent_button)

        self.prev_window = None
        # self.book_katalog = QPushButton("", parent=self)

    def catalog_books_form_show(self):
        self.work_window = Catalog_books_form()
        self.work_window.prev_window = self
        self.work_window.show()
        self.hide()

    def closeEvent(self, ivent):
        self.prev_window.show()
        ivent.accept()

    def closeEvent_button(self):
        self.hide()
        self.prev_window.show()
    

class Admin_page(librarian_window):  # Админ
    def __init__(self):
        super().__init__()

        self.label2 = QLabel("Создать пользователя", parent=self)
        self.label2.setGeometry(20, 80, style.Label_Width, style.Label_Height)

        self.user_create = QPushButton('Создать', parent=self)
        self.user_create.setGeometry(20, 110, style.Buttons_Width, style.Buttons_Height)
       

class logining_window(QDialog):# вход в систему
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Афина')
        self.setGeometry(80, 80, 300, 300)

        self.log_button = QPushButton('Войти', parent=self)
        self.log_button.setGeometry(110, 260, style.Buttons_Width, style.Buttons_Height)
        self.log_button.clicked.connect(self.logining)

        self.log_lab = QLabel("Ввдите логин", parent=self)
        self.log_lab.setGeometry(80, 115, style.Label_Width, style.Label_Height)

        self.login_input = QLineEdit(parent=self)
        self.login_input.setGeometry(80, 150, style.Input_Width, style.Input_Height)

        self.pass_lab = QLabel("Ввдите пароль", parent=self)
        self.pass_lab.setGeometry(80, 185, 140, 30)

        self.pass_input = QLineEdit(parent=self)
        self.pass_input.setGeometry(80, 220, style.Input_Width, style.Input_Height)
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.pass_look = QCheckBox(f"Показать \nпароль", parent=self)
        self.pass_look.move(220, 223)
        self.pass_look.clicked.connect(self.look_password)

    def look_password(self):
        if self.pass_look.isChecked():
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

    def logining(self):
        login, pwr = self.login_input.text(), self.pass_input.text()
        usersArr = session.query(Users).all()
        active_user = 0
        self.pass_input.setStyleSheet("")
        self.login_input.setStyleSheet("")
        for user in usersArr:
            if active_user == 0:
                print(user.name)
                if login == user.login and hash_password(pwr) == user.password:
                    for role in user.user_roles:
                        print(f"роль {role.roles.id_role}")
                        match role.roles.id_role:
                            case 1:
                                self.work_window = Admin_page()
                                self.work_window.prev_window = self
                                self.work_window.show()
                                self.pass_input.setText('')
                                self.login_input.setText('')
                                self.hide()
                                active_user = user.id_users
                                break
                            case 2:
                                self.work_window = librarian_window()
                                self.work_window.prev_window = self
                                self.work_window.show()
                                self.pass_input.setText('')
                                self.login_input.setText('')
                                self.hide()
                                active_user = user.id_users
                                break
                    
            else:
                break     
        if active_user == 0:
            print(f"Error")
            self.login_input.setStyleSheet(style.Input_Error_style)
            self.pass_input.setStyleSheet(style.Input_Error_style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = logining_window()
    window.show()
    sys.exit(app.exec())