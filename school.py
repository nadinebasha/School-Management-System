import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import json
import os

# Data Structure Implementations

class Node:
    """
    Represents a node in a linked list.
    """
    def __init__(self, data):
        """
        Initializes a new node.

        Args:
            data: The data to be stored in the node.
        """
        self.data = data
        self.next = None

class LinkedList:
    """
    Implements a singly linked list.
    """
    def __init__(self):
        """
        Initializes an empty linked list.
        """
        self.head = None

    def append(self, data):
        """
        Appends a new node with the given data to the end of the list.

        Args:
            data: The data to be appended.
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def remove(self, data):
        """
        Removes the first node with the given data from the list.

        Args:
            data: The data to be removed.
        """
        current_node = self.head
        if current_node and current_node.data == data:
            self.head = current_node.next
            current_node = None
            return
        previous_node = None
        while current_node and current_node.data != data:
            previous_node = current_node
            current_node = current_node.next
        if current_node is None:
             return
        previous_node.next = current_node.next
        current_node = None
    
    def to_list(self):
         """
         Converts the linked list to a Python list.
         
         Returns:
             list: A list of the data in the linked list
         """
         elements = []
         current = self.head
         while current:
            elements.append(current.data)
            current = current.next
         return elements

class Queue:
    """
    Implements a queue data structure.
    """
    def __init__(self):
        """
        Initializes an empty queue.
        """
        self.items = []

    def enqueue(self, item):
        """
        Adds an item to the end of the queue.

        Args:
            item: The item to be added.
        """
        self.items.append(item)

    def dequeue(self):
        """
        Removes and returns the item at the front of the queue.

        Returns:
             The item at the front of the queue or None if the queue is empty.
        """
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        """
        Checks if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.items) == 0

