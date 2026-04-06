from db_Sqlalchemy import *
import sys
from  Forms.Form import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = logining_window()
    window.show()
    sys.exit(app.exec())
