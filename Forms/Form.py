from PySide6 import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from db_Sqlalchemy import *
import hashlib

def hash_password(pas):
    return hashlib.sha256(pas.encode()).hexdigest()

class Style():
    def __init__(self):
        self.Buttons_Width = 70
        self.Buttons_Height = 30

        self.Input_Width = 140
        self.Input_Height = 30

        self.Input_Error_style = """ border: 1px solid red; """

        self.Label_Width = 140
        self.Label_Height = 30

        self.Big_button_Width = 250
        self.Big_button_Height = 40

        self.H1 = 'font: 75 15pt "MS Shell Dlg 2";'

style = Style()

class User_Info_Form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.prev_window = null
        self.active_user = null

        self.setWindowTitle("Информация о пользователе")
        self.setGeometry(20, 20, 600, 500)

        self.image = QLabel("", parent=self)#Imege
        self.image.setGeometry(20, 20, 250, 240)
        self.image.setPixmap(QPixmap())
        self.image.setScaledContents(True)

        self.name_label = QLabel("Имя ", parent=self)
        self.name_label.setGeometry(280, 20, style.Label_Width, style.Label_Height)

        self.fam_label = QLabel("Фамилия ", parent=self)
        self.fam_label.setGeometry(280, 60, style.Label_Width, style.Label_Height)

        self.phone_label = QLabel("Тел. ", parent=self)
        self.phone_label.setGeometry(280, 100, style.Label_Width, style.Label_Height)

        self.login_label = QLabel("login ", parent=self)
        self.login_label.setGeometry(280, 140, style.Label_Width, style.Label_Height)

        self.password_svap = QPushButton("Изменить пароль", parent=self)
        self.password_svap.setGeometry(280, 220, style.Big_button_Width, style.Big_button_Height)
        self.password_svap.clicked.connect(self.pas_svap)

        self.button_select_image = QPushButton("Выбрать изображение", parent=self)
        self.button_select_image.setGeometry(20, 280, style.Big_button_Width, style.Big_button_Height)
        self.button_select_image.clicked.connect(self.select_new_image)

    def pas_svap(self):
        dialog = QDialog()
        dialog.setWindowTitle("Сменить пароль")
        dialog.setGeometry(100,100,300,200)

        dialog.inp1 = QLineEdit(parent=dialog)
        dialog.inp2 = QLineEdit(parent=dialog)
        
        dialog.lab1 = QLabel("Введите новый пароль", parent=dialog)
        dialog.lab2 = QLabel("Подтвердите новый пароль", parent=dialog)

        dialog.lab1.setGeometry(20,10,260,30)
        dialog.lab2.setGeometry(20,70,260,30)

        dialog.inp1.setGeometry(20, 40, 260, 30)
        dialog.inp2.setGeometry(20, 100, 260, 30)

        dialog.ok = QPushButton("Подтвердить",parent=dialog)
        dialog.ok.setGeometry(20, 140, 260, style.Big_button_Height)
        dialog.exec()

    def closeEvent(self, ivent):
        self.prev_window.show()
        ivent.accept()

    def select_new_image(self):
        file_path = QFileDialog.getOpenFileName(self, "Выберите файл", '', "Изображения (*.png *.jpeg *.jpg);;Все файлы (*.*)")
        print(file_path[0])
        self.image.setPixmap(QPixmap(file_path[0]))

