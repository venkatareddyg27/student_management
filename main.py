

from operations import (
    add_student, remove_student, update_student,
    search_students, list_all_students
)

def menu():
    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. Remove Student")
        print("3. Update Student")
        print("4. Search Student")
        print("5. List All Students")
        print("6. Exit")

        choice = input("Enter your choice: ")

        # 1. Add student
        if choice == "1":
            sid = input("Student ID: ")
            name = input("Name: ")
            age = input("Age: ")
            course = input("Course: ")
            email = input("Email: ")

            ok, msg = add_student(sid, name, age, course, email)
            print(msg)

        # 2. Remove student
        elif choice == "2":
            sid = input("Enter ID to remove: ")
            ok, msg = remove_student(sid)
            print(msg)

        # 3. Update student
        elif choice == "3":
            sid = input("Enter ID to update: ")

            print("Leave blank to keep the same value.")
            name = input("New Name: ")
            age = input("New Age: ")
            course = input("New Course: ")
            email = input("New Email: ")

            # Convert blank input to None
            if name == "":
                name = None
            if age == "":
                age = None
            if course == "":
                course = None
            if email == "":
                email = None

            ok, msg = update_student(sid, name=name, age_str=age, course=course, email=email)
            print(msg)

        # 4. Search
        elif choice == "4":
            keyword = input("Enter search keyword: ")
            ok, result = search_students(keyword)

            if ok:
                print("\nSearch Results:")
                for r in result:
                    print(r)
            else:
                print(result)

        # 5. List all
        elif choice == "5":
            ok, result = list_all_students()
            if ok:
                print("\nAll Students:")
                for r in result:
                    print(r)
            else:
                print(result)

        # 6. Exit
        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please enter 1–6.")

if __name__ == "__main__":
    menu()
