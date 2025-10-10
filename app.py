import csv
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


APP_TITLE = "TutorRen Management"
DATA_DIR = Path(__file__).resolve().parent / "data"


DATA_SPECS = {
    "users": {"filename": "users.csv", "headers": ["username", "password", "role"], "unique": "username"},
    "tutors": {"filename": "tutors.csv", "headers": ["id", "name", "email", "subjects"], "unique": "id"},
    "students": {"filename": "students.csv", "headers": ["id", "name", "email", "year"], "unique": "id"},
    "classes": {"filename": "classes.csv", "headers": ["id", "title", "tutor_id", "student_id", "schedule"], "unique": "id"},
}


for spec in DATA_SPECS.values():
    path = DATA_DIR / spec["filename"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(spec["headers"])


def load_records(name):
    spec = DATA_SPECS[name]
    path = DATA_DIR / spec["filename"]
    with path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def append_record(name, record):
    spec = DATA_SPECS[name]
    path = DATA_DIR / spec["filename"]
    headers = spec["headers"]
    unique_field = spec.get("unique")
    if unique_field:
        existing = load_records(name)
        if any(row.get(unique_field) == record.get(unique_field) for row in existing):
            raise ValueError(f"{unique_field.title()} already exists.")
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writerow(record)


def replace_records(name, rows):
    spec = DATA_SPECS[name]
    path = DATA_DIR / spec["filename"]
    headers = spec["headers"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def generate_id(prefix, records):
    max_value = 0
    for row in records:
        identifier = row.get("id", "")
        if identifier.startswith(prefix + "-"):
            try:
                max_value = max(max_value, int(identifier.split("-", 1)[1]))
            except ValueError:
                continue
    return f"{prefix}-{max_value + 1:03d}"


class LoginFrame(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, padding=40)
        self.on_success = on_success
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="TutorRen Management", font=("Helvetica", 20, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 30)
        )

        ttk.Label(self, text="Username:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.username_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.username_var).grid(row=1, column=1, sticky=tk.EW)

        ttk.Label(self, text="Password:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.password_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.password_var, show="*").grid(
            row=2, column=1, sticky=tk.EW, pady=(10, 0)
        )

        login_btn = ttk.Button(self, text="Login", command=self.attempt_login)
        login_btn.grid(row=3, column=0, columnspan=2, pady=(25, 0), sticky=tk.EW)

        self.bind_all("<Return>", lambda _event: self.attempt_login())

    def attempt_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("Missing information", "Please enter both username and password.")
            return
        users = load_records("users")
        for user in users:
            if user["username"] == username and user["password"] == password:
                self.on_success(user)
                return
        messagebox.showerror("Login failed", "Invalid username or password.")


class Dashboard(ttk.Frame):
    def __init__(self, master, current_user):
        super().__init__(master)
        self.current_user = current_user
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.master.title(f"{APP_TITLE} — {self.current_user['username']}")
        self.master.geometry("960x640")

        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        navigation_menu = tk.Menu(self.menu_bar, tearoff=0)
        navigation_menu.add_command(label="Dashboard", command=lambda: self.show_view("dashboard"))
        navigation_menu.add_separator()
        navigation_menu.add_command(label="Tutors", command=lambda: self.show_view("tutors"))
        navigation_menu.add_command(label="Students", command=lambda: self.show_view("students"))
        navigation_menu.add_command(label="Classes", command=lambda: self.show_view("classes"))
        self.menu_bar.add_cascade(label="Navigate", menu=navigation_menu)

        account_menu = tk.Menu(self.menu_bar, tearoff=0)
        account_menu.add_command(label="Logout", command=self.logout)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)

        header = ttk.Frame(self, padding=20)
        header.pack(fill=tk.X)
        ttk.Label(
            header,
            text=f"Welcome, {self.current_user['username']} ({self.current_user['role']})",
            font=("Helvetica", 16, "bold"),
        ).pack(side=tk.LEFT)

        self.content = ttk.Frame(self)
        self.content.pack(fill=tk.BOTH, expand=True)

        self.views = {
            "dashboard": DashboardView(self.content),
            "tutors": TutorsView(self.content, self.current_user),
            "students": StudentsView(self.content, self.current_user),
            "classes": ClassesView(self.content, self.current_user),
        }
        self.show_view("dashboard")

    def show_view(self, name):
        for view_name, frame in self.views.items():
            if view_name == name:
                frame.tkraise()
                frame.refresh()
            else:
                frame.lower()

    def logout(self):
        self.master.menu = None
        self.master.config(menu=None)
        self.destroy()
        self.master.show_login()


class DashboardView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=30)
        self.grid(row=0, column=0, sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        ttk.Label(self, text="Dashboard", font=("Helvetica", 18, "bold")).pack(anchor=tk.W)
        ttk.Label(
            self,
            text="Use the Navigate menu to manage tutors, students, and classes. This overview summarizes current records.",
            wraplength=600,
        ).pack(anchor=tk.W, pady=(10, 30))

        self.stats = ttk.Treeview(self, columns=("type", "count"), show="headings", height=5)
        self.stats.heading("type", text="Data Type")
        self.stats.heading("count", text="Count")
        self.stats.column("type", width=200)
        self.stats.column("count", width=80, anchor=tk.CENTER)
        self.stats.pack(fill=tk.X)
        self.refresh()

    def refresh(self):
        for row in self.stats.get_children():
            self.stats.delete(row)
        for dataset in ("tutors", "students", "classes"):
            records = load_records(dataset)
            self.stats.insert("", tk.END, values=(dataset.title(), len(records)))


class DataListView(ttk.Frame):
    columns: tuple[str, ...] = ()
    dataset: str = ""
    add_fields: tuple[tuple[str, str], ...] = ()

    def __init__(self, master, current_user):
        super().__init__(master, padding=20)
        self.current_user = current_user
        self.grid(row=0, column=0, sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text=self.dataset.title(), font=("Helvetica", 18, "bold"))
        title.pack(anchor=tk.W)

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=12)
        for col, label in zip(self.columns, self.columns):
            self.tree.heading(col, text=label.replace("_", " ").title())
            self.tree.column(col, anchor=tk.W, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=(15, 10))

        form = ttk.LabelFrame(self, text=f"Add {self.dataset[:-1].title()}")
        form.pack(fill=tk.X, pady=(10, 0))

        self.form_vars = {}
        for idx, (field, label) in enumerate(self.add_fields):
            ttk.Label(form, text=label).grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)
            var = tk.StringVar()
            entry = ttk.Entry(form, textvariable=var, width=40)
            entry.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=5)
            self.form_vars[field] = var

        add_button = ttk.Button(form, text=f"Add {self.dataset[:-1].title()}", command=self.add_record)
        add_button.grid(row=len(self.add_fields), column=0, columnspan=2, pady=10)

        if self.dataset == "classes":
            # Placeholders for combobox attributes populated in subclass implementation
            self.tutor_combo = None
            self.student_combo = None

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for record in load_records(self.dataset):
            values = [record.get(col, "") for col in self.columns]
            self.tree.insert("", tk.END, values=values)
        if self.dataset == "classes" and self.tutor_combo and self.student_combo:
            tutors = load_records("tutors")
            students = load_records("students")
            tutor_options = [f"{row['id']} — {row['name']}" for row in tutors]
            student_options = [f"{row['id']} — {row['name']}" for row in students]
            self.tutor_combo.configure(values=tutor_options)
            self.student_combo.configure(values=student_options)

    def add_record(self):
        raise NotImplementedError


