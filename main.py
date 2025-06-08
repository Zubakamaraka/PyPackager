import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from packager import build_exe
import math
import time
BG_COLOR = "#000011"
PANEL_COLOR = "#001122"
ACCENT_COLOR = "#00FFFF"
ACCENT2_COLOR = "#FF00FF"
TEXT_COLOR = "#FFFFFF"
BUTTON_COLOR = "#003366"
BUTTON_HOVER = "#0066CC"
BORDER_COLOR = "#00AAAA"

translations = {
    "ru": {
        "title": "PyPackager - Сборщик EXE",
        "subtitle": "━━━ СОЗДАНО ZUBAKAMARAKA ━━━",
        "drag_project": ">>> ГЛАВНЫЙ ФАЙЛ ПРОЕКТА (.PY) <<<",
        "path": "ПУТЬ: НЕ ВЫБРАН",
        "drag_icon": ">>> ФАЙЛ ИКОНКИ (.ICO) <<<",
        "build": "[ СОБРАТЬ EXE ]",
        "start": "[+] НАЧИНАЕМ ПРОЦЕСС СБОРКИ...",
        "done": "[✓] СБОРКА ЗАВЕРШЕНА УСПЕШНО!",
        "choose_first": "ОШИБКА: СНАЧАЛА ВЫБЕРИТЕ ГЛАВНЫЙ ФАЙЛ ПРОЕКТА!",
        "invalid_icon": "ОШИБКА: НЕВЕРНЫЙ ФОРМАТ ФАЙЛА ИКОНКИ!",
        "invalid_project": "ОШИБКА: ВЫБЕРИТЕ PYTHON ФАЙЛ (.py)!",
        "lang": "РУ",
        "output_dir": ">>> ПАПКА ВЫВОДА <<<",
        "status": "ГОТОВ К РАБОТЕ",
        "credits": "СОЗДАНО: ZUBAKAMARAKA | ПРИВЕТ ВСЕМ КОДЕРАМ",
        "browse": "ОБЗОР",
        "console_title": ">>> ВЫВОД КОНСОЛИ <<<",
        "drag_ico_here": "ПЕРЕТАЩИТЕ .ICO ФАЙЛ",
        "drag_py_here": "ПЕРЕТАЩИТЕ .PY ФАЙЛ",
        "loaded": "ЗАГРУЖЕН",
        "icon": "ИКОНКА",
        "project_loaded": "ГЛАВНЫЙ ФАЙЛ ЗАГРУЖЕН",
        "project_ready": "ПРОЕКТ ГОТОВ",
        "icon_loaded": "ИКОНКА ЗАГРУЖЕНА",
        "output_folder": "ПАПКА ВЫВОДА",
        "select_project": "Выберите главный файл проекта (.py)",
        "select_icon": "Выберите файл иконки",
        "select_output": "Выберите папку для вывода",
        "error": "ОШИБКА",
        "status_building": "СБОРКА...",
        "status_complete": "СБОРКА ЗАВЕРШЕНА!",
        "status_failed": "СБОРКА ПРОВАЛЕНА!",
        "help_text": "Выберите главный файл проекта (main.py, app.py и т.д.)"
    },
    "en": {
        "title": "PyPackager - EXE Builder",
        "subtitle": "━━━ CREATED BY ZUBAKAMARAKA ━━━",
        "drag_project": ">>> MAIN PROJECT FILE (.PY) <<<",
        "path": "PATH: NOT SELECTED",
        "drag_icon": ">>> ICON FILE (.ICO) <<<",
        "build": "[ BUILD EXE ]",
        "start": "[+] STARTING BUILD PROCESS...",
        "done": "[✓] BUILD COMPLETED SUCCESSFULLY!",
        "choose_first": "ERROR: SELECT MAIN PROJECT FILE FIRST!",
        "invalid_icon": "ERROR: INVALID ICON FILE FORMAT!",
        "invalid_project": "ERROR: SELECT PYTHON FILE (.py)!",
        "lang": "EN",
        "output_dir": ">>> OUTPUT DIRECTORY <<<",
        "status": "READY FOR ACTION",
        "credits": "CODED BY: ZUBAKAMARAKA | GREETS TO: CODERS",
        "browse": "BROWSE",
        "console_title": ">>> CONSOLE OUTPUT <<<",
        "drag_ico_here": "DRAG .ICO FILE HERE",
        "drag_py_here": "DRAG .PY FILE HERE",
        "loaded": "LOADED",
        "icon": "ICON",
        "project_loaded": "MAIN FILE LOADED",
        "project_ready": "PROJECT READY",
        "icon_loaded": "ICON LOADED",
        "output_folder": "OUTPUT DIR",
        "select_project": "Select main project file (.py)",
        "select_icon": "Select icon file",
        "select_output": "Select output folder",
        "error": "ERROR",
        "status_building": "BUILDING...",
        "status_complete": "BUILD COMPLETE!",
        "status_failed": "BUILD FAILED!",
        "help_text": "Select main project file (main.py, app.py, etc.)"
    }
}


class NeonFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg=PANEL_COLOR, relief="ridge", bd=2,
                       highlightbackground=BORDER_COLOR, highlightthickness=1)


class NeonButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg=BUTTON_COLOR,
            fg=ACCENT_COLOR,
            activebackground=BUTTON_HOVER,
            activeforeground=TEXT_COLOR,
            relief="raised",
            bd=2,
            font=("Courier New", 10, "bold"),
            cursor="hand2"
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(bg=BUTTON_HOVER, fg=TEXT_COLOR)

    def on_leave(self, e):
        self.configure(bg=BUTTON_COLOR, fg=ACCENT_COLOR)


class ScrollingText(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            bg="#000000",
            fg=ACCENT_COLOR,
            insertbackground=ACCENT_COLOR,
            font=("Courier New", 9),
            relief="sunken",
            bd=2
        )


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "ru"
        self.file_path = None
        self.icon_path = None
        self.output_dir = os.getcwd()
        self.ui_elements = {}

        self.setup_window()
        self.create_header()
        self.create_main_panel()
        self.create_footer()
        self.start_animations()

    def setup_window(self):
        self.title(translations[self.lang]["title"])
        self.geometry("900x750")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (750 // 2)
        self.geometry(f"900x750+{x}+{y}")

    def create_header(self):
        header = NeonFrame(self, height=120)
        header.pack(fill="x", padx=10, pady=5)
        header.pack_propagate(False)

        self.ui_elements['title_label'] = tk.Label(header, text=translations[self.lang]["title"],
                                                   bg=PANEL_COLOR, fg=ACCENT_COLOR,
                                                   font=("Arial Black", 18, "bold"))
        self.ui_elements['title_label'].pack(pady=5)

        self.ui_elements['subtitle_label'] = tk.Label(header, text=translations[self.lang]["subtitle"],
                                                      bg=PANEL_COLOR, fg=ACCENT2_COLOR,
                                                      font=("Courier New", 10, "bold"))
        self.ui_elements['subtitle_label'].pack()

        status_frame = tk.Frame(header, bg=PANEL_COLOR)
        status_frame.pack(fill="x", pady=5)

        self.status_label = tk.Label(status_frame, text=f"[STATUS] {translations[self.lang]['status']}",
                                     bg=PANEL_COLOR, fg="#00FF00",
                                     font=("Courier New", 9))
        self.status_label.pack(side="left")
        self.lang_button = NeonButton(status_frame, text=translations[self.lang]["lang"],
                                      command=self.toggle_lang, width=3)
        self.lang_button.pack(side="right", padx=5)

    def create_main_panel(self):
        main_frame = NeonFrame(self, height=500)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        main_frame.pack_propagate(False)
        self.create_drop_section(main_frame, "drag_project", self.on_drop, 0)
        self.create_drop_section(
            main_frame, "drag_icon", self.on_icon_drop, 1, is_icon=True)
        self.create_output_section(main_frame)
        button_frame = tk.Frame(main_frame, bg=PANEL_COLOR)
        button_frame.pack(pady=15)

        self.build_button = tk.Button(button_frame, text=translations[self.lang]["build"],
                                      command=self.start_build,
                                      bg="#006600", fg="#FFFFFF", activebackground="#00AA00",
                                      font=("Arial Black", 14, "bold"),
                                      relief="raised", bd=3, cursor="hand2",
                                      width=20, height=2)
        self.build_button.pack()

        console_frame = NeonFrame(main_frame)
        console_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.ui_elements['console_label'] = tk.Label(console_frame, text=translations[self.lang]["console_title"],
                                                     bg=PANEL_COLOR, fg=ACCENT_COLOR,
                                                     font=("Courier New", 10, "bold"))
        self.ui_elements['console_label'].pack()

        self.console = ScrollingText(console_frame, height=12, wrap="word")
        self.console.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(console_frame, command=self.console.yview)
        self.console.config(yscrollcommand=scrollbar.set)

    def create_drop_section(self, parent, label_key, callback, row, is_icon=False):
        section_frame = NeonFrame(parent, height=80)
        section_frame.pack(fill="x", padx=10, pady=5)
        section_frame.pack_propagate(False)

        if is_icon:
            self.ui_elements['drag_icon_label'] = tk.Label(section_frame, text=translations[self.lang][label_key],
                                                           bg=PANEL_COLOR, fg=ACCENT2_COLOR,
                                                           font=("Courier New", 10, "bold"))
            self.ui_elements['drag_icon_label'].pack(pady=2)
        else:
            self.ui_elements['drag_project_label'] = tk.Label(section_frame, text=translations[self.lang][label_key],
                                                              bg=PANEL_COLOR, fg=ACCENT2_COLOR,
                                                              font=("Courier New", 10, "bold"))
            self.ui_elements['drag_project_label'].pack(pady=2)

        container = tk.Frame(section_frame, bg=PANEL_COLOR)
        container.pack(fill="x", padx=10, pady=2)

        drop_frame = tk.Frame(container, bg="#000033", relief="sunken", bd=2,
                              highlightbackground=BORDER_COLOR, highlightthickness=1)
        drop_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        drop_frame.drop_target_register(DND_FILES)
        drop_frame.dnd_bind('<<Drop>>', callback)
        if is_icon:
            self.ui_elements['browse_icon_btn'] = NeonButton(container, text=translations[self.lang]["browse"],
                                                             command=self.browse_icon, width=8)
            self.ui_elements['browse_icon_btn'].pack(side="right")
        else:
            self.ui_elements['browse_project_btn'] = NeonButton(container, text=translations[self.lang]["browse"],
                                                                command=self.browse_project, width=8)
            self.ui_elements['browse_project_btn'].pack(side="right")
        if not is_icon:
            self.path_label = tk.Label(drop_frame, text=translations[self.lang]["path"],
                                       bg="#000033", fg=ACCENT_COLOR,
                                       font=("Courier New", 8))
            self.path_label.pack(pady=8)
        else:
            self.icon_label = tk.Label(drop_frame, text=translations[self.lang]["drag_ico_here"],
                                       bg="#000033", fg=ACCENT_COLOR,
                                       font=("Courier New", 8))
            self.icon_label.pack(pady=8)

    def create_output_section(self, parent):
        section_frame = NeonFrame(parent, height=80)
        section_frame.pack(fill="x", padx=10, pady=5)
        section_frame.pack_propagate(False)

        self.ui_elements['output_dir_label'] = tk.Label(section_frame, text=translations[self.lang]["output_dir"],
                                                        bg=PANEL_COLOR, fg=ACCENT2_COLOR,
                                                        font=("Courier New", 10, "bold"))
        self.ui_elements['output_dir_label'].pack(pady=2)

        output_frame = tk.Frame(section_frame, bg=PANEL_COLOR)
        output_frame.pack(fill="x", padx=10, pady=2)

        self.output_label = tk.Label(output_frame, text=self.output_dir,
                                     bg="#000033", fg=ACCENT_COLOR,
                                     font=("Courier New", 8), relief="sunken", bd=1)
        self.output_label.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.ui_elements['browse_output_btn'] = NeonButton(output_frame, text=translations[self.lang]["browse"],
                                                           command=self.browse_output)
        self.ui_elements['browse_output_btn'].pack(side="right")

    def create_footer(self):
        footer = NeonFrame(self, height=40)
        footer.pack(fill="x", padx=10, pady=5)
        footer.pack_propagate(False)

        self.ui_elements['credits'] = tk.Label(footer, text=translations[self.lang]["credits"],
                                               bg=PANEL_COLOR, fg="#666666",
                                               font=("Courier New", 8))
        self.ui_elements['credits'].pack(expand=True)

    def start_animations(self):
        def blink_status():
            current_color = self.status_label.cget("fg")
            new_color = "#00FF00" if current_color == "#006600" else "#006600"
            self.status_label.configure(fg=new_color)
            self.after(1000, blink_status)

        blink_status()

    def toggle_lang(self):
        self.lang = "en" if self.lang == "ru" else "ru"
        self.update_ui_texts()

    def update_ui_texts(self):
        self.title(translations[self.lang]["title"])

        self.ui_elements['title_label'].configure(
            text=translations[self.lang]["title"])
        self.ui_elements['subtitle_label'].configure(
            text=translations[self.lang]["subtitle"])

        self.lang_button.configure(text=translations[self.lang]["lang"])
        self.build_button.configure(text=translations[self.lang]["build"])
        self.ui_elements['browse_project_btn'].configure(
            text=translations[self.lang]["browse"])
        self.ui_elements['browse_icon_btn'].configure(
            text=translations[self.lang]["browse"])
        self.ui_elements['browse_output_btn'].configure(
            text=translations[self.lang]["browse"])

        self.ui_elements['drag_project_label'].configure(
            text=translations[self.lang]["drag_project"])
        self.ui_elements['drag_icon_label'].configure(
            text=translations[self.lang]["drag_icon"])
        self.ui_elements['output_dir_label'].configure(
            text=translations[self.lang]["output_dir"])
        self.ui_elements['console_label'].configure(
            text=translations[self.lang]["console_title"])
        self.ui_elements['credits'].configure(
            text=translations[self.lang]["credits"])

        current_status = self.status_label.cget("text")
        if "ГОТОВ К РАБОТЕ" in current_status or "READY FOR ACTION" in current_status:
            self.status_label.configure(
                text=f"[STATUS] {translations[self.lang]['status']}")
        elif "ПРОЕКТ ГОТОВ" in current_status or "PROJECT READY" in current_status:
            self.status_label.configure(
                text=f"[STATUS] {translations[self.lang]['project_ready']}")

        if self.file_path is None:
            self.path_label.configure(text=translations[self.lang]["path"])

        if self.icon_path is None:
            self.icon_label.configure(
                text=translations[self.lang]["drag_ico_here"])

    def validate_python_file(self, file_path):
        """Проверяет, что файл является Python файлом"""
        return file_path.lower().endswith('.py') and os.path.isfile(file_path)

    def on_drop(self, event):
        file_path = event.data.strip('{}')
        if not self.validate_python_file(file_path):
            if os.path.isdir(file_path):
                messagebox.showerror(translations[self.lang]["error"],
                                     "Выберите файл Python (.py), а не папку!")
            else:
                messagebox.showerror(translations[self.lang]["error"],
                                     translations[self.lang]["invalid_project"])
            return

        self.file_path = file_path
        filename = os.path.basename(file_path)
        self.path_label.configure(
            text=f"{translations[self.lang]['loaded']}: {filename}")
        self.console.insert(
            "end", f"[+] {translations[self.lang]['project_loaded']}: {file_path}\n")
        self.console.see("end")
        self.status_label.configure(
            text=f"[STATUS] {translations[self.lang]['project_ready']}")

    def on_icon_drop(self, event):
        path = event.data.strip('{}')
        if path.lower().endswith(".ico") and os.path.isfile(path):
            self.icon_path = path
            filename = os.path.basename(path)
            self.icon_label.configure(
                text=f"{translations[self.lang]['icon']}: {filename}")
            self.console.insert(
                "end", f"[+] {translations[self.lang]['icon_loaded']}: {filename}\n")
            self.console.see("end")
        else:
            messagebox.showerror(
                translations[self.lang]["error"], translations[self.lang]["invalid_icon"])

    def browse_project(self):
        file_path = filedialog.askopenfilename(
            title=translations[self.lang]["select_project"],
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path and self.validate_python_file(file_path):
            self.file_path = file_path
            filename = os.path.basename(file_path)
            self.path_label.configure(
                text=f"{translations[self.lang]['loaded']}: {filename}")
            self.console.insert(
                "end", f"[+] {translations[self.lang]['project_loaded']}: {file_path}\n")
            self.console.see("end")
            self.status_label.configure(
                text=f"[STATUS] {translations[self.lang]['project_ready']}")
        elif file_path:
            messagebox.showerror(translations[self.lang]["error"],
                                 translations[self.lang]["invalid_project"])

    def browse_icon(self):
        file_path = filedialog.askopenfilename(
            title=translations[self.lang]["select_icon"],
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")]
        )
        if file_path:
            if file_path.lower().endswith(".ico"):
                self.icon_path = file_path
                filename = os.path.basename(file_path)
                self.icon_label.configure(
                    text=f"{translations[self.lang]['icon']}: {filename}")
                self.console.insert(
                    "end", f"[+] {translations[self.lang]['icon_loaded']}: {filename}\n")
                self.console.see("end")
            else:
                messagebox.showerror(translations[self.lang]["error"],
                                     translations[self.lang]["invalid_icon"])

    def browse_output(self):
        folder = filedialog.askdirectory(
            title=translations[self.lang]["select_output"]
        )
        if folder:
            self.output_dir = folder
            self.output_label.configure(text=folder)
            self.console.insert(
                "end", f"[+] {translations[self.lang]['output_folder']}: {folder}\n")
            self.console.see("end")

    def start_build(self):
        if not self.file_path:
            messagebox.showerror(
                translations[self.lang]["error"], translations[self.lang]["choose_first"])
            return

        self.console.insert("end", f"\n{'='*50}\n")
        self.console.insert("end", translations[self.lang]["start"] + "\n")
        self.console.insert("end", f"{'='*50}\n")
        self.console.see("end")
        self.status_label.configure(
            text=f"[STATUS] {translations[self.lang]['status_building']}")
        self.update()

        try:
            for line in build_exe(self.file_path, self.icon_path, self.output_dir):
                self.console.insert("end", f"[BUILD] {line}\n")
                self.console.see("end")
                self.update()

            self.console.insert("end", f"\n{'='*50}\n")
            self.console.insert("end", translations[self.lang]["done"] + "\n")
            self.console.insert("end", f"{'='*50}\n\n")
            self.console.see("end")
            self.status_label.configure(
                text=f"[STATUS] {translations[self.lang]['status_complete']}")

        except Exception as e:
            self.console.insert("end", f"[ERROR] BUILD FAILED: {str(e)}\n")
            self.status_label.configure(
                text=f"[STATUS] {translations[self.lang]['status_failed']}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
