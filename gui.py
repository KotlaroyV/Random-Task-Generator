import tkinter as tk
from tkinter import ttk, messagebox
from task_manager import TaskManager
from datetime import datetime

class TaskGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("800x600")
        
        self.task_manager = TaskManager()
        
        self.setup_ui()
        self.update_category_list()
        self.update_history()
    
    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Генератор случайных задач", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Фрейм для фильтрации и генерации
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Фильтр по типу задачи
        tk.Label(control_frame, text="Тип задачи:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(control_frame, textvariable=self.filter_var, 
                                         state="readonly", width=20)
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        
        # Кнопка генерации
        self.generate_btn = tk.Button(control_frame, text="🎲 Сгенерировать задачу", 
                                      command=self.generate_task, 
                                      bg="#4CAF50", fg="white", 
                                      font=("Arial", 10, "bold"))
        self.generate_btn.pack(side=tk.LEFT, padx=20)
        
        # Отображение последней сгенерированной задачи
        self.task_display = tk.Label(self.root, text="Нажмите кнопку для генерации задачи", 
                                    font=("Arial", 12), bg="#f0f0f0", 
                                    relief=tk.RAISED, padx=10, pady=10)
        self.task_display.pack(pady=15, padx=20, fill=tk.X)
        
        # Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Вкладка истории
        self.history_frame = tk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📋 История")
        self.setup_history_tab()
        
        # Вкладка управления задачами
        self.manage_frame = tk.Frame(self.notebook)
        self.notebook.add(self.manage_frame, text="⚙️ Управление задачами")
        self.setup_manage_tab()
    
    def setup_history_tab(self):
        # Фильтр для истории
        filter_frame = tk.Frame(self.history_frame)
        filter_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT, padx=5)
        
        self.history_filter_var = tk.StringVar(value="Все")
        history_filter_combo = ttk.Combobox(filter_frame, 
                                           textvariable=self.history_filter_var,
                                           state="readonly", width=20)
        history_filter_combo['values'] = ["Все"] + self.task_manager.get_categories()
        history_filter_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(filter_frame, text="Применить фильтр", 
                 command=self.update_history).pack(side=tk.LEFT, padx=5)
        
        tk.Button(filter_frame, text="Обновить", 
                 command=self.update_history).pack(side=tk.LEFT, padx=5)
        
        # Список истории
        list_frame = tk.Frame(self.history_frame)
        list_frame.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                         font=("Courier", 10))
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
    
    def setup_manage_tab(self):
        # Добавление новой задачи
        add_frame = tk.LabelFrame(self.manage_frame, text="Добавить новую задачу", 
                                 padx=10, pady=10)
        add_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(add_frame, text="Категория:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.add_category_var = tk.StringVar()
        self.add_category_combo = ttk.Combobox(add_frame, 
                                              textvariable=self.add_category_var,
                                              state="readonly", width=25)
        self.add_category_combo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Задача:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.task_entry = tk.Entry(add_frame, width=30, font=("Arial", 10))
        self.task_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(add_frame, text="Добавить задачу", 
                 command=self.add_task, 
                 bg="#2196F3", fg="white").grid(row=2, column=0, columnspan=2, pady=10)
        
        # Добавление новой категории
        category_frame = tk.LabelFrame(self.manage_frame, text="Добавить новую категорию", 
                                      padx=10, pady=10)
        category_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.category_entry = tk.Entry(category_frame, width=30, font=("Arial", 10))
        self.category_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(category_frame, text="Добавить категорию", 
                 command=self.add_category,
                 bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Просмотр задач по категориям
        view_frame = tk.LabelFrame(self.manage_frame, text="Просмотр задач", 
                                  padx=10, pady=10)
        view_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        tk.Label(view_frame, text="Категория:").pack(side=tk.LEFT, padx=5)
        
        self.view_category_var = tk.StringVar()
        self.view_category_combo = ttk.Combobox(view_frame, 
                                               textvariable=self.view_category_var,
                                               state="readonly", width=20)
        self.view_category_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Button(view_frame, text="Показать задачи", 
                 command=self.show_tasks_by_category).pack(side=tk.LEFT, padx=5)
        
        tasks_list_frame = tk.Frame(view_frame)
        tasks_list_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(tasks_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tasks_listbox = tk.Listbox(tasks_list_frame, yscrollcommand=scrollbar.set,
                                       font=("Arial", 10))
        self.tasks_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)
    
    def generate_task(self):
        """Генерирует случайную задачу"""
        filter_type = self.filter_var.get()
        
        if filter_type == "Все":
            task_record = self.task_manager.generate_task()
        else:
            task_record = self.task_manager.generate_task(filter_type)
        
        if task_record:
            timestamp = datetime.fromisoformat(task_record['timestamp'])
            time_str = timestamp.strftime("%H:%M:%S")
            
            display_text = f"📌 {task_record['task']} [{task_record['type'].upper()}]"
            self.task_display.config(text=display_text, fg="#2196F3")
            
            self.task_manager.save_data()
            self.update_history()
        else:
            messagebox.showwarning("Предупреждение", 
                                 "Нет доступных задач для выбранного типа!")
    
    def add_task(self):
        """Добавляет новую задачу"""
        category = self.add_category_var.get()
        task = self.task_entry.get().strip()
        
        if not task:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return
        
        if not category:
            messagebox.showerror("Ошибка", "Выберите категорию!")
            return
        
        if self.task_manager.add_task(category, task):
            messagebox.showinfo("Успех", f"Задача '{task}' добавлена в категорию '{category}'")
            self.task_entry.delete(0, tk.END)
            self.task_manager.save_data()
        else:
            messagebox.showwarning("Предупреждение", "Такая задача уже существует!")
    
    def add_category(self):
        """Добавляет новую категорию"""
        category = self.category_entry.get().strip()
        
        if not category:
            messagebox.showerror("Ошибка", "Название категории не может быть пустым!")
            return
        
        if self.task_manager.add_category(category):
            messagebox.showinfo("Успех", f"Категория '{category}' добавлена!")
            self.category_entry.delete(0, tk.END)
            self.update_category_list()
            self.task_manager.save_data()
        else:
            messagebox.showwarning("Предупреждение", "Такая категория уже существует!")
    
    def update_category_list(self):
        """Обновляет списки категорий"""
        categories = ["Все"] + self.task_manager.get_categories()
        
        self.filter_combo['values'] = categories
        self.add_category_combo['values'] = self.task_manager.get_categories()
        self.view_category_combo['values'] = self.task_manager.get_categories()
        
        if not self.filter_var.get():
            self.filter_var.set("Все")
    
    def show_tasks_by_category(self):
        """Показывает задачи выбранной категории"""
        category = self.view_category_var.get()
        
        if not category:
            messagebox.showwarning("Предупреждение", "Выберите категорию!")
            return
        
        self.tasks_listbox.delete(0, tk.END)
        
        if category in self.task_manager.tasks:
            tasks = self.task_manager.tasks[category]
            for i, task in enumerate(tasks, 1):
                self.tasks_listbox.insert(tk.END, f"{i}. {task}")
            
            if not tasks:
                self.tasks_listbox.insert(tk.END, "Нет задач в этой категории")
        else:
            self.tasks_listbox.insert(tk.END, "Категория не найдена")
    
    def update_history(self):
        """Обновляет список истории"""
        self.history_listbox.delete(0, tk.END)
        
        filter_type = self.history_filter_var.get()
        
        if filter_type == "Все":
            history = self.task_manager.get_history()
        else:
            history = self.task_manager.get_history(filter_type)
        
        for i, record in enumerate(reversed(history[-50:]), 1):  # Показываем последние 50 записей
            timestamp = datetime.fromisoformat(record['timestamp'])
            time_str = timestamp.strftime("%d.%m.%Y %H:%M:%S")
            self.history_listbox.insert(tk.END, 
                                       f"{i}. [{time_str}] {record['type'].upper()}: {record['task']}")

def main():
    root = tk.Tk()
    app = TaskGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()