class TutorsView(DataListView):
    columns = ("id", "name", "email", "subjects")
    dataset = "tutors"
    add_fields = (("name", "Name"), ("email", "Email"), ("subjects", "Subjects (comma separated)"))

    def add_record(self):
        name = self.form_vars["name"].get().strip()
        email = self.form_vars["email"].get().strip()
        subjects = self.form_vars["subjects"].get().strip()
        if not name or not email:
            messagebox.showwarning("Missing data", "Name and email are required.")
            return
        records = load_records("tutors")
        new_id = generate_id("T", records)
        record = {"id": new_id, "name": name, "email": email, "subjects": subjects.replace(",", ";")}
        append_record("tutors", record)
        self.refresh()
        for var in self.form_vars.values():
            var.set("")


class StudentsView(DataListView):
    columns = ("id", "name", "email", "year")
    dataset = "students"
    add_fields = (("name", "Name"), ("email", "Email"), ("year", "Year Level"))

    def add_record(self):
        name = self.form_vars["name"].get().strip()
        email = self.form_vars["email"].get().strip()
        year = self.form_vars["year"].get().strip()
        if not name or not email or not year:
            messagebox.showwarning("Missing data", "All fields are required.")
            return
        records = load_records("students")
        new_id = generate_id("S", records)
        record = {"id": new_id, "name": name, "email": email, "year": year}
        append_record("students", record)
        self.refresh()
        for var in self.form_vars.values():
            var.set("")


class ClassesView(DataListView):
    columns = ("id", "title", "tutor_id", "student_id", "schedule")
    dataset = "classes"
    add_fields = (("title", "Class Title"), ("schedule", "Schedule (e.g. Mon 10:00)"))

    def create_widgets(self):
        super().create_widgets()
        form = next(child for child in self.winfo_children() if isinstance(child, ttk.LabelFrame))
        start_row = len(self.add_fields)

        ttk.Label(form, text="Tutor").grid(row=start_row, column=0, sticky=tk.W, padx=5, pady=5)
        self.tutor_combo = ttk.Combobox(form, state="readonly", width=38)
        self.tutor_combo.grid(row=start_row, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(form, text="Student").grid(row=start_row + 1, column=0, sticky=tk.W, padx=5, pady=5)
        self.student_combo = ttk.Combobox(form, state="readonly", width=38)
        self.student_combo.grid(row=start_row + 1, column=1, sticky=tk.W, padx=5, pady=5)

        add_button = next(child for child in form.winfo_children() if isinstance(child, ttk.Button))
        add_button.grid_configure(row=start_row + 2)

    def add_record(self):
        title = self.form_vars["title"].get().strip()
        schedule = self.form_vars["schedule"].get().strip()
        tutor_value = self.tutor_combo.get()
        student_value = self.student_combo.get()

        if not title or not schedule or not tutor_value or not student_value:
            messagebox.showwarning("Missing data", "Please complete all fields.")
            return

        tutor_id = tutor_value.split(" — ")[0]
        student_id = student_value.split(" — ")[0]

        classes = load_records("classes")
        new_id = generate_id("C", classes)
        record = {
            "id": new_id,
            "title": title,
            "tutor_id": tutor_id,
            "student_id": student_id,
            "schedule": schedule,
        }
        append_record("classes", record)
        self.refresh()
        for var in self.form_vars.values():
            var.set("")
        self.tutor_combo.set("")
        self.student_combo.set("")


class TutorRenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("520x360")
        self.resizable(False, False)
        self.current_user = None
        self.show_login()

    def show_login(self):
        self.current_user = None
        for child in self.winfo_children():
            child.destroy()
        login = LoginFrame(self, self.on_login_success)
        login.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, user):
        self.current_user = user
        for child in self.winfo_children():
            child.destroy()
        self.resizable(True, True)
        Dashboard(self, self.current_user)


if __name__ == "__main__":
    app = TutorRenApp()
    app.mainloop()
