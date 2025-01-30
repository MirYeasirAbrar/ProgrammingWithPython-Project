import os
from abc import ABC, abstractmethod

print("""
----------------------------------------------------------------------
                      :: Online Exam System ::
----------------------------------------------------------------------
""")

# Abstract class for shared user behavior
class User(ABC):
    def __init__(self, username, password):
        self._username = username  # Encapsulation: Protecting username
        self._password = password  # Encapsulation: Protecting password

    @abstractmethod
    def display_info(self):
        pass  # Polymorphism: Enforced implementation in subclasses

    def login(self, username, password):
        return self._username == username and self._password == password


# Admin class inheriting from User class
class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.exams = {}  # Dictionary to store exam data
        self.student_results = {}  # Dictionary to store student results

    def add_exam(self, exam_name, department_name):
        """Add a new exam to the system."""
        if exam_name in self.exams:
            print("Exam already exists.")
        else:
            self.exams[exam_name] = {"department": department_name, "questions": []}
            print(f"Exam '{exam_name}' under department '{department_name}' added successfully.")

    def delete_exam(self, exam_name):
        """Delete an existing exam from the system."""
        if exam_name in self.exams:
            del self.exams[exam_name]
            print(f"Exam '{exam_name}' deleted successfully.")
        else:
            print("Exam does not exist.")

    def add_question(self, exam_name, question, options, correct_option):
        """Add a question to an existing exam."""
        if exam_name not in self.exams:
            print("Exam does not exist.")
            return

        if correct_option not in options:
            print("Correct option must be one of the provided options.")
            return

        self.exams[exam_name]["questions"].append({
            "question": question,
            "options": options,
            "correct": correct_option
        })
        print("Question added successfully.")

    def view_questions(self, exam_name):
        """View all questions in a specific exam."""
        if exam_name not in self.exams:
            print("Exam does not exist.")
            return

        questions = self.exams[exam_name]["questions"]
        if not questions:
            print("No questions available in this exam.")
            return

        print(f"Questions in exam '{exam_name}':")
        for idx, question in enumerate(questions, 1):
            print(f"{idx}. {question['question']}")
            for i, option in enumerate(question['options'], 1):
                print(f"   {i}. {option}")
            print(f"   Correct Answer: {question['correct']}")

    def edit_question(self, exam_name, question_index, new_question, new_options, new_correct_option):
        """Edit an existing question in an exam."""
        if exam_name not in self.exams:
            print("Exam does not exist.")
            return

        questions = self.exams[exam_name]["questions"]
        if question_index < 1 or question_index > len(questions):
            print("Invalid question index.")
            return

        if new_correct_option not in new_options:
            print("Correct option must be one of the provided options.")
            return

        questions[question_index - 1] = {
            "question": new_question,
            "options": new_options,
            "correct": new_correct_option
        }
        print("Question updated successfully.")

    def display_info(self):
        """Display admin information."""
        print(f"Admin: {self._username}")  # Polymorphism: Different display for Admin

    def view_exams(self):
        """View all exams created by the admin."""
        if not self.exams:
            print("No exams available.")
        else:
            for exam, data in self.exams.items():
                print(f"Exam: {exam} (Department: {data['department']}, {len(data['questions'])} questions)")

    def record_student_result(self, student_username, exam_name, score):
        """Record the score of a student for a specific exam."""
        if student_username not in self.student_results:
            self.student_results[student_username] = []
        self.student_results[student_username].append({"exam": exam_name, "score": score})

    def view_all_student_results(self):
        """Display all student results in a formatted table."""
        if not self.student_results:
            print("No student results available.")
            return

        results_list = []
        for student, results in self.student_results.items():
            for result in results:
                results_list.append({
                    "username": student,
                    "exam": result["exam"],
                    "score": result["score"],
                    "department": self.exams[result["exam"]]["department"]
                })

        # Sort results by department and username
        sorted_results = sorted(results_list, key=lambda x: (x["department"], x["username"]))

        print("\nStudent Results:")
        print(f"{'Serial No.':<12}{'Student Name':<15}{'Department':<15}{'Exam Name':<30}{'Result':<10}")
        print("=" * 80)

        for idx, result in enumerate(sorted_results, start=1):
            print(f"{idx:<12}{result['username']:<15}{result['department']:<15}{result['exam']:<30}{result['score']:<10}")


