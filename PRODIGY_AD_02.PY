import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as sql

class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Database setup
        self.connection = sql.connect('listOfTasks.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('create table if not exists tasks (title text)')
        
        self.tasks = []
        self.retrieve_database()
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Header frame
        header_frame = tk.Frame(self.root, bg="#4a7a8c")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        header_label = tk.Label(
            header_frame,
            text="To-Do List",
            font=("Helvetica", 24, "bold"),
            bg="#4a7a8c",
            fg="white"
        )
        header_label.pack(pady=10)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Left panel (input and buttons)
        left_panel = tk.Frame(main_frame, bg="#f0f0f0")
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        
        # Task entry
        task_label = tk.Label(
            left_panel,
            text="New Task:",
            font=("Helvetica", 11),
            bg="#f0f0f0"
        )
        task_label.pack(anchor="w", pady=(0, 5))
        
        self.task_field = ttk.Entry(
            left_panel,
            font=("Helvetica", 12),
            width=25
        )
        self.task_field.pack(pady=(0, 15))
        self.task_field.bind("<Return>", lambda e: self.add_task())
        
        # Buttons
        button_style = ttk.Style()
        button_style.configure("TButton", font=("Helvetica", 10), padding=6)
        
        add_button = ttk.Button(
            left_panel,
            text="Add Task",
            command=self.add_task
        )
        add_button.pack(fill="x", pady=5)
        
        del_button = ttk.Button(
            left_panel,
            text="Delete Selected",
            command=self.delete_task
        )
        del_button.pack(fill="x", pady=5)
        
        clear_button = ttk.Button(
            left_panel,
            text="Clear All",
            command=self.delete_all_tasks
        )
        clear_button.pack(fill="x", pady=5)
        
        exit_button = ttk.Button(
            left_panel,
            text="Exit",
            command=self.close
        )
        exit_button.pack(fill="x", pady=5)
        
        # Right panel (task list)
        right_panel = tk.Frame(main_frame, bg="#ffffff", relief="solid", borderwidth=1)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Task list with scrollbar
        scrollbar = ttk.Scrollbar(right_panel)
        scrollbar.pack(side="right", fill="y")
        
        self.task_listbox = tk.Listbox(
            right_panel,
            font=("Helvetica", 12),
            selectmode="SINGLE",
            yscrollcommand=scrollbar.set,
            bg="white",
            fg="#333333",
            selectbackground="#4a7a8c",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0
        )
        self.task_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Update the list with tasks from database
        self.list_update()
    
    def add_task(self):
        task_string = self.task_field.get().strip()
        if not task_string:
            messagebox.showinfo('Error', 'Field is Empty.')
        else:
            self.tasks.append(task_string)
            self.cursor.execute('insert into tasks values (?)', (task_string,))
            self.list_update()
            self.task_field.delete(0, 'end')
    
    def list_update(self):
        self.clear_list()
        for task in self.tasks:
            self.task_listbox.insert('end', task)
    
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            the_value = self.task_listbox.get(selected_index)
            if the_value in self.tasks:
                self.tasks.remove(the_value)
                self.cursor.execute('delete from tasks where title = ?', (the_value,))
                self.list_update()
        except IndexError:
            messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')
    
    def delete_all_tasks(self):
        if messagebox.askyesno('Delete All', 'Are you sure you want to delete all tasks?'):
            self.tasks.clear()
            self.cursor.execute('delete from tasks')
            self.list_update()
    
    def clear_list(self):
        self.task_listbox.delete(0, 'end')
    
    def retrieve_database(self):
        self.tasks.clear()
        for row in self.cursor.execute('select title from tasks'):
            self.tasks.append(row[0])
    
    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()