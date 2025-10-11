import csv
import datetime as dt
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


APP_TITLE = "TutorRen Management"
DATA_DIR = Path(__file__).resolve().parent / "data"
EXPORT_DIR = DATA_DIR / "exports"

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
TIME_SLOTS = [f"{hour:02d}:00" for hour in range(8, 21)]


class ThemePalette:
    BACKGROUND = "#0f172a"
    SURFACE = "#18263c"
    SURFACE_ALT = "#1f304d"
    PRIMARY = "#6366f1"
    PRIMARY_ACTIVE = "#4f46e5"
    ACCENT = "#22d3ee"
    TEXT = "#e2e8f0"
    MUTED_TEXT = "#94a3b8"
    BORDER = "#1f2737"
    CARD_BORDER = "#223147"
    SLOT_AVAILABLE_BG = "#134e4a"
    SLOT_AVAILABLE_FG = "#a7f3d0"
    SLOT_TAKEN_BG = "#4c1d95"
    SLOT_TAKEN_FG = "#ede9fe"


def init_theme(app: tk.Tk) -> None:
    style = ttk.Style(app)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    app.configure(bg=ThemePalette.BACKGROUND)

    base_font = ("Segoe UI", 11)
    style.configure(".", font=base_font)

    style.configure("TFrame", background=ThemePalette.BACKGROUND)
    style.configure("Background.TFrame", background=ThemePalette.BACKGROUND)
    style.configure(
        "Card.TFrame",
        background=ThemePalette.SURFACE,
        borderwidth=0,
        relief="flat",
    )
    style.configure("Hero.TFrame", background=ThemePalette.PRIMARY)

    style.configure("TLabel", background=ThemePalette.BACKGROUND, foreground=ThemePalette.TEXT)
    style.configure(
        "Card.TLabel",
        background=ThemePalette.SURFACE,
        foreground=ThemePalette.TEXT,
    )
    style.configure(
        "SectionTitle.TLabel",
        background=ThemePalette.BACKGROUND,
        foreground=ThemePalette.TEXT,
        font=("Segoe UI", 20, "bold"),
    )
    style.configure(
        "CardTitle.TLabel",
        background=ThemePalette.SURFACE,
        foreground=ThemePalette.TEXT,
        font=("Segoe UI", 16, "bold"),
    )
    style.configure(
        "HeroTitle.TLabel",
        background=ThemePalette.PRIMARY,
        foreground="#ffffff",
        font=("Segoe UI", 22, "bold"),
    )
    style.configure(
        "HeroSubtitle.TLabel",
        background=ThemePalette.PRIMARY,
        foreground="#e0e7ff",
    )
    style.configure(
        "Badge.TLabel",
        background=ThemePalette.ACCENT,
        foreground=ThemePalette.BACKGROUND,
        font=("Segoe UI", 10, "bold"),
        padding=(12, 4),
    )
    style.configure(
        "Muted.TLabel",
        background=ThemePalette.BACKGROUND,
        foreground=ThemePalette.MUTED_TEXT,
    )

    style.configure(
        "Accent.TButton",
        background=ThemePalette.PRIMARY,
        foreground="#ffffff",
        padding=(18, 10),
        borderwidth=0,
        focusthickness=1,
        focuscolor=ThemePalette.PRIMARY,
    )
    style.map(
        "Accent.TButton",
        background=[("active", ThemePalette.PRIMARY_ACTIVE), ("pressed", ThemePalette.PRIMARY_ACTIVE)],
        foreground=[("disabled", ThemePalette.MUTED_TEXT)],
    )
    style.configure(
        "TButton",
        padding=(16, 9),
        background=ThemePalette.SURFACE_ALT,
        foreground=ThemePalette.TEXT,
        borderwidth=0,
    )
    style.map(
        "TButton",
        background=[("active", ThemePalette.PRIMARY_ACTIVE)],
        foreground=[("disabled", ThemePalette.MUTED_TEXT)],
    )

    entry_settings = {
        "fieldbackground": ThemePalette.SURFACE_ALT,
        "foreground": ThemePalette.TEXT,
        "background": ThemePalette.SURFACE_ALT,
        "bordercolor": ThemePalette.CARD_BORDER,
        "lightcolor": ThemePalette.PRIMARY,
        "darkcolor": ThemePalette.CARD_BORDER,
        "insertcolor": ThemePalette.TEXT,
    }
    style.configure("TEntry", **entry_settings)
    style.map("TEntry", fieldbackground=[("focus", ThemePalette.SURFACE_ALT)])
    style.configure("TCombobox", **entry_settings)
    style.map("TCombobox", fieldbackground=[("readonly", ThemePalette.SURFACE_ALT)])

    style.configure(
        "Card.TLabelframe",
        background=ThemePalette.SURFACE,
        foreground=ThemePalette.TEXT,
        borderwidth=1,
        relief="solid",
        bordercolor=ThemePalette.CARD_BORDER,
    )
    style.configure(
        "Card.TLabelframe.Label",
        background=ThemePalette.SURFACE,
        foreground=ThemePalette.MUTED_TEXT,
        font=("Segoe UI", 11, "bold"),
    )

    style.configure(
        "Data.Treeview",
        background=ThemePalette.SURFACE,
        fieldbackground=ThemePalette.SURFACE,
        foreground=ThemePalette.TEXT,
        rowheight=28,
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "Data.Treeview",
        background=[("selected", ThemePalette.PRIMARY)],
        foreground=[("selected", "#ffffff")],
    )
    style.configure(
        "Data.Treeview.Heading",
        background=ThemePalette.SURFACE_ALT,
        foreground=ThemePalette.TEXT,
        relief="flat",
        padding=(8, 6),
        font=("Segoe UI", 11, "bold"),
    )
    style.map("Data.Treeview.Heading", background=[("active", ThemePalette.SURFACE_ALT)])

    style.configure(
        "Horizontal.TSeparator",
        background=ThemePalette.BORDER,
    )

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