class Stack:
    """
    Implements a stack data structure.
    """
    def __init__(self):
        """
        Initializes an empty stack.
        """
        self.items = []

    def push(self, item):
        """
        Adds an item to the top of the stack.

        Args:
            item: The item to be added.
        """
        self.items.append(item)

    def pop(self):
        """
        Removes and returns the item at the top of the stack.

        Returns:
            The item at the top of the stack or None if the stack is empty.
        """
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """
        Returns the item at the top of the stack without removing it.
        
        Returns:
            The item at the top of the stack, or None if the stack is empty.
        """
        if not self.is_empty():
          return self.items[-1]
        return None
    def is_empty(self):
        """
        Checks if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self.items) == 0
    
class TreeNode:
    """
    Represents a node in a tree data structure.
    """
    def __init__(self, data):
        """
        Initializes a tree node.

        Args:
            data: The data to be stored in the node.
        """
        self.data = data
        self.children = []
    
    def add_child(self, child):
        """
        Adds a child node to this node.

        Args:
           child: The child TreeNode to add.
        """
        self.children.append(child)

class SchoolManagementSystem:
    """
    Implements a School Management System GUI using Tkinter.
    """
    def __init__(self, root):
        """
        Initializes the School Management System.

        Args:
            root: The Tkinter root window.
        """
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#e6f2ff")

        # Font settings
        self.title_font = ("Helvetica", 20, "bold")
        self.label_font = ("Arial", 13)
        self.button_font = ("Arial", 12, "bold")
        self.entry_font = ("Arial",12)

        # Color settings
        self.button_color = "#4caf50" 
        self.button_hover_color = "#45a049"
        self.label_color = "#333333" 
        self.text_color = "#555555" 
        self.entry_color = "#ffffff" 
        self.entry_bg_color ="#f0f0f0"

        # Data Storage
        self.students = {}
        self.majors = {}
        self.grades = {}
        self.schedules = {}
        self.student_feedback = Queue()
        self.navigation_stack = Stack()
        # Major Course Tree
        self.major_tree = TreeNode("Majors")
         # Initial majors and courses
        self.default_majors = {
            "Business": ["Accounting", "Marketing", "Management", "Economics","Business Law","Financial Analysis","Human Resources"],
            "Computer Science": ["Data Structures", "Algorithms", "Databases", "Operating Systems","Web Development","Software Engineering","Artificial Intelligence"],
            "Media": ["Film Production", "Journalism", "Digital Media", "Graphic Design","Photography","Video Editing","Social Media Management"]
        }

        # File paths
        self.students_file = "students.json"
        self.grades_file = "grades.json"
        self.schedules_file = "schedules.json"
        self.feedback_file = "feedback.json"
        
        # Load data
        self.load_data()

        # Hash passwords
        self.hashed_admin_password = self.hash_password("admin123")

        self.current_user = None
        self.create_login_page()

        # Configure button style
        style = ttk.Style()
        style.configure("TButton", font=self.button_font, background=self.button_color, foreground="black", padding=8, relief="flat")
        style.map("TButton", background=[("active", self.button_hover_color)])

        style.configure("TCombobox", font=self.entry_font, padding=6)
        style.configure("TLabel", font=self.label_font)

    def hash_password(self, password):
        """
        Hashes a password using SHA256.

        Args:
            password: The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, stored_hash, password):
        """
        Verifies a password against a stored hash.

        Args:
           stored_hash: The stored hash value.
           password: The password to be verified.

        Returns:
           bool: True if the password matches the hash, False otherwise.
        """
        hashed_password = self.hash_password(password)
        return hashed_password == stored_hash
    
    def load_data(self):
        """
        Loads data from JSON files into the application's data structures.
        """
        try:
            if os.path.exists(self.students_file):
                with open(self.students_file, "r") as f:
                    self.students = json.load(f)
            if os.path.exists(self.grades_file):
                with open(self.grades_file, "r") as f:
                    self.grades = json.load(f)
            if os.path.exists(self.schedules_file):
                with open(self.schedules_file, "r") as f:
                    self.schedules = json.load(f)
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, "r") as f:
                    loaded_feedback = json.load(f)
                    for item in loaded_feedback:
                         self.student_feedback.enqueue(item)
            
            # Load majors into the tree
            if os.path.exists("majors.json"):
                with open("majors.json", "r") as f:
                    loaded_majors = json.load(f)
                    for major, courses in loaded_majors.items():
                        major_node = TreeNode(major)
                        self.major_tree.add_child(major_node)
                        for course in courses:
                            course_node = TreeNode(course)
                            major_node.add_child(course_node)
            else:
                 # Initialize tree with default data
                 for major, courses in self.default_majors.items():
                     major_node = TreeNode(major)
                     self.major_tree.add_child(major_node)
                     for course in courses:
                        course_node = TreeNode(course)
                        major_node.add_child(course_node)
            
            # Load majors into linked list
            if os.path.exists("majors_list.json"):
                with open("majors_list.json", "r") as f:
                    loaded_majors = json.load(f)
                    for major, student_ids in loaded_majors.items():
                        self.majors[major] = LinkedList()
                        for student_id in student_ids:
                            self.majors[major].append(student_id)
            else:
               for major, courses in self.default_majors.items():
                  self.majors[major] = LinkedList() # initialize linked list for each major

        except (FileNotFoundError, json.JSONDecodeError):
             self.students = {}
             # Initialize tree with default data
             for major, courses in self.default_majors.items():
                 major_node = TreeNode(major)
                 self.major_tree.add_child(major_node)
                 for course in courses:
                    course_node = TreeNode(course)
                    major_node.add_child(course_node)
             for major, courses in self.default_majors.items():
                  self.majors[major] = LinkedList() # initialize linked list for each major

    def save_data(self):
         """
         Saves the application's data structures to JSON files.
         """
         files = {
            self.students_file : self.students,
            self.grades_file : self.grades,
            self.schedules_file : self.schedules
        }
         for file_path , data in files.items():
            with open(file_path, "w") as f:
                json.dump(data, f)
         with open("majors.json", "w") as f:
            majors_dict = {}
            for node in self.major_tree.children:
                courses_list = [course.data for course in node.children]
                majors_dict[node.data] = courses_list
            json.dump(majors_dict, f)

         feedback_list = []
         while not self.student_feedback.is_empty():
              feedback_list.append(self.student_feedback.dequeue())
         with open(self.feedback_file, "w") as f:
            json.dump(feedback_list, f)

         majors_list_dict = {}
         for major, linked_list in self.majors.items():
           majors_list_dict[major] = linked_list.to_list()
         with open("majors_list.json", "w") as f:
            json.dump(majors_list_dict,f)

    def create_login_page(self):
        """
        Creates the initial login page.
        """
        self.clear_window()
        self.create_label("Login As:", self.title_font).pack(pady=20)
        self.create_button("Admin Login", self.admin_login_page).pack(pady=10)
        self.create_button("Student Login", self.student_login_page).pack(pady=10)
        
        self.navigation_stack.push("login_page")
    
    def clear_window(self):
        """
        Clears all widgets from the main window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_label(self, text, font=None, color=None):
        """
        Creates a styled label.

        Args:
          text: The text of the label.
          font: The font of the label (optional).
          color: The color of the label (optional).

        Returns:
            ttk.Label: The created label widget.
        """
        font = font or self.label_font
        color = color or self.label_color
        return ttk.Label(self.root, text=text, font=font, foreground=color, background="#e6f2ff")
    
    def create_entry(self,show=None):
        """
        Creates a styled entry field.

        Args:
            show: The character to mask the entry (optional, for passwords).

        Returns:
             ttk.Entry: The created entry widget.
        """
        entry = ttk.Entry(self.root,show=show, font=self.entry_font)
        entry.configure(foreground=self.text_color, background=self.entry_bg_color)
        return entry
    
    def create_button(self,text,command):
        """
        Creates a styled button.

        Args:
           text: The text of the button.
           command: The command to be executed when the button is pressed.

        Returns:
            ttk.Button: The created button widget.
        """
        return ttk.Button(self.root, text=text, command=command, style="TButton")

    def admin_login_page(self):
         """
         Creates the admin login page.
         """
         self.clear_window()
         self.create_label("Username:").pack()
         username_entry = self.create_entry()
         username_entry.pack()
         self.create_label("Password:").pack()
         password_entry = self.create_entry(show="*")
         password_entry.pack()
         self.create_button("Login", lambda: self.admin_login(username_entry.get(), password_entry.get())).pack(pady=10)
         self.create_button("Back", self.navigate_back).pack(pady=10)
         self.navigation_stack.push("admin_login_page")
    
    def navigate_back(self):
         """
         Navigates back to the previous page using the navigation stack.
         """
         if self.navigation_stack.peek() == "login_page":
           return
         self.navigation_stack.pop()
         previous_page = self.navigation_stack.peek()
         if previous_page == "login_page":
            self.create_login_page()
         elif previous_page == "admin_login_page":
             self.admin_login_page()
         elif previous_page == "admin_dashboard":
             self.create_admin_dashboard()
         elif previous_page == "add_student_page":
             self.add_student_page()
         elif previous_page == "edit_student_page":
             self.edit_student_page()
         elif previous_page == "delete_student_page":
             self.delete_student_page()
         elif previous_page == "grading_page":
             self.grading_page()
         elif previous_page == "enrolled_students_page":
              self.enrolled_students_page()
         elif previous_page == "schedule_page":
             self.schedule_page()
         elif previous_page == "admin_feedback_page":
              self.admin_feedback_page()
         elif previous_page == "student_login_page":
             self.student_login_page()
         elif previous_page == "student_dashboard":
             self.create_student_dashboard()
         elif previous_page == "student_profile_page":
             self.student_profile_page()
         elif previous_page == "change_password_page":
             self.change_password_page()
         elif previous_page == "student_courses_page":
            self.student_courses_page()
         elif previous_page == "student_grades_page":
             self.student_grades_page()
         elif previous_page == "student_schedule_page":
             self.student_schedule_page()
         elif previous_page == "student_feedback_page":
             self.student_feedback_page()

    def admin_login(self, username, password):
        """
        Handles the admin login logic.

        Args:
           username: The entered username.
           password: The entered password.
        """
        if username == "admin" and self.verify_password(self.hashed_admin_password, password):
            self.current_user = "admin"
            self.create_admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_admin_dashboard(self):
         """
         Creates the main admin dashboard.
         """
         self.clear_window()
         self.create_admin_menu()
         self.create_label("Admin Dashboard", self.title_font).pack(pady=20)
         self.create_label("Welcome Admin!", font=("Arial", 16), color="#007BFF").pack(pady=20)
         self.create_label("Use the 'Admin' menu to manage the system.", font=("Arial", 10), color=self.text_color).pack(pady=10)
         self.navigation_stack.push("admin_dashboard")
        
    def create_admin_menu(self):
        """
        Creates the admin menu bar.
        """
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        admin_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Admin", menu=admin_menu)
        
        admin_menu.add_command(label="Add Student", command=self.add_student_page)
        admin_menu.add_command(label="Grading", command=self.grading_page)
        admin_menu.add_command(label="Enrolled Students", command=self.enrolled_students_page)
        admin_menu.add_command(label="Schedule", command=self.schedule_page)
        admin_menu.add_command(label="Student Feedback", command=self.admin_feedback_page)
        admin_menu.add_separator()
        admin_menu.add_command(label="Logout", command=self.logout)
        admin_menu.add_separator()
        admin_menu.add_command(label="Back to Admin Dashboard", command=self.navigate_back)
    
    def add_student_page(self):
        """
        Creates the add student page.
        """
        self.clear_window()
        name_entry = self.create_entry_with_label("Student Name:")
        id_entry = self.create_entry_with_label("Student ID:")
        password_entry = self.create_entry_with_label("Password:", show="*")
        year_entry = self.create_entry_with_label("Year:")
        major_combo = self.create_combobox_with_label("Major:", self.get_major_names())
       
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(pady=10)

        self.create_button("Add Student",lambda: self.add_student(name_entry.get(), id_entry.get(),password_entry.get(), year_entry.get(), major_combo.get())).pack(in_=buttons_frame, side=tk.LEFT, padx=5)
        self.create_button("Edit Student", self.edit_student_page).pack(in_=buttons_frame, side=tk.LEFT, padx=5)
        self.create_button("Delete Student", self.delete_student_page).pack(in_=buttons_frame, side=tk.LEFT, padx=5)
        self.create_button("Back to Admin Dashboard", self.navigate_back).pack()
        self.navigation_stack.push("add_student_page")
        
    def create_entry_with_label(self, label_text, show=None):
        """
        Creates an entry field with a label.

        Args:
           label_text: The text of the label.
           show: The character to mask the entry (optional, for passwords).
        
        Returns:
           ttk.Entry: The created entry widget.
        """
        self.create_label(label_text).pack()
        entry = self.create_entry(show=show)
        entry.pack()
        return entry
    
    def create_combobox_with_label(self, label_text, values):
         """
         Creates a combobox with a label.

         Args:
            label_text: The text of the label.
            values: The list of values for the combobox.

         Returns:
            ttk.Combobox: The created combobox widget.
         """
         self.create_label(label_text).pack()
         combo = ttk.Combobox(self.root, values=values, style="TCombobox")
         combo.pack()
         return combo
    
    def get_major_names(self):
        """
        Retrieves major names from the linked list, ensuring dynamic updates.
        
        Returns:
            list: A list of major names
        """
        return list(self.majors.keys())

    def add_student(self, name, student_id, password, year, major):
         """
         Adds a new student to the system.

         Args:
             name: The name of the student.
             student_id: The unique ID of the student.
             password: The password for the student account.
             year: The student's year of study.
             major: The student's major.
         """
         if name and student_id and password and year and major:
            hashed_password = self.hash_password(password)
            self.students[student_id] = {"name": name, "password": hashed_password,"year": year,"major": major,"courses": []}
            self.save_data()
            
            if major not in self.majors:
              self.majors[major] = LinkedList()
            self.majors[major].append(student_id)
            self.save_data()

            messagebox.showinfo("Success", "Student added successfully")
         else:
             messagebox.showerror("Error", "All fields are required")
    
    def edit_student_page(self):
         """
         Creates the edit student page.
         """
         self.clear_window()
         id_entry = self.create_entry_with_label("Enter Student ID to Edit:")
         self.create_button("Edit", lambda: self.edit_student_details(id_entry.get())).pack(pady=10)
         self.create_button("Back to Add Student Page", self.navigate_back).pack()
         self.navigation_stack.push("edit_student_page")

    def edit_student_details(self, student_id):
         """
         Displays the details of the student for editing.

         Args:
             student_id: The ID of the student to edit.
         """
         if student_id in self.students:
           self.clear_window()
           student_data = self.students[student_id]
           name_entry = self.create_entry_with_label("Student Name:")
           name_entry.insert(0,student_data["name"])
           id_entry = self.create_entry_with_label("Student ID:")
           id_entry.insert(0,student_id)
           id_entry.config(state=tk.DISABLED)
           year_entry = self.create_entry_with_label("Year:")
           year_entry.insert(0,student_data["year"])
           major_combo = self.create_combobox_with_label("Major:", self.get_major_names())
           major_combo.set(student_data["major"])
           self.create_button("Save", lambda: self.save_edited_student(name_entry.get(), id_entry.get(), year_entry.get(), major_combo.get())).pack(pady=10)
           self.create_button("Back to Add Student Page", self.navigate_back).pack()
           
         else:
           messagebox.showerror("Error", "Student not found.")
    
    def save_edited_student(self,name, student_id, year, major):
         """
         Saves the edited student details.

         Args:
            name: The edited name of the student.
            student_id: The ID of the student to edit.
            year: The edited year of the student.
            major: The edited major of the student.
         """
         if name and student_id and year and major:
            old_major = self.students[student_id]["major"]
            self.students[student_id]["name"] = name
            self.students[student_id]["year"] = year
            if old_major != major:
              self.majors[old_major].remove(student_id)
              if major not in self.majors:
                self.majors[major] = LinkedList()
              self.majors[major].append(student_id)
              self.students[student_id]["major"] = major
              self.students[student_id]["courses"] = self.get_course_list(major)

            self.save_data()
            messagebox.showinfo("Success", "Student updated successfully")
            self.add_student_page()
         else:
            messagebox.showerror("Error", "All fields are required")

    def get_course_list(self, major):
         """
         Retrieves the list of courses for a given major.

         Args:
            major: The name of the major.

         Returns:
            list: A list of courses associated with the major.
         """
         for major_node in self.major_tree.children:
            if major_node.data == major:
                return [course_node.data for course_node in major_node.children]
         return []
            
    def delete_student_page(self):
         """
         Creates the delete student page.
         """
         self.clear_window()
         id_entry = self.create_entry_with_label("Enter Student ID to Delete:")
         self.create_button("Delete", lambda: self.delete_student(id_entry.get())).pack(pady=10)
         self.create_button("Back to Add Student Page", self.navigate_back).pack()
         self.navigation_stack.push("delete_student_page")

    def delete_student(self, student_id):
        """
        Deletes a student from the system.

        Args:
            student_id: The ID of the student to delete.
        """
        if student_id in self.students:
            major = self.students[student_id]["major"]
            self.majors[major].remove(student_id)
            del self.students[student_id]
            if student_id in self.grades:
                del self.grades[student_id]
            self.save_data()
            messagebox.showinfo("Success", "Student deleted successfully")
            self.add_student_page()
        else:
            messagebox.showerror("Error", "Student not found.")
    
    def grading_page(self):
        """
        Creates the grading page.
        """
        self.clear_window()
        student_combo = self.create_combobox_with_label("Select Student ID:", list(self.students.keys()))
        course_combo = self.create_combobox_with_label("Select Course:", [])
        student_combo.bind("<<ComboboxSelected>>", lambda event: self.update_courses(course_combo, student_combo.get()))
        grade_entry = self.create_entry_with_label("Enter Grade Percentage:")
        self.create_button("Submit Grade", lambda: self.submit_grade(student_combo.get(), course_combo.get(), grade_entry.get())).pack(pady=10)
        self.create_button("Back to Admin Dashboard", self.navigate_back).pack()
        self.navigation_stack.push("grading_page")
    
    def update_courses(self,course_combo, selected_student):
        """
        Updates the courses dropdown based on the selected student.

        Args:
           course_combo: The combobox to be updated with courses.
           selected_student: The student ID selected.
        """
        if selected_student in self.students:
            course_combo["values"] = self.students[selected_student].get("courses", [])
        else:
            course_combo["values"] = []

    def submit_grade(self, student_id, course, grade_percentage):
        """
        Submits a grade for a student in a course.

        Args:
            student_id: The ID of the student.
            course: The name of the course.
            grade_percentage: The grade as percentage.
        """
        if not student_id or not course or not grade_percentage:
            messagebox.showerror("Error", "Please select a student, course and enter a grade.")
            return
         
        try:
             grade_percentage = int(grade_percentage)
             if student_id in self.students and course in self.students[student_id].get("courses", []):
                if 97 <= grade_percentage <= 100:
                    grade = "A+"
                elif 93 <= grade_percentage < 97:
                     grade = "A"
                elif 90 <= grade_percentage < 93:
                     grade = "A-"
                elif 87 <= grade_percentage < 90:
                     grade = "B+"
                elif 83 <= grade_percentage < 87:
                     grade = "B"
                elif 80 <= grade_percentage < 83:
                     grade = "B-"
                elif 77 <= grade_percentage < 80:
                     grade = "C+"
                elif 73 <= grade_percentage < 77:
                     grade = "C"
                elif 70 <= grade_percentage < 73:
                     grade = "C-"
                elif 67 <= grade_percentage < 70:
                     grade = "D+"
                elif 63 <= grade_percentage < 67:
                     grade = "D"
                elif 60 <= grade_percentage < 63:
                     grade = "D-"
                else:
                     grade = "F"
                  
                if student_id not in self.grades:
                    self.grades[student_id] = {}
                self.grades[student_id][course] = grade
                self.save_data()
                messagebox.showinfo("Success", f"Grade '{grade}' added for {student_id} in {course}")
             else:
                 messagebox.showerror("Error", "Invalid student or course.")
        except ValueError:
             messagebox.showerror("Error", "Invalid grade percentage.")

    def enrolled_students_page(self):
      """
      Creates the enrolled students page.
      """
      self.clear_window()
      tree = ttk.Treeview(self.root, columns=("Name", "ID", "Courses", "Major"), show="headings")
      tree.heading("Name", text="Name")
      tree.heading("ID", text="ID")
      tree.heading("Courses", text="Courses")
      tree.heading("Major", text="Major")
        
      for student_id, student_data in self.students.items():
         courses = ", ".join(student_data.get("courses", []))
         tree.insert("", "end", values=(student_data["name"], student_id, courses, student_data.get("major","N/A")))
      tree.pack(pady=20)
      self.create_button("Back to Admin Dashboard", self.navigate_back).pack()
      self.navigation_stack.push("enrolled_students_page")
    
    def schedule_page(self):
        """
        Creates the schedule management page.
        """
        self.clear_window()
        major_combo = self.create_combobox_with_label("Select Major:", self.get_major_names())
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        schedule_frame = ttk.Frame(self.root)
        schedule_frame.pack(pady=20)
        self.schedule_entries = {}
        for i, day in enumerate(days):
           self.create_label(f"{day}:").grid(row=i, column=0, padx=5, pady=5, sticky="e", in_=schedule_frame)
           course_combo = ttk.Combobox(schedule_frame, values=[], style="TCombobox")
           course_combo.grid(row=i, column=1, padx=5, pady=5, sticky="w")
           time_entry = self.create_entry()
           time_entry.grid(row=i, column=2, padx=5, pady=5, sticky="w",in_=schedule_frame)
           self.schedule_entries[day] = {"course": course_combo, "time": time_entry}
        
        # update available course once major selected
        major_combo.bind("<<ComboboxSelected>>", lambda event: self.update_major_courses(major_combo.get()))
        self.create_button("Submit Schedule", lambda: self.submit_schedule(major_combo.get())).pack(pady=10)
        self.create_button("Back to Admin Dashboard", self.navigate_back).pack()
        self.navigation_stack.push("schedule_page")

    def update_major_courses(self,selected_major):
        """
        Updates course comboboxes based on the selected major.
        
        Args:
           selected_major: The major selected in the combobox.
        """
        if selected_major:
             courses = self.get_course_list(selected_major)
             for day, entry_dict in self.schedule_entries.items():
               course_combo = entry_dict["course"]
               course_combo["values"] = courses

    def submit_schedule(self, major):
        """
        Submits the schedule for a given major.

        Args:
            major: The selected major from the combobox
        """
        if major:
            schedule_data = {}
            for day, entry_dict in self.schedule_entries.items():
               course_combo = entry_dict["course"]
               time_slot = entry_dict["time"].get()
               selected_courses =  course_combo.get()

               if selected_courses and time_slot:
                    schedule_data[day] = {
                        "courses": selected_courses,
                        "time": time_slot
                     }
               else:
                    schedule_data[day] = {
                        "courses": [],
                        "time":""
                   }
            self.schedules[major] = schedule_data
            self.save_data()
            messagebox.showinfo("Success", "Schedule updated successfully for the selected major")
        else:
            messagebox.showerror("Error", "Invalid Major Selected.")

    def admin_feedback_page(self):
        """
        Creates the page for viewing student feedback.
        """
        self.clear_window()
        text_area = tk.Text(self.root, height=10, width=60)
        text_area.pack(pady=20)

        if not self.student_feedback.is_empty():
           while not self.student_feedback.is_empty():
              feedback = self.student_feedback.dequeue()
              text_area.insert(tk.END, f"Student ID: {feedback.split(':')[0]}\nFeedback: {feedback.split(':')[1]}\n\n")
        else:
           text_area.insert(tk.END,"No feedback submitted by students yet.\n")
        text_area.config(state="disabled")
        self.create_button("Back to Admin Dashboard", self.navigate_back).pack()
        self.navigation_stack.push("admin_feedback_page")

    def student_login_page(self):
         """
         Creates the student login page.
         """
         self.clear_window()
         id_entry = self.create_entry_with_label("Student ID:")
         password_entry = self.create_entry_with_label("Password:",show="*")
         self.create_button("Login", lambda: self.student_login(id_entry.get(), password_entry.get())).pack(pady=10)
         self.create_button("Back", self.navigate_back).pack(pady=10)
         self.navigation_stack.push("student_login_page")

    def student_login(self, student_id, password):
         """
         Handles student login logic.

         Args:
             student_id: The student ID entered.
             password: The password entered.
         """
         if student_id in self.students and self.verify_password(self.students[student_id]["password"], password):
            self.current_user = student_id
            self.create_student_dashboard()
         else:
            messagebox.showerror("Login Failed", "Invalid student ID or password")

    def create_student_dashboard(self):
         """
         Creates the student dashboard.
         """
         self.clear_window()
         self.create_student_menu()
         self.create_label("Student Dashboard", self.title_font).pack(pady=20)
         self.create_label("Welcome Student!", font=("Arial", 16), color="#007BFF").pack(pady=20)
         self.create_label("Use the 'Student' menu to access your data.", font=("Arial", 10), color=self.text_color).pack(pady=10)
         self.navigation_stack.push("student_dashboard")
       
    def create_student_menu(self):
        """
        Creates the student menu bar.
        """
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        student_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Student", menu=student_menu)

        student_menu.add_command(label="Profile", command=self.student_profile_page)
        student_menu.add_command(label="Courses", command=self.student_courses_page)
        student_menu.add_command(label="Grades", command=self.student_grades_page)
        student_menu.add_command(label="Schedule", command=self.student_schedule_page)
        student_menu.add_command(label="Student Feedback", command=self.student_feedback_page)
        student_menu.add_separator()
        student_menu.add_command(label="Logout", command=self.logout)
    
    def student_profile_page(self):
        """
        Creates the student profile page.
        """
        self.clear_window()
        student_data = self.students.get(self.current_user)
        if student_data:
            self.create_label(f"Name: {student_data['name']}").pack()
            self.create_label(f"Student ID: {self.current_user}").pack()
            self.create_label(f"Year: {student_data['year']}").pack()
            self.create_label(f"Major: {student_data['major']}").pack()
            self.create_button("Change Password", self.change_password_page).pack(pady=20)
        else:
           messagebox.showerror("Error", "Student data not found.")
        self.create_button("Back to Student Dashboard", self.navigate_back).pack()
        self.navigation_stack.push("student_profile_page")
    
    def change_password_page(self):
        """
        Creates the change password page.
        """
        self.clear_window()
        old_password_entry = self.create_entry_with_label("Old Password:", show="*")
        new_password_entry = self.create_entry_with_label("New Password:", show="*")
        self.create_button("Change Password", lambda: self.change_password(old_password_entry.get(), new_password_entry.get())).pack(pady=10)
        self.create_button("Back to Profile", self.navigate_back).pack(pady=10)
        self.navigation_stack.push("change_password_page")
    
    def change_password(self, old_password, new_password):
         """
         Handles the change password logic.

         Args:
            old_password: The old password entered.
            new_password: The new password entered.
         """
         student_id = self.current_user
         if self.verify_password(self.students[student_id]["password"], old_password):
            hashed_new_password = self.hash_password(new_password)
            self.students[student_id]["password"] = hashed_new_password
            self.save_data()
            messagebox.showinfo("Success", "Password changed successfully")
            self.student_profile_page()
         else:
            messagebox.showerror("Error", "Invalid old password.")
    
    def student_courses_page(self):
         """
         Creates the student courses page.
         """
         self.clear_window()
         student_id = self.current_user
         available_courses = self.get_course_list(self.students[student_id].get("major",[]))
         course_combo = self.create_combobox_with_label("Available Courses:",available_courses)
         self.create_button("Enroll in Course", lambda: self.enroll_course(course_combo.get())).pack(pady=10)
         
         tree = ttk.Treeview(self.root, columns=("Courses"), show="headings")
         tree.heading("Courses", text="Courses")
         for course in self.students[self.current_user].get("courses",[]):
            tree.insert("", "end", values=(course,))
         tree.pack(pady=20)
         self.create_button("Back to Student Dashboard", self.navigate_back).pack()
         self.navigation_stack.push("student_courses_page")

    def enroll_course(self, course):
        """
        Enrolls a student in a course.

        Args:
           course: The course the student wants to enroll in
        """
        if course:
           if course not in self.students[self.current_user].get("courses",[]):
                self.students[self.current_user].get("courses",[]).append(course)
                self.save_data()
                messagebox.showinfo("Success", f"Enrolled in '{course}' successfully.")
           else:
                messagebox.showinfo("Info", "You have already enrolled in this course.")
        else:
            messagebox.showerror("Error", "Please select a course.")
        self.student_courses_page()

    def student_grades_page(self):
        """
        Creates the student grades page.
        """
        self.clear_window()
        student_id = self.current_user
        if student_id in self.grades:
            tree = ttk.Treeview(self.root, columns=("Course","Grade", "Result"), show="headings")
            tree.heading("Course", text="Course")
            tree.heading("Grade", text="Grade")
            tree.heading("Result", text="Result")

            for course, grade in self.grades[student_id].items():
                 result = "Pass" if grade not in ["D-","F"] else "Fail"
                 tree.insert("", "end", values=(course, grade, result))
            tree.pack(pady=20)
        else:
             self.create_label(f"You don't have grades yet").pack(pady=20)
        self.create_button("Back to Student Dashboard", self.navigate_back).pack()
        self.navigation_stack.push("student_grades_page")
    
    def student_schedule_page(self):
         """
         Creates the student schedule page.
         """
         self.clear_window()
         student_id = self.current_user
         student_major = self.students[student_id].get("major")
         
         if student_major and student_major in self.schedules:
            schedule_frame = ttk.Frame(self.root)
            schedule_frame.pack(pady=20)
             
            for i , (day, schedule_data) in enumerate(self.schedules[student_major].items()):
                self.create_label(f"{day}:").grid(row=i, column=0, padx=5, pady=5, sticky="e", in_=schedule_frame)
                student_courses = [course for course in schedule_data.get("courses",[]) if course in self.students[student_id].get("courses",[])]
                self.create_label(", ".join(student_courses)).grid(row=i, column=1, padx=5, pady=5, sticky="w", in_=schedule_frame)
                self.create_label(f"Time : {schedule_data.get('time','')}").grid(row=i, column=2, padx=5, pady=5, sticky="w", in_=schedule_frame)
         else:
             self.create_label(f"No Schedule Set Yet").pack(pady=20)
         self.create_button("Back to Student Dashboard", self.navigate_back).pack()
         self.navigation_stack.push("student_schedule_page")
    
    def student_feedback_page(self):
         """
         Creates the student feedback page.
         """
         self.clear_window()
         self.create_label("Enter Your Feedback:").pack()
         feedback_entry = tk.Text(self.root, height=5, width=50)
         feedback_entry.pack()
         self.create_button("Submit Feedback", lambda: self.submit_feedback(feedback_entry.get("1.0", "end-1c"))).pack(pady=20)
         self.create_button("Back to Student Dashboard", self.navigate_back).pack()
         self.navigation_stack.push("student_feedback_page")

    def submit_feedback(self, feedback):
        """
        Submits feedback from the student.

        Args:
            feedback: The feedback entered by the student.
        """
        student_id = self.current_user
        self.student_feedback.enqueue(f"{student_id}:{feedback}")
        self.save_data()
        
        messagebox.showinfo("Success", "Feedback submitted successfully")
    
    def logout(self):
        """
        Logs the current user out.
        """
        self.current_user = None
        self.create_login_page()
        messagebox.showinfo("Logged Out", "You have been logged out.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolManagementSystem(root)
    root.mainloop()