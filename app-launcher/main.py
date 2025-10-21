import tkinter as tk
from tkinter import filedialog, messagebox, Listbox
import subprocess
import json
import os

CONFIG_FILE = "apps.json"

class AppLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("App Launcher")
        self.root.geometry("500x400")

        self.apps = self.load_apps()

        # Список приложений
        self.listbox = Listbox(self.root, height=15)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Кнопки
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(frame, text="Добавить", command=self.add_app).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Удалить", command=self.remove_app).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Запустить всё", command=self.run_all).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Сохранить", command=self.save_apps).pack(side=tk.LEFT, padx=5)

        self.refresh_list()

    def add_app(self):
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Выберите приложение",
            filetypes=[
                ("Executable files", "*.exe"),
                ("All files", "*.*")
            ]
        )
        if filename:
            if filename not in self.apps:
                self.apps.append(filename)
                self.refresh_list()

    def remove_app(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            del self.apps[index]
            self.refresh_list()
        else:
            messagebox.showwarning("Предупреждение", "Выберите приложение для удаления")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for app in self.apps:
            self.listbox.insert(tk.END, os.path.basename(app))

    def run_all(self):
        for app in self.apps:
            if os.path.isfile(app):
                subprocess.Popen([app])
            else:
                messagebox.showerror("Ошибка", f"Файл не найден: {app}")

    def save_apps(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.apps, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Сохранено", "Список приложений сохранён!")

    def load_apps(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLauncher(root)
    root.mainloop()