# Student class inheriting from User class
class Student(User):
    def __init__(self, username, password, department):
        super().__init__(username, password)
        self.department = department  # Store the department of the student
        self.results = {}  # Dictionary to store exam results

    def view_available_exams(self, all_exams):
        """View available exams for the student's department."""
        available_exams = {name: data for name, data in all_exams.items() if data['department'] == self.department}

        if not available_exams:
            print("No exams available for your department.")
            return []

        print("Available Exams:")
        for i, (exam_name, exam_data) in enumerate(available_exams.items(), 1):
            print(f"  {i}. {exam_name} (Department: {exam_data['department']}, {len(exam_data['questions'])} questions)")

        return list(available_exams.keys())

    def take_exam(self, exam_name, questions):
        """Take an exam and calculate the score."""
        if not questions:
            print("No questions available for this exam.")
            return

        score = 0
        print(f"Starting exam: {exam_name}\n")
        for i, q in enumerate(questions, 1):
            print(f"Q{i}: {q['question']}")
            for j, option in enumerate(q['options'], 1):
                print(f"  {j}. {option}")

            while True:
                try:
                    answer = int(input("Your answer: "))
                    if 1 <= answer <= len(q['options']):
                        break
                    else:
                        print("Invalid choice. Please select a valid option number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

            if q['options'][answer - 1] == q['correct']:
                score += 1

        self.results[exam_name] = score
        print(f"Exam completed. Your score: {score}/{len(questions)}")

    def view_results(self):
        """View the results of the exams taken by the student."""
        if not self.results:
            print("No results available.")
        else:
            for exam, score in self.results.items():
                print(f"{exam}: {score}")

    def display_info(self):
        """Display student information."""
        print(f"Student: {self._username} (Department: {self.department})")  # Polymorphism: Different display for Student


# Utility functions
def save_data(filename, data):
    """Save data to a file."""
    with open(filename, 'w') as file:
        file.write(str(data))


def load_data(filename):
    """Load data from a file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, 'r') as file:
        return eval(file.read())


def collect_all_exams(admins):
    """Aggregate all exams from all admins."""
    all_exams = {}
    for admin in admins.values():
        all_exams.update(admin.exams)
    return all_exams


def main():
    admin_data_file = "admin_data.txt"
    student_data_file = "student_data.txt"
    exams_data_file = "exams_data.txt"

    admins = load_data(admin_data_file)
    students = load_data(student_data_file)

    for username, password in admins.items():
        admins[username] = Admin(username, password)

    for username, (password, department) in students.items():
        students[username] = Student(username, password, department)

    while True:
        print("\nWelcome to the Online Examination System")
        print("1. Admin Login")
        print("2. Student Login")
        print("3. Admin Sign-Up")
        print("4. Student Sign-Up")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            username = input("Enter admin username: ").strip()
            password = input("Enter admin password: ").strip()

            if username in admins and admins[username].login(username, password):
                admin = admins[username]
                print("\nAdmin logged in successfully.")
                while True:
                    print("\nAdmin Menu")
                    print("1. Add Exam")
                    print("2. Delete Exam")
                    print("3. Add Question to Exam")
                    print("4. View Exams")
                    print("5. View Questions in Exam")
                    print("6. Edit Question in Exam")
                    print("7. View All Student Results")
                    print("8. Logout")

                    admin_choice = input("Enter your choice: ").strip()

                    if admin_choice == "1":
                        exam_name = input("Enter exam name: ").strip()
                        department_name = input("Enter department name: ").strip()
                        if exam_name and department_name:
                            admin.add_exam(exam_name, department_name)
                        else:
                            print("Exam name and department name cannot be empty.")
                    elif admin_choice == "2":
                        exam_name = input("Enter exam name to delete: ").strip()
                        admin.delete_exam(exam_name)
                    elif admin_choice == "3":
                        exam_name = input("Enter exam name: ").strip()
                        if exam_name not in admin.exams:
                            print("Invalid exam name. Please try again.")
                            continue
                        question = input("Enter question: ").strip()
                        if not question:
                            print("Question cannot be empty.")
                            continue
                        options = input("Enter options separated by commas: ").strip().split(',')
                        if len(options) < 2:
                            print("At least two options are required.")
                            continue
                        correct_option = input("Enter the correct option: ").strip()
                        admin.add_question(exam_name, question, options, correct_option)
                    elif admin_choice == "4":
                        admin.view_exams()
                    elif admin_choice == "5":
                        exam_name = input("Enter exam name: ").strip()
                        admin.view_questions(exam_name)
                    elif admin_choice == "6":
                        exam_name = input("Enter exam name: ").strip()
                        if exam_name not in admin.exams:
                            print("Invalid exam name. Please try again.")
                            continue

                        try:
                            question_index = int(input("Enter the question number to edit: ").strip())
                        except ValueError:
                            print("Invalid input. Please enter a valid question number.")
                            continue

                        new_question = input("Enter the new question: ").strip()
                        if not new_question:
                            print("Question cannot be empty.")
                            continue

                        new_options = input("Enter the new options separated by commas: ").strip().split(',')
                        if len(new_options) < 2:
                            print("At least two options are required.")
                            continue

                        new_correct_option = input("Enter the new correct option: ").strip()
                        admin.edit_question(exam_name, question_index, new_question, new_options, new_correct_option)
                    elif admin_choice == "7":
                        admin.view_all_student_results()
                    elif admin_choice == "8":
                        save_data(exams_data_file, {k: v.exams for k, v in admins.items()})
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice. Please select a valid option.")

            else:
                print("Invalid credentials. Please try again.")

        elif choice == "2":
            username = input("Enter student username: ").strip()
            password = input("Enter student password: ").strip()

            if username in students and students[username].login(username, password):
                student = students[username]
                print("\nStudent logged in successfully.")
                while True:
                    print("\nStudent Menu")
                    print("1. View Available Exams")
                    print("2. Take Exam")
                    print("3. View Results")
                    print("4. Logout")

                    student_choice = input("Enter your choice: ").strip()

                    if student_choice == "1":
                        all_exams = collect_all_exams(admins)
                        student.view_available_exams(all_exams)
                    elif student_choice == "2":
                        all_exams = collect_all_exams(admins)
                        available_exams = student.view_available_exams(all_exams)
                        if available_exams:
                            exam_choice = input("Enter the exam name you want to take: ").strip()
                            if exam_choice in all_exams:
                                student.take_exam(exam_choice, all_exams[exam_choice]["questions"])
                                # Record the result for the admin
                                score = student.results.get(exam_choice, 0)
                                for admin in admins.values():
                                    admin.record_student_result(student._username, exam_choice, score)
                            else:
                                print("Invalid exam name. Please choose from the available exams.")
                    elif student_choice == "3":
                        student.view_results()
                    elif student_choice == "4":
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice. Please select a valid option.")

            else:
                print("Invalid credentials. Please try again.")

        elif choice == "3":
            username = input("Enter new admin username: ").strip()
            password = input("Enter new admin password: ").strip()

            if not username or not password:
                print("Username and password cannot be empty.")
            elif username in admins:
                print("Admin username already exists.")
            else:
                admins[username] = Admin(username, password)
                save_data(admin_data_file, {k: v._password for k, v in admins.items()})
                print("Admin account created successfully.")

        elif choice == "4":
            username = input("Enter new student username: ").strip()
            password = input("Enter new student password: ").strip()
            department = input("Enter department: ").strip()

            if not username or not password or not department:
                print("Username, password, and department cannot be empty.")
            elif username in students:
                print("Student username already exists.")
            else:
                students[username] = Student(username, password, department)
                save_data(student_data_file, {k: (v._password, v.department) for k, v in students.items()})
                print("Student account created successfully.")

        elif choice == "5":
            save_data(admin_data_file, {k: v._password for k, v in admins.items()})
            save_data(student_data_file, {k: (v._password, v.department) for k, v in students.items()})
            save_data(exams_data_file, {k: v.exams for k, v in admins.items()})
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()