def ensure_directories():
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


ensure_directories()


def is_valid_email(value: str) -> bool:
    value = value.strip()
    if "@" not in value:
        return False
    if value.count("@") != 1:
        return False
    local, domain = value.split("@", 1)
    if not local or not domain or "." not in domain:
        return False
    return True


def escape_pdf_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


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


def schedule_sort_key(schedule: str) -> tuple[int, int, int]:
    day, _, time = schedule.partition(" ")
    try:
        day_index = DAYS.index(day)
    except ValueError:
        day_index = len(DAYS)
    hour, minute = 0, 0
    if ":" in time:
        try:
            hour, minute = map(int, time.split(":", 1))
        except ValueError:
            pass
    return (day_index, hour, minute)


class LoginFrame(ttk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, style="Background.TFrame")
        self.on_success = on_success
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        hero = ttk.Frame(self, style="Hero.TFrame", padding=48)
        hero.grid(row=0, column=0, sticky="nsew")
        hero.columnconfigure(0, weight=1)
        ttk.Label(hero, text="TutorRen", style="HeroTitle.TLabel").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(
            hero,
            text="Effortlessly orchestrate tutors, students, and schedules.",
            style="HeroSubtitle.TLabel",
            wraplength=260,
        ).grid(row=1, column=0, sticky=tk.W, pady=(12, 0))
        ttk.Label(hero, text="Spot upcoming sessions at a glance.", style="HeroSubtitle.TLabel").grid(
            row=2, column=0, sticky=tk.W, pady=(24, 0)
        )
        ttk.Label(hero, text="CSV backups you can trust", style="Badge.TLabel").grid(
            row=3, column=0, sticky=tk.W, pady=(40, 0)
        )

        card = ttk.Frame(self, style="Card.TFrame", padding=40)
        card.grid(row=0, column=1, sticky="nsew", padx=60, pady=60)
        card.columnconfigure(0, weight=1)

        ttk.Label(card, text="Sign in", style="CardTitle.TLabel").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(
            card,
            text="Enter your credentials to access TutorRen.",
            style="Card.TLabel",
        ).grid(row=1, column=0, sticky=tk.W, pady=(6, 18))

        ttk.Label(card, text="Username", style="Card.TLabel").grid(row=2, column=0, sticky=tk.W)
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(card, textvariable=self.username_var)
        username_entry.grid(row=3, column=0, sticky=tk.EW, pady=(6, 16))

        ttk.Label(card, text="Password", style="Card.TLabel").grid(row=4, column=0, sticky=tk.W)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(card, textvariable=self.password_var, show="*")
        password_entry.grid(row=5, column=0, sticky=tk.EW, pady=(6, 24))

        login_btn = ttk.Button(card, text="Sign in", style="Accent.TButton", command=self.attempt_login)
        login_btn.grid(row=6, column=0, sticky=tk.EW)

        ttk.Label(
            card,
            text="Managers can create accounts once inside the app.",
            style="Card.TLabel",
        ).grid(row=7, column=0, sticky=tk.W, pady=(20, 0))

        self._return_binding = None
        self._return_binding = self.master.bind("<Return>", lambda _event: self.attempt_login())
        username_entry.focus_set()

    def destroy(self):
        if self._return_binding:
            self.master.unbind("<Return>")
        super().destroy()

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
        super().__init__(master, style="Background.TFrame")
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
        if self.current_user.get("role") == "Manager":
            navigation_menu.add_command(label="Users", command=lambda: self.show_view("users"))
        navigation_menu.add_command(label="Tutors", command=lambda: self.show_view("tutors"))
        navigation_menu.add_command(label="Students", command=lambda: self.show_view("students"))
        navigation_menu.add_command(label="Classes", command=lambda: self.show_view("classes"))
        self.menu_bar.add_cascade(label="Navigate", menu=navigation_menu)

        account_menu = tk.Menu(self.menu_bar, tearoff=0)
        account_menu.add_command(label="Logout", command=self.logout)
        self.menu_bar.add_cascade(label="Account", menu=account_menu)

        header = ttk.Frame(self, style="Hero.TFrame", padding=(28, 18))
        header.pack(fill=tk.X)
        ttk.Label(
            header,
            text=f"Welcome back, {self.current_user['username']}",
            style="HeroTitle.TLabel",
        ).pack(anchor=tk.W)
        ttk.Label(
            header,
            text=f"You are signed in as {self.current_user['role']}. Manage your schedules below.",
            style="HeroSubtitle.TLabel",
        ).pack(anchor=tk.W, pady=(6, 0))

        self.content = ttk.Frame(self, style="Background.TFrame")
        self.content.pack(fill=tk.BOTH, expand=True)

        self.views = {
            "dashboard": DashboardView(self.content, self.current_user),
            "tutors": TutorsView(self.content, self.current_user),
            "students": StudentsView(self.content, self.current_user),
            "classes": ClassesView(self.content, self.current_user),
        }
        if self.current_user.get("role") == "Manager":
            self.views["users"] = UsersView(self.content, self.current_user)
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
    def __init__(self, master, current_user):
        super().__init__(master, padding=30, style="Background.TFrame")
        self.current_user = current_user
        self.grid(row=0, column=0, sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        ttk.Label(self, text="Dashboard", style="SectionTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(
            self,
            text="Access quick actions and high-level statistics for your tutoring center.",
            style="Muted.TLabel",
            wraplength=640,
        ).pack(anchor=tk.W, pady=(8, 26))

        controls = ttk.Frame(self, style="Background.TFrame")
        controls.pack(anchor=tk.W, pady=(0, 24))
        ttk.Button(
            controls,
            text="Generate Weekly Schedule PDFs",
            style="Accent.TButton",
            command=self.generate_schedule_pdfs,
        ).grid(row=0, column=0, padx=(0, 12))
        ttk.Button(
            controls,
            text="View 3-Day Schedule Snapshot",
            command=self.show_three_day_schedule,
        ).grid(row=0, column=1)

        stats_card = ttk.Frame(self, style="Card.TFrame", padding=20)
        stats_card.pack(fill=tk.X)
        ttk.Label(stats_card, text="At a glance", style="CardTitle.TLabel").pack(anchor=tk.W, pady=(0, 12))

        self.stats = ttk.Treeview(stats_card, columns=("type", "count"), show="headings", height=6, style="Data.Treeview")
        self.stats.heading("type", text="Data Type")
        self.stats.heading("count", text="Count")
        self.stats.column("type", width=240)
        self.stats.column("count", width=80, anchor=tk.CENTER)
        self.stats.pack(fill=tk.X)
        self.refresh()

    def refresh(self):
        for row in self.stats.get_children():
            self.stats.delete(row)
        for dataset in ("users", "tutors", "students", "classes"):
            if dataset == "users" and self.current_user.get("role") != "Manager":
                continue
            records = load_records(dataset)
            self.stats.insert("", tk.END, values=(dataset.title(), len(records)))

    def show_three_day_schedule(self):
        today = dt.date.today()
        classes = load_records("classes")
        tutors = {row["id"]: row for row in load_records("tutors")}
        students = {row["id"]: row for row in load_records("students")}

        lines: list[str] = []
        for offset in range(3):
            target_date = today + dt.timedelta(days=offset)
            label = target_date.strftime("%A (%b %d)")
            day_code = target_date.strftime("%a")
            lines.append(label + ":")
            day_classes = [
                lesson
                for lesson in classes
                if lesson.get("schedule", " ").split(" ")[0] == day_code
            ]
            if not day_classes:
                lines.append("  • No sessions scheduled")
                lines.append("")
                continue

            for lesson in sorted(day_classes, key=lambda item: schedule_sort_key(item.get("schedule", ""))):
                time = lesson.get("schedule", "").split(" ")[1] if " " in lesson.get("schedule", "") else ""
                tutor_name = tutors.get(lesson["tutor_id"], {}).get("name", lesson["tutor_id"])
                student_name = students.get(lesson["student_id"], {}).get("name", lesson["student_id"])
                title = lesson.get("title", "Lesson")
                lines.append(f"  • {time} — {title} (Tutor: {tutor_name}, Student: {student_name})")
            lines.append("")

        message = "\n".join(lines).strip()
        messagebox.showinfo("Upcoming Sessions", message or "No sessions scheduled in the next three days.")

    def generate_schedule_pdfs(self):
        classes = load_records("classes")
        tutors = {row["id"]: row for row in load_records("tutors")}
        students = {row["id"]: row for row in load_records("students")}
        tutor_sections: dict[str, list[str]] = {}
        student_sections: dict[str, list[str]] = {}
        for lesson in sorted(classes, key=lambda item: schedule_sort_key(item.get("schedule", ""))):
            tutor = tutors.get(lesson["tutor_id"], {})
            student = students.get(lesson["student_id"], {})
            entry = f"{lesson['schedule']} — {lesson['title']} with {student.get('name', 'Unknown')}"
            tutor_label = f"Tutor: {tutor.get('name', lesson['tutor_id'])} ({lesson['tutor_id']})"
            tutor_sections.setdefault(tutor_label, []).append(entry)

            student_entry = f"{lesson['schedule']} — {lesson['title']} with {tutor.get('name', 'Unknown Tutor')}"
            student_label = f"Student: {student.get('name', lesson['student_id'])} ({lesson['student_id']})"
            student_sections.setdefault(student_label, []).append(student_entry)

        tutor_path = EXPORT_DIR / "tutor_schedule.pdf"
        student_path = EXPORT_DIR / "student_schedule.pdf"
        create_schedule_pdf(tutor_path, tutor_sections or {"Tutors": []})
        create_schedule_pdf(student_path, student_sections or {"Students": []})
        messagebox.showinfo(
            "Schedules exported",
            f"Tutor schedule: {tutor_path}\nStudent schedule: {student_path}",
        )


class DataListView(ttk.Frame):
    columns: tuple[str, ...] = ()
    dataset: str = ""
    add_fields: tuple[tuple[str, str], ...] = ()

    def __init__(self, master, current_user):
        super().__init__(master, padding=24, style="Background.TFrame")
        self.current_user = current_user
        self.grid(row=0, column=0, sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text=self.dataset.title(), style="SectionTitle.TLabel")
        title.pack(anchor=tk.W)

        list_card = ttk.Frame(self, style="Card.TFrame", padding=20)
        list_card.pack(fill=tk.BOTH, expand=True, pady=(18, 16))
        list_card.columnconfigure(0, weight=1)
        list_card.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(list_card, columns=self.columns, show="headings", style="Data.Treeview")
        for col, label in zip(self.columns, self.columns):
            self.tree.heading(col, text=label.replace("_", " ").title())
            self.tree.column(col, anchor=tk.W, width=150)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.tag_configure("even", background=ThemePalette.SURFACE)
        self.tree.tag_configure("odd", background=ThemePalette.SURFACE_ALT)

        tree_scroll = ttk.Scrollbar(list_card, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.form_frame = ttk.LabelFrame(
            self,
            text=f"Add {self.dataset[:-1].title()}",
            style="Card.TLabelframe",
            padding=20,
        )
        self.form_frame.pack(fill=tk.X, pady=(0, 16))

        self.form_vars = {}
        self.form_entries: dict[str, ttk.Entry] = {}
        for idx, (field, label) in enumerate(self.add_fields):
            ttk.Label(self.form_frame, text=label, style="Card.TLabel").grid(
                row=idx, column=0, sticky=tk.W, padx=5, pady=5
            )
            var = tk.StringVar()
            entry = ttk.Entry(self.form_frame, textvariable=var, width=40)
            entry.grid(row=idx, column=1, sticky=tk.W, padx=5, pady=5)
            self.form_vars[field] = var
            self.form_entries[field] = entry

        self.add_button = ttk.Button(
            self.form_frame,
            text=f"Add {self.dataset[:-1].title()}",
            style="Accent.TButton",
            command=self.add_record,
        )
        self.add_button.grid(row=len(self.add_fields), column=0, columnspan=2, pady=10)

        if self.dataset == "classes":
            # Placeholders for combobox attributes populated in subclass implementation
            self.tutor_combo = None
            self.student_combo = None

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, record in enumerate(load_records(self.dataset)):
            values = [record.get(col, "") for col in self.columns]
            tag = "even" if idx % 2 == 0 else "odd"
            self.tree.insert("", tk.END, values=values, tags=(tag,))
        if self.dataset == "classes" and self.tutor_combo and self.student_combo:
            tutors = load_records("tutors")
            students = load_records("students")
            tutor_options = [f"{row['id']} — {row['name']}" for row in tutors]
            student_options = [f"{row['id']} — {row['name']}" for row in students]
            self.tutor_combo.configure(values=tutor_options)
            self.student_combo.configure(values=student_options)

    def add_record(self):
        raise NotImplementedError


class UsersView(DataListView):
    columns = ("username", "role")
    dataset = "users"
    add_fields = (("username", "Username"), ("password", "Password"))
    role_options = ("Manager", "Tutor", "Employee")

    def create_widgets(self):
        super().create_widgets()
        if "password" in self.form_entries:
            self.form_entries["password"].configure(show="*")
        ttk.Label(self.form_frame, text="Role", style="Card.TLabel").grid(
            row=len(self.add_fields), column=0, sticky=tk.W, padx=5, pady=5
        )
        self.role_var = tk.StringVar(value=self.role_options[0])
        self.role_combo = ttk.Combobox(
            self.form_frame, state="readonly", values=self.role_options, textvariable=self.role_var, width=38
        )
        self.role_combo.grid(row=len(self.add_fields), column=1, sticky=tk.W, padx=5, pady=5)
        self.add_button.grid_configure(row=len(self.add_fields) + 1)
        if self.current_user.get("role") != "Manager":
            self.disable_form()

    def disable_form(self):
        for entry in self.form_entries.values():
            entry.configure(state="disabled")
        self.add_button.configure(state="disabled")
        self.role_combo.configure(state="disabled")

    def refresh(self):
        super().refresh()
        if self.current_user.get("role") != "Manager":
            self.disable_form()

    def add_record(self):
        if self.current_user.get("role") != "Manager":
            messagebox.showerror("Permission denied", "Only managers can create new users.")
            return
        username = self.form_vars["username"].get().strip()
        password = self.form_vars["password"].get().strip()
        role = self.role_var.get()
        if not username or not password:
            messagebox.showwarning("Missing data", "Username and password are required.")
            return
        record = {"username": username, "password": password, "role": role}
        try:
            append_record("users", record)
        except ValueError as exc:
            messagebox.showerror("Could not add user", str(exc))
            return
        self.refresh()
        for var in self.form_vars.values():
            var.set("")
        self.role_var.set(self.role_options[0])


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
        if not is_valid_email(email):
            messagebox.showerror("Invalid email", "Please enter a valid email address.")
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
        if not is_valid_email(email):
            messagebox.showerror("Invalid email", "Please enter a valid email address.")
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
    add_fields = (("title", "Class Title"),)

    def create_widgets(self):
        super().create_widgets()
        start_row = len(self.add_fields)

        ttk.Label(self.form_frame, text="Tutor", style="Card.TLabel").grid(
            row=start_row, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.tutor_combo = ttk.Combobox(self.form_frame, state="readonly", width=38)
        self.tutor_combo.grid(row=start_row, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Student", style="Card.TLabel").grid(
            row=start_row + 1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.student_combo = ttk.Combobox(self.form_frame, state="readonly", width=38)
        self.student_combo.grid(row=start_row + 1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Schedule", style="Card.TLabel").grid(
            row=start_row + 2, column=0, sticky=tk.NW, padx=5, pady=5
        )
        self.schedule_selector = ScheduleSelector(self.form_frame)
        self.schedule_selector.grid(row=start_row + 2, column=1, sticky=tk.W, padx=5, pady=5)

        self.add_button.grid_configure(row=start_row + 3, columnspan=2)

    def refresh(self):
        super().refresh()
        if getattr(self, "schedule_selector", None):
            self.schedule_selector.refresh()

    def add_record(self):
        title = self.form_vars["title"].get().strip()
        tutor_value = self.tutor_combo.get()
        student_value = self.student_combo.get()

        if not title or not tutor_value or not student_value:
            messagebox.showwarning("Missing data", "Please complete all fields.")
            return

        schedule = self.schedule_selector.get_schedule()
        if not schedule:
            return

        tutor_id = tutor_value.split(" — ")[0]
        student_id = student_value.split(" — ")[0]

        classes = load_records("classes")
        for lesson in classes:
            if lesson["schedule"] == schedule and (
                lesson["tutor_id"] == tutor_id or lesson["student_id"] == student_id
            ):
                messagebox.showerror(
                    "Schedule conflict",
                    "The selected tutor or student already has a class at this time.",
                )
                return

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
        init_theme(self)
        self.title(APP_TITLE)
        self.geometry("940x560")
        self.minsize(880, 520)
        self.resizable(False, False)
        self.current_user = None
        self.show_login()

    def show_login(self):
        self.current_user = None
        for child in self.winfo_children():
            child.destroy()
        self.resizable(False, False)
        self.geometry("940x560")
        login = LoginFrame(self, self.on_login_success)
        login.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, user):
        self.current_user = user
        for child in self.winfo_children():
            child.destroy()
        self.resizable(True, True)
        Dashboard(self, self.current_user)


def create_schedule_pdf(filename: Path, sections: dict[str, list[str]]):
    lines: list[str] = []
    y = 760
    title = f"Weekly Schedule — {dt.date.today().isoformat()}"
    lines.append(f"BT /F1 18 Tf 50 {y} Td ({escape_pdf_text(title)}) Tj ET")
    y -= 30
    for section_name, entries in sections.items():
        lines.append(f"BT /F1 14 Tf 50 {y} Td ({escape_pdf_text(section_name)}) Tj ET")
        y -= 22
        if not entries:
            lines.append(f"BT /F2 12 Tf 60 {y} Td (No scheduled items) Tj ET")
            y -= 18
        else:
            for entry in entries:
                if y < 60:
                    break
                lines.append(f"BT /F2 12 Tf 60 {y} Td ({escape_pdf_text(entry)}) Tj ET")
                y -= 16
        y -= 12

    content_stream = "\n".join(lines) + "\n"
    stream_bytes = content_stream.encode("utf-8")

    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        (
            b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >> endobj\n"
        ),
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> endobj\n",
        b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
        b"6 0 obj << /Length "
        + str(len(stream_bytes)).encode("ascii")
        + b" >> stream\n"
        + stream_bytes
        + b"endstream\nendobj\n",
    ]

    header = b"%PDF-1.4\n"
    offsets = []
    current = len(header)
    for obj in objects:
        offsets.append(current)
        current += len(obj)

    xref_offset = current
    xref_entries = [b"0000000000 65535 f \n"]
    for offset in offsets:
        xref_entries.append(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf_bytes = header + b"".join(objects)
    pdf_bytes += b"xref\n0 " + str(len(xref_entries)).encode("ascii") + b"\n" + b"".join(xref_entries)
    pdf_bytes += (
        b"trailer\n<< /Size "
        + str(len(xref_entries)).encode("ascii")
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_offset).encode("ascii")
        + b"\n%%EOF\n"
    )

    with filename.open("wb") as fh:
        fh.write(pdf_bytes)


class ScheduleSelector(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, style="Card.TFrame")
        self.day_var = tk.StringVar(value=DAYS[0])
        self.occupied_by_day: dict[str, set[str]] = {day: set() for day in DAYS}
        ttk.Label(self, text="Day", style="Card.TLabel").grid(row=0, column=0, sticky=tk.W)
        self.day_combo = ttk.Combobox(self, textvariable=self.day_var, values=DAYS, state="readonly", width=10)
        self.day_combo.grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self, text="Time Slot", style="Card.TLabel").grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        self.times_list = tk.Listbox(
            self,
            height=len(TIME_SLOTS),
            exportselection=False,
            width=16,
            bg=ThemePalette.SURFACE_ALT,
            fg=ThemePalette.TEXT,
            selectbackground=ThemePalette.PRIMARY,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",
        )
        self.times_list.grid(row=1, column=1, sticky=tk.NW, padx=(10, 0))
        self.current_times: list[str] = []
        self.day_var.trace_add("write", lambda *_: self.render_times())
        self.refresh()

    def refresh(self):
        self.occupied_by_day = {day: set() for day in DAYS}
        for lesson in load_records("classes"):
            day, _, time = lesson.get("schedule", "   ").partition(" ")
            if day in self.occupied_by_day and time:
                self.occupied_by_day[day].add(time)
        self.render_times()

    def render_times(self):
        day = self.day_var.get() or DAYS[0]
        self.times_list.delete(0, tk.END)
        self.current_times = []
        taken = self.occupied_by_day.get(day, set())
        for idx, slot in enumerate(TIME_SLOTS):
            self.current_times.append(slot)
            self.times_list.insert(tk.END, slot)
            if slot in taken:
                self.times_list.itemconfig(
                    idx,
                    {"bg": ThemePalette.SLOT_TAKEN_BG, "fg": ThemePalette.SLOT_TAKEN_FG},
                )
            else:
                self.times_list.itemconfig(
                    idx,
                    {"bg": ThemePalette.SLOT_AVAILABLE_BG, "fg": ThemePalette.SLOT_AVAILABLE_FG},
                )

    def get_schedule(self) -> str:
        if not self.times_list.curselection():
            return ""
        index = self.times_list.curselection()[0]
        time_value = self.current_times[index]
        day = self.day_var.get()
        if time_value in self.occupied_by_day.get(day, set()):
            messagebox.showerror("Time unavailable", "The selected time slot is already booked.")
            return ""
        return f"{day} {time_value}"
if __name__ == "__main__":
    app = TutorRenApp()
    app.mainloop()

