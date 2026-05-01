import json
import random
from datetime import datetime
from typing import List, Dict, Optional

class TaskManager:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: Dict[str, List[str]] = {
            "учеба": ["Прочитать статью", "Решить задачу", "Посмотреть лекцию", 
                     "Написать конспект", "Подготовиться к тесту"],
            "спорт": ["Сделать зарядку", "Пробежать 5 км", "Отжаться 30 раз", 
                     "Сделать растяжку", "Позаниматься йогой"],
            "работа": ["Ответить на email", "Подготовить отчет", "Провести встречу", 
                      "Обновить документацию", "Проверить дедлайны"]
        }
        self.history: List[Dict] = []
        self.load_data()
    
    def add_task(self, task_type: str, task: str) -> bool:
        """Добавляет новую задачу в указанную категорию"""
        if not task or not task.strip():
            return False
        
        task = task.strip()
        if task_type in self.tasks:
            if task not in self.tasks[task_type]:
                self.tasks[task_type].append(task)
                return True
        return False
    
    def add_category(self, category: str) -> bool:
        """Добавляет новую категорию"""
        category = category.strip().lower()
        if category and category not in self.tasks:
            self.tasks[category] = []
            return True
        return False
    
    def generate_task(self, task_type: Optional[str] = None) -> Optional[Dict]:
        """Генерирует случайную задачу"""
        if task_type and task_type in self.tasks and self.tasks[task_type]:
            task = random.choice(self.tasks[task_type])
        elif not task_type:
            # Выбираем из всех категорий
            all_tasks = []
            for tasks in self.tasks.values():
                all_tasks.extend(tasks)
            if all_tasks:
                task = random.choice(all_tasks)
                task_type = self.get_task_type(task)
            else:
                return None
        else:
            return None
        
        task_record = {
            "task": task,
            "type": task_type,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(task_record)
        return task_record
    
    def get_task_type(self, task: str) -> str:
        """Определяет тип задачи"""
        for task_type, tasks in self.tasks.items():
            if task in tasks:
                return task_type
        return "неизвестно"
    
    def get_history(self, task_type: Optional[str] = None) -> List[Dict]:
        """Возвращает историю задач с возможностью фильтрации"""
        if task_type:
            return [h for h in self.history if h.get("type") == task_type]
        return self.history
    
    def get_categories(self) -> List[str]:
        """Возвращает список категорий"""
        return list(self.tasks.keys())
    
    def save_data(self):
        """Сохраняет задачи и историю в JSON файл"""
        data = {
            "tasks": self.tasks,
            "history": self.history
        }
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_data(self):
        """Загружает задачи и историю из JSON файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = data.get("tasks", self.tasks)
                self.history = data.get("history", [])
        except FileNotFoundError:
            self.save_data()
        except Exception as e:
            print(f"Ошибка загрузки: {e}")