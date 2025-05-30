import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QLineEdit, QMessageBox, QListWidget, QDialog, QInputDialog, QComboBox, QCheckBox
)
import mysql.connector

class EgramSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_user_id = None
        self.is_user_admin = False
        self.is_user_professor = False

        self.setWindowTitle('EGRAM')

        
        self.setGeometry(100, 100, 800, 600)  

        self.db_conn = self.db_connect()
        self.active_widget = None  

        self.initialize_login_interface()  

    def initialize_login_interface(self):
        self.reset_layout()

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Sign In', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton('Sign Up', self)
        self.register_button.clicked.connect(self.display_signup_interface)
        layout.addWidget(self.register_button)

        self.set_main_widget(layout)

    def display_signup_interface(self):
        self.reset_layout()

        layout = QVBoxLayout()

        self.new_username_input = QLineEdit(self)
        self.new_username_input.setPlaceholderText('Username')
        layout.addWidget(self.new_username_input)

        self.new_password_input = QLineEdit(self)
        self.new_password_input.setPlaceholderText('Password')
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText('Email')  
        layout.addWidget(self.email_input)

        self.professor_checkbox = QCheckBox('Professor', self)
        layout.addWidget(self.professor_checkbox)

        self.create_account_btn = QPushButton('Create Account', self)
        self.create_account_btn.clicked.connect(self.signup)
        layout.addWidget(self.create_account_btn)

        self.back_to_login_btn = QPushButton('Back to Sign In', self)
        self.back_to_login_btn.clicked.connect(self.initialize_login_interface)
        layout.addWidget(self.back_to_login_btn)

        self.set_main_widget(layout)

    def set_main_widget(self, layout):
        if self.active_widget:
            self.active_widget.deleteLater()  

        self.active_widget = QWidget()
        self.active_widget.setLayout(layout)
        self.setCentralWidget(self.active_widget)

    def reset_layout(self):
        if self.active_widget:
            current_layout = self.active_widget.layout()
            if current_layout:
                while current_layout.count():
                    item = current_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

    def db_connect(self):
        try:
            db_connection = mysql.connector.connect(
                host='localhost',
                user='-------',
                password='----------',
                database='egram'
            )
            return db_connection
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            sys.exit(1)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        cursor = self.db_conn.cursor()
        query = "SELECT user_id, is_admin, is_professor FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            self.current_user_id = user[0]
            self.is_user_admin = user[1]
            self.is_user_professor = user[2]
            QMessageBox.information(self, 'Success', 'Login successful!')
            self.display_main_menu()  
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password.')

    def signup(self):
        username = self.new_username_input.text()
        password = self.new_password_input.text()
        email = self.email_input.text()
        is_professor = self.professor_checkbox.isChecked()

        if not username or not password or not email:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields.')
            return

        cursor = self.db_conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                QMessageBox.warning(self, 'Error', 'Username already exists. Please choose a different username.')
            else:
                insert_query = "INSERT INTO users (username, password, email, is_professor) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_query, (username, password, email, is_professor))
                self.db_conn.commit()
                QMessageBox.information(self, 'Success', 'Sign up successful! You can now sign in.')
        except mysql.connector.Error as err:
            QMessageBox.warning(self, 'Error', f'Failed to create account: {err}')

    def display_main_menu(self):
        layout = QVBoxLayout()

        if self.is_user_admin:
            self.add_course_btn = QPushButton('Add Course', self)
            self.add_course_btn.clicked.connect(self.add_course)
            layout.addWidget(self.add_course_btn)

            self.delete_course_btn = QPushButton('Delete Course', self)
            self.delete_course_btn.clicked.connect(self.delete_course)
            layout.addWidget(self.delete_course_btn)

            self.delete_user_btn = QPushButton('Delete User', self)
            self.delete_user_btn.clicked.connect(self.delete_user)
            layout.addWidget(self.delete_user_btn)
        elif self.is_user_professor:
            self.add_grades_btn = QPushButton('Add Grades', self)
            self.add_grades_btn.clicked.connect(self.add_grades)
            layout.addWidget(self.add_grades_btn)

            self.assign_course_btn = QPushButton('Assign Courses', self)
            self.assign_course_btn.clicked.connect(self.assign_courses)
            layout.addWidget(self.assign_course_btn)

            self.unenroll_course_btn = QPushButton('Unenroll from Course', self)
            self.unenroll_course_btn.clicked.connect(self.unenroll_course)
            layout.addWidget(self.unenroll_course_btn)
        else:
            self.view_grades_btn = QPushButton('Show Grades', self)
            self.view_grades_btn.clicked.connect(self.show_grades)
            layout.addWidget(self.view_grades_btn)

            self.enroll_course_btn = QPushButton('Enroll in Course', self)
            self.enroll_course_btn.clicked.connect(self.enroll_course)
            layout.addWidget(self.enroll_course_btn)

        self.contacts_btn = QPushButton('Contacts', self)
        self.contacts_btn.clicked.connect(self.show_contacts)
        layout.addWidget(self.contacts_btn)

        self.sign_out_btn = QPushButton('Sign Out', self)
        self.sign_out_btn.clicked.connect(self.sign_out)
        layout.addWidget(self.sign_out_btn)

        self.set_main_widget(layout)

        
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        if course_count == 0:
            if hasattr(self, 'enroll_course_btn'):
                self.enroll_course_btn.setEnabled(False)
            if self.is_user_professor and hasattr(self, 'unenroll_course_btn'):
                self.unenroll_course_btn.setEnabled(False)

    def add_course(self):
        course_name, ok = QInputDialog.getText(self, 'Add Course', 'Course Name:')
        if ok and course_name:
            cursor = self.db_conn.cursor()
            try:
                cursor.execute("INSERT INTO courses (course_name) VALUES (%s)", (course_name,))
                self.db_conn.commit()
                QMessageBox.information(self, 'Success', f'Course {course_name} added successfully!')
            except mysql.connector.Error as err:
                QMessageBox.warning(self, 'Error', f'Failed to add course: {err}')

    def delete_course(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT course_name FROM courses")
        courses = cursor.fetchall()
        course_names = [course[0] for course in courses]

        course_to_delete, ok = QInputDialog.getItem(self, "Delete Course", "Select course to delete:", course_names, 0, False)
        if ok and course_to_delete:
            try:
                cursor.execute("DELETE FROM enrolled_courses WHERE course_name = %s", (course_to_delete,))
                cursor.execute("DELETE FROM grades WHERE course_name = %s", (course_to_delete,))
                cursor.execute("DELETE FROM professor_courses WHERE course_name = %s", (course_to_delete,))
                cursor.execute("DELETE FROM courses WHERE course_name = %s", (course_to_delete,))
                self.db_conn.commit()

               
                cursor.execute("CREATE TEMPORARY TABLE temp_courses AS SELECT course_name FROM courses;")
                cursor.execute("DELETE FROM courses;")
                cursor.execute("ALTER TABLE courses AUTO_INCREMENT = 1;")
                cursor.execute("INSERT INTO courses (course_name) SELECT course_name FROM temp_courses;")
                cursor.execute("DROP TEMPORARY TABLE temp_courses;")

                self.db_conn.commit()

                QMessageBox.information(self, 'Success', f'Course {course_to_delete} and all related records deleted successfully!')
            except mysql.connector.Error as err:
                QMessageBox.warning(self, 'Error', f'Failed to delete course: {err}')

    def delete_user(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT username FROM users WHERE user_id != %s", (self.current_user_id,))
        users = cursor.fetchall()
        usernames = [user[0] for user in users]

        user_to_delete, ok = QInputDialog.getItem(self, "Delete User", "Select user to delete:", usernames, 0, False)
        if ok and user_to_delete:
            try:
                cursor.execute("SELECT user_id FROM users WHERE username = %s", (user_to_delete,))
                user_id = cursor.fetchone()[0]
                
                cursor.execute("DELETE FROM professor_courses WHERE professor_id = %s", (user_id,))
                cursor.execute("DELETE FROM enrolled_courses WHERE user_id = %s", (user_id,))
                cursor.execute("DELETE FROM grades WHERE user_id = %s", (user_id,))
                cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
                self.db_conn.commit()

                # Επαναφορά των ID στον πίνακα users
                cursor.execute("CREATE TEMPORARY TABLE temp_users AS SELECT username, password, email, is_admin, is_professor FROM users;")
                cursor.execute("DELETE FROM users;")
                cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1;")
                cursor.execute("INSERT INTO users (username, password, email, is_admin, is_professor) SELECT username, password, email, is_admin, is_professor FROM temp_users;")
                cursor.execute("DROP TEMPORARY TABLE temp_users;")

                
                cursor.execute("SELECT user_id, username FROM users;")
                new_users = cursor.fetchall()
                for new_user_id, username in new_users:
                    cursor.execute("UPDATE enrolled_courses SET user_id = %s WHERE user_id = %s;", (new_user_id, user_id))
                    cursor.execute("UPDATE grades SET user_id = %s WHERE user_id = %s;", (new_user_id, user_id))
                    cursor.execute("UPDATE professor_courses SET professor_id = %s WHERE professor_id = %s;", (new_user_id, user_id))

                self.db_conn.commit()

                QMessageBox.information(self, 'Success', f'User {user_to_delete} and all related records deleted successfully!')
            except mysql.connector.Error as err:
                QMessageBox.warning(self, 'Error', f'Failed to delete user: {err}')

    def show_contacts(self):
        if self.current_user_id is None:
            QMessageBox.warning(self, 'Error', 'User is not logged in.')
            return

        try:
            cursor = self.db_conn.cursor()
            cursor.execute("SELECT username, email FROM users")
            users = cursor.fetchall()

            if not users:
                QMessageBox.information(self, 'No Contacts', 'No contacts found.')
                return

            contacts_window = QDialog(self)
            contacts_window.setWindowTitle('Contacts')

            
            contacts_window.setGeometry(100, 100, 600, 400)  #

            layout = QVBoxLayout()
            contacts_list = QListWidget()

            for username, email in users:
                contacts_list.addItem(f'{username} - {email}')

            layout.addWidget(contacts_list)
            contacts_window.setLayout(layout)
            contacts_window.exec_()
            
        except mysql.connector.Error as err:
            print(f"Error fetching contacts: {err}")
            QMessageBox.warning(self, 'Error', 'Failed to fetch contacts.')

    def show_grades(self):
        if self.current_user_id is None:
            QMessageBox.warning(self, 'Error', 'User is not logged in.')
            return

        cursor = self.db_conn.cursor()
        query = """
        SELECT ec.course_name, COALESCE(g.grade, '-') AS grade
        FROM enrolled_courses ec
        LEFT JOIN grades g ON ec.user_id = g.user_id AND ec.course_name = g.course_name
        WHERE ec.user_id = %s
        """
        cursor.execute(query, (self.current_user_id,))
        grades = cursor.fetchall()

        grades_dialog = QDialog(self)
        grades_dialog.setWindowTitle('Grades')
        
        
        grades_dialog.setGeometry(100, 100, 600, 400)  
        
        layout = QVBoxLayout()
        grades_list = QListWidget()

        if not grades:
            grades_list.addItem("No grades available.")  

        for course_name, grade in grades:
            grades_list.addItem(f'{course_name}: {grade}')

        layout.addWidget(grades_list)
        grades_dialog.setLayout(layout)
        grades_dialog.exec_()

    def enroll_course(self):
        if self.current_user_id is None:
            QMessageBox.warning(self, 'Error', 'User is not logged in.')
            return

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT course_name FROM courses")
        courses = cursor.fetchall()
        course_names = [course[0] for course in courses]

        if not course_names:
            QMessageBox.warning(self, 'Error', 'No courses available.')
            return

        course_name, ok = QInputDialog.getItem(self, "Enroll in Course", "Select course:", course_names, 0, False)
        if ok and course_name:
            try:
                
                check_query = "SELECT * FROM enrolled_courses WHERE user_id = %s AND course_name = %s"
                cursor.execute(check_query, (self.current_user_id, course_name))
                existing_enrollment = cursor.fetchone()
                
                if existing_enrollment:
                    QMessageBox.warning(self, 'Error', f'You are already enrolled in {course_name}.')
                else:
                    insert_query = "INSERT INTO enrolled_courses (user_id, course_name) VALUES (%s, %s)"
                    cursor.execute(insert_query, (self.current_user_id, course_name))
                    self.db_conn.commit()
                    QMessageBox.information(self, 'Success', f'Enrolled in {course_name} successfully!')
            except mysql.connector.Error as err:
                print(f"Error enrolling in course: {err}")
                QMessageBox.warning(self, 'Error', 'Failed to enroll in course.')

    def unenroll_course(self):
        if not self.is_user_professor:
            QMessageBox.warning(self, 'Error', 'You do not have permission to unenroll from courses.')
            return

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT course_name FROM professor_courses WHERE professor_id = %s", (self.current_user_id,))
        courses = cursor.fetchall()
        course_names = [course[0] for course in courses]

        if not course_names:
            QMessageBox.warning(self, 'Error', 'You have not been assigned any courses.')
            return

        course_name, ok = QInputDialog.getItem(self, "Unenroll from Course", "Select course to unenroll:", course_names, 0, False)
        if not ok or not course_name:
            return

        try:
            cursor.execute("DELETE FROM professor_courses WHERE professor_id = %s AND course_name = %s", (self.current_user_id, course_name))
            cursor.execute("DELETE FROM enrolled_courses WHERE course_name = %s", (course_name,))
            cursor.execute("DELETE FROM grades WHERE course_name = %s", (course_name,))
            self.db_conn.commit()
            QMessageBox.information(self, 'Success', f'Unenrolled from course {course_name} successfully! All students also unenrolled.')
        except mysql.connector.Error as err:
            QMessageBox.warning(self, 'Error', f'Failed to unenroll from course: {err}')

    def add_grades(self):
        if not self.is_user_professor:
            QMessageBox.warning(self, 'Error', 'You do not have permission to add grades.')
            return

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT course_name FROM professor_courses WHERE professor_id = %s", (self.current_user_id,))
        courses = cursor.fetchall()
        course_names = [course[0] for course in courses]

        if not course_names:
            QMessageBox.warning(self, 'Error', 'You have not been assigned any courses.')
            return

        course_name, ok = QInputDialog.getItem(self, "Select Course", "Select course to add grades:", course_names, 0, False)
        if not ok or not course_name:
            return

        cursor.execute("SELECT u.username FROM enrolled_courses ec JOIN users u ON ec.user_id = u.user_id WHERE ec.course_name = %s", (course_name,))
        users = cursor.fetchall()
        usernames = [user[0] for user in users]

        if not usernames:
            QMessageBox.warning(self, 'Error', f'No students are enrolled in the course {course_name}.')
            return

        user_dialog = QDialog(self)
        user_dialog.setWindowTitle('Select User')
        layout = QVBoxLayout()

        self.user_combo_box = QComboBox()
        self.user_combo_box.addItems(usernames)
        layout.addWidget(self.user_combo_box)

        select_button = QPushButton('Select')
        select_button.clicked.connect(lambda: self.add_grades_for_user(self.user_combo_box.currentText(), course_name, user_dialog))
        layout.addWidget(select_button)

        user_dialog.setLayout(layout)
        user_dialog.exec_()

    def add_grades_for_user(self, username, course_name, user_dialog):
        user_dialog.accept()

        add_grades_dialog = QDialog(self)
        add_grades_dialog.setWindowTitle(f'Add Grades for {username}')
        layout = QVBoxLayout()

        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText('Enter grade')
        layout.addWidget(self.grade_input)

        submit_button = QPushButton('Submit Grade')
        submit_button.clicked.connect(lambda: self.submit_grade(username, course_name, add_grades_dialog))
        layout.addWidget(submit_button)

        add_grades_dialog.setLayout(layout)
        add_grades_dialog.exec_()

    def submit_grade(self, username, course_name, dialog):
        grade = self.grade_input.text()
        if not grade:
            QMessageBox.warning(self, 'Error', 'Please enter a grade.')
            return

        cursor = self.db_conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            user_id = user[0]
            try:
                cursor.execute("""
                    INSERT INTO grades (user_id, course_name, grade)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE grade = VALUES(grade)
                """, (user_id, course_name, grade))
                self.db_conn.commit()
                QMessageBox.information(self, 'Success', 'Grade submitted successfully!')
                dialog.accept()
            except mysql.connector.Error as err:
                QMessageBox.warning(self, 'Error', f'Failed to submit grade: {err}')

    def assign_courses(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT course_name FROM courses")
        courses = cursor.fetchall()
        course_names = [course[0] for course in courses]

        course_name, ok = QInputDialog.getItem(self, "Assign Course", "Select course:", course_names, 0, False)
        if ok and course_name:
            try:
                cursor.execute("INSERT INTO professor_courses (professor_id, course_name) VALUES (%s, %s)",
                               (self.current_user_id, course_name))
                self.db_conn.commit()
                QMessageBox.information(self, 'Success', f'Assigned to course {course_name} successfully!')
            except mysql.connector.Error as err:
                QMessageBox.warning(self, 'Error', f'Failed to assign course: {err}')

    def sign_out(self):
        self.current_user_id = None
        self.is_user_admin = False
        self.is_user_professor = False
        QMessageBox.information(self, 'Success', 'You have been signed out.')
        self.initialize_login_interface()

    def get_logged_in_user_id(self):
        return self.current_user_id

if __name__ == '__main__':
    app = QApplication(sys.argv)
    email_app = EgramSystem()
    email_app.show()
    sys.exit(app.exec_())