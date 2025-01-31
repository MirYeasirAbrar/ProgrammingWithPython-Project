import os


print("""
**************************************************
        Dhaka Internation University
Department of Computer Science and Engineering
**************************************************

     :: Academic Transcript Generator ::

""")
def read_student_data(filename):
    """Reads student data from a file and returns a dictionary."""
    if not os.path.exists(filename):
        return {}

    student_data = {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) < 3:
                continue

            student_id, course, grade = parts[0], parts[1], parts[2]
            grade = float(grade) if grade.replace('.', '', 1).isdigit() else 0.0

            if student_id not in student_data:
                student_data[student_id] = []

            student_data[student_id].append((course, grade))

    return student_data

def write_student_data(filename, student_data):
    """Writes student data back to the file."""
    with open(filename, 'w') as file:
        for student_id, courses in student_data.items():
            for course, grade in courses:
                file.write(f"{student_id},{course},{grade}\n")

def calculate_gpa(grades):
    """Calculates GPA from a list of grades."""
    if not grades:
        return 0.0

    total_points = sum(grades)
    return round(total_points / len(grades), 2)

def generate_transcript(student_data, output_file):
    """Generates academic transcripts and writes to a file."""
    with open(output_file, 'w') as file:
        for student_id, courses in student_data.items():
            file.write(f"Student ID: {student_id}\n")
            file.write("Courses:\n")

            grades = []
            for course, grade in courses:
                file.write(f"  {course}: {grade}\n")
                grades.append(grade)

            gpa = calculate_gpa(grades)
            file.write(f"GPA: {gpa}\n\n")

    print(f"Transcript has been generated in '{output_file}'.")

def add_result(student_data):
    """Adds a new result to the student data."""
    student_id = input("Enter Student ID: ").strip()
    course = input("Enter Course Name: ").strip()
    grade = input("Enter Grade: ").strip()

    try:
        grade = float(grade)
    except ValueError:
        print("Invalid grade. Must be a number.")
        return

    if student_id not in student_data:
        student_data[student_id] = []

    student_data[student_id].append((course, grade))
    print("Result added successfully.")

def edit_result(student_data):
    """Edits an existing result."""
    student_id = input("Enter Student ID: ").strip()

    if student_id not in student_data:
        print("Student ID not found.")
        return

    course = input("Enter Course Name to Edit: ").strip()

    for i, (c, grade) in enumerate(student_data[student_id]):
        if c == course:
            new_grade = input(f"Enter New Grade for {course}: ").strip()
            try:
                new_grade = float(new_grade)
                student_data[student_id][i] = (course, new_grade)
                print("Result updated successfully.")
                return
            except ValueError:
                print("Invalid grade. Must be a number.")
                return

    print("Course not found.")

def show_specific_result(student_data):
    """Shows results for a specific student."""
    student_id = input("Enter Student ID: ").strip()

    if student_id not in student_data:
        print("Student ID not found.")
        return

    print(f"Results for Student ID: {student_id}")
    grades = []
    for course, grade in student_data[student_id]:
        print(f"  {course}: {grade}")
        grades.append(grade)

    gpa = calculate_gpa(grades)
    print(f"GPA: {gpa}")

def show_all(student_data):
    """Shows results for all students."""
    if not student_data:
        print("No data available.")
        return

    for student_id, courses in student_data.items():
        print(f"Student ID: {student_id}")
        grades = []
        for course, grade in courses:
            print(f"  {course}: {grade}")
            grades.append(grade)

        gpa = calculate_gpa(grades)
        print(f"GPA: {gpa}\n")

def delete_result(student_data):
    """Deletes a result for a specific course of a student."""
    student_id = input("Enter Student ID: ").strip()

    if student_id not in student_data:
        print("Student ID not found.")
        return

    course = input("Enter Course Name to Delete: ").strip()

    for i, (c, grade) in enumerate(student_data[student_id]):
        if c == course:
            del student_data[student_id][i]
            if not student_data[student_id]:
                del student_data[student_id]  # Remove student if no courses left
            print("Result deleted successfully.")
            return

    print("Course not found.")

def main():
    input_file = 'student_data.txt'
    output_file = 'transcript.txt'

    student_data = read_student_data(input_file)

    while True:
        print("\nChoose an option:")
        print("1. Add Result")
        print("2. Edit Result")
        print("3. Show Specific Result")
        print("4. Show All")
        print("5. Delete Result")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_result(student_data)
        elif choice == '2':
            edit_result(student_data)
        elif choice == '3':
            show_specific_result(student_data)
        elif choice == '4':
            show_all(student_data)
        elif choice == '5':
            delete_result(student_data)
        elif choice == '6':
            write_student_data(input_file, student_data)
            print("Data saved. Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