class Book_Info_form(QMainWindow):
    def __init__(self):
        super().__init__()

        self.id_book = null

        self.setWindowTitle('')
        self.setGeometry(80, 80, 700, 700)

        self.image = QLabel("", parent=self)#Imege
        self.image.setGeometry(20, 20, 250, 370)
        self.image.setPixmap(QPixmap())
        self.image.setScaledContents(True)

        self.H1 = QLabel("", parent=self)#Title_book
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
        self.button_select_image.setGeometry(20, 410, style.Big_button_Width, style.Big_button_Height)
        self.button_select_image.clicked.connect(self.select_new_image)

        self.table_author = QTableWidget(1, 2, parent=self)#Table authors/таблица авторов
        self.table_author.setHorizontalHeaderLabels(['Имя', "Фамилия"])
        self.table_author.setGeometry(300, 320, 220, 130)
        self.table_author.setEditTriggers(QAbstractItemView.NoEditTriggers)#Read only
        self.table_author.setSelectionMode(QAbstractItemView.NoSelection)#No select element

        self.table_types = QTableWidget(1, 1, parent=self)
        self.table_types.setHorizontalHeaderLabels(['Жанры'])#Table types/таблица жанров
        self.table_types.setGeometry(530, 320, 140, 130)
        self.table_types.setColumnWidth(0, 140)
        self.table_types.setEditTriggers(QAbstractItemView.NoEditTriggers)#Read only
        self.table_types.setSelectionMode(QAbstractItemView.NoSelection)#No select element

        self.save_button = QPushButton("Сохранить", parent=self)
        self.save_button.setGeometry(20, 460, style.Big_button_Width, style.Big_button_Height)
        self.save_button.clicked.connect(self.save_info)

        self.drop_button = QPushButton("Сбросить", parent=self)
        self.drop_button.setGeometry(300, 460, style.Big_button_Width, style.Big_button_Height)
        self.drop_button.clicked.connect(self.drop_form_info)

        # self.save_button = QPushButton("Сохранить", parent=self)
        # self.save_button.setGeometry(300, 490, style.Big_button_Width, style.Big_button_Height)

    def save_info(self):
        # masege_form = QDialogButtonBox()
        result = QMessageBox.critical(#warning
        None,
        "Изменить",
        "Подтвердить изменения",
        QMessageBox.Yes | QMessageBox.No
        # QMessageBox.Warning
    )
        if result == QMessageBox.Yes:
            result = True
        else:
            result = False


        print(result)
        return result == QMessageBox.Yes


    def drop_form_info(self):
        # book = session.query(Book).filter_by(book_title = self.windowTitle()).all()
        book = session.query(Book).filter(Book.id_book == self.id_book).one()
        # book = book[0]
        self.image.setPixmap(QPixmap(book.pictcher))
        self.H1.setText(f"Информация о книге: {book.book_title}")
        self.Input_info_titile_book.setText(book.book_title)
        self.Input_info_date.setDate(book.publication_date)
        self.Input_info_in_stock.setValue(book.in_stock)

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
        self.table.setColumnWidth(0, 290)
        self.table.setColumnWidth(1, 90)
        self.table.setColumnWidth(2, 30)
        self.table.setColumnWidth(3, 170)

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
        self.work_window.id_book = book.id_book
        self.work_window.image.setPixmap(QPixmap(book.pictcher))
        self.work_window.H1.setText(f"Информация о книге: {book.book_title}")
        self.work_window.Input_info_titile_book.setText(book.book_title)
        self.work_window.Input_info_date.setDate(book.publication_date)
        self.work_window.Input_info_in_stock.setValue(book.in_stock)
        self.work_window.table_author.setRowCount(len(book.authors_book))
        authors = book.authors_book
        for row in range(len(authors)):
            for col in range(self.work_window.table_author.columnCount()):
                match col:
                    # case 0:
                        # self.work_window.table.setItem(row, col, QTableWidgetItem(str(authors[row].author.id_author)))
                    case 0:
                        self.work_window.table_author.setItem(row, col, QTableWidgetItem(str(authors[row].author.name)))
                    case 1:
                        self.work_window.table_author.setItem(row, col, QTableWidgetItem(str(authors[row].author.sure_name)))

        types_book = book.book_types
        self.work_window.table_types.setRowCount(len(types_book))
        # print(f"Количество строк в таблице: {self.work_window.table_types.rowCount()}")
        for i in range(len(types_book)):
            # print(types_book[i].type_book.book_type)
            self.work_window.table_types.setItem(i, 0, QTableWidgetItem(str(types_book[i].type_book.book_type)))
        self.work_window.show()
        self.work_window.setWindowTitle(f"{book.book_title}")

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

        self.user_info = QPushButton("Профиль", parent=self)
        self.user_info.setGeometry(180, 50, style.Buttons_Width, style.Buttons_Height)
        self.user_info.clicked.connect(self.user_info_form_show)

        self.prev_window = None
        # self.book_katalog = QPushButton("", parent=self)

    def user_info_form_show(self):
        self.work_window = User_Info_Form()
        self.work_window.prev_window = self
        self.work_window.show()
        self.work_window.active_user = self.active_user
        self.work_window.name_label.setText(f"Имя: {self.work_window.active_user.name}")
        self.work_window.fam_label.setText(f"Фамилия: {self.work_window.active_user.sure_name}")
        self.work_window.phone_label.setText(f"Тел: {self.work_window.active_user.phone}")
        self.work_window.login_label.setText(f"Логин: {self.work_window.active_user.login}")
        self.work_window.image.setPixmap(QPixmap(self.work_window.active_user.image))
        self.hide()

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
        self.user_create.clicked.connect(self.create_user)

    def create_user(self):
        pass


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
        active_user = null
        self.pass_input.setStyleSheet("")
        self.login_input.setStyleSheet("")
        for user in usersArr:
            if active_user == null:
                # print(user.name)
                if login == user.login and hash_password(pwr) == user.password:
                    for role in user.user_roles:
                        # print(f"роль {role.roles.id_role}")
                        match role.roles.id_role:
                            case 1:
                                self.work_window = Admin_page()
                                self.work_window.prev_window = self
                                self.work_window.show()
                                self.pass_input.setText('')
                                self.login_input.setText('')
                                self.hide()
                                self.work_window.active_user = user
                                active_user = user
                                break
                            case 2:
                                self.work_window = librarian_window()
                                self.work_window.prev_window = self
                                self.work_window.show()
                                self.pass_input.setText('')
                                self.login_input.setText('')
                                self.hide()
                                self.work_window.active_user = user
                                active_user = user
                                break
                    
            else:
                break     
        if active_user == null:
            print(f"Error")
            self.login_input.setStyleSheet(style.Input_Error_style)
            self.pass_input.setStyleSheet(style.Input_Error_style)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = logining_window()
    window.show()
    sys.exit(app.exec())