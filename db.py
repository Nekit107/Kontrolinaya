import psycopg2
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QFormLayout, QComboBox
)

# Конфигурация базы данных
DB_CONFIG = {
    "dbname": "pro_41_nn",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

# Подключение к БД
def connect_db():
    
    return psycopg2.connect(**DB_CONFIG)

# Окно для добавления сотрудника
class AddEmployeeWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Добавить сотрудника")
        self.parent = parent
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.first_name_input = QLineEdit()
        self.last_name_input = QLineEdit()
        self.position_input = QLineEdit()
        self.salary_input = QLineEdit()
        self.hire_date_input = QLineEdit()
        self.department_id_input = QLineEdit()

        form_layout.addRow("Имя:", self.first_name_input)
        form_layout.addRow("Фамилия:", self.last_name_input)
        form_layout.addRow("Должность:", self.position_input)
        form_layout.addRow("Зарплата:", self.salary_input)
        form_layout.addRow("Дата приёма:", self.hire_date_input)
        form_layout.addRow("ID отдела:", self.department_id_input)

        layout.addLayout(form_layout)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_employee)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_employee(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO employees (first_name, last_name, position, salary, hire_date, department_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (self.first_name_input.text(), self.last_name_input.text(), self.position_input.text(),
             self.salary_input.text(), self.hire_date_input.text(), self.department_id_input.text())
        )
        conn.commit()
        conn.close()
        self.parent.load_data()
        self.close()

# Окно для работы с сотрудниками
class EmployeeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сотрудники")
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Должность"])
        layout.addWidget(self.table)

        self.load_data()

        self.add_button = QPushButton("Добавить сотрудника")
        self.add_button.clicked.connect(self.open_add_employee_window)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def load_data(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, first_name, last_name, position FROM employees")
        employees = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(employees))
        for row, emp in enumerate(employees):
            for col, data in enumerate(emp):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def open_add_employee_window(self):
        self.add_employee_window = AddEmployeeWindow(self)
        self.add_employee_window.show()

# Окно для добавления новой задачи
class AddTaskWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Добавить задачу")
        self.parent = parent
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.description_input = QLineEdit()
        self.status_combo = QComboBox()
        self.status_combo.addItems(["в процессе", "завершена", "отменена"])
        self.project_id_input = QLineEdit()
        self.assignee_id_input = QLineEdit()

        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Описание:", self.description_input)
        form_layout.addRow("Статус:", self.status_combo)
        form_layout.addRow("ID проекта:", self.project_id_input)
        form_layout.addRow("ID сотрудника:", self.assignee_id_input)

        layout.addLayout(form_layout)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_task(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tasks (name, description, status, project_id, assignee_id) VALUES (%s, %s, %s, %s, %s)",
            (self.name_input.text(), self.description_input.text(), self.status_combo.currentText(),
             self.project_id_input.text(), self.assignee_id_input.text())
        )
        conn.commit()
        conn.close()
        self.parent.load_data()
        self.close()


class TaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задачи")
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Статус"])
        layout.addWidget(self.table)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["в процессе", "завершена", "отменена"])
        layout.addWidget(self.status_combo)

        self.update_button = QPushButton("Обновить статус")
        self.update_button.clicked.connect(self.update_status)
        layout.addWidget(self.update_button)

        self.add_task_button = QPushButton("Добавить задачу")
        self.add_task_button.clicked.connect(self.open_add_task_window)
        layout.addWidget(self.add_task_button)

        self.load_data()
        self.setLayout(layout)

    def load_data(self):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, name, status FROM tasks")
        tasks = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            for col, data in enumerate(task):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def update_status(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            task_id = int(self.table.item(selected_row, 0).text())
            new_status = self.status_combo.currentText()

            conn = connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (new_status, task_id))
            conn.commit()
            conn.close()

            self.load_data()

    def open_add_task_window(self):
        self.add_task_window = AddTaskWindow(self)
        self.add_task_window.show()

# Главное окно
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление данными")
        layout = QVBoxLayout()

        self.employee_button = QPushButton("Сотрудники")
        self.employee_button.clicked.connect(self.show_employees)
        layout.addWidget(self.employee_button)

        self.task_button = QPushButton("Задачи")
        self.task_button.clicked.connect(self.show_tasks)
        layout.addWidget(self.task_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_employees(self):
        self.employee_window = EmployeeWindow()
        self.employee_window.show()

    def show_tasks(self):
        self.task_window = TaskWindow()
        self.task_window.show()

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
