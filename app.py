import json
import random
import tkinter as tk
from tkinter import messagebox, filedialog


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Подготовка к тестам")
        self.root.geometry("720x620")

        # ---------- Загрузка данных ----------


        # ---------- Состояние ----------
        self.current_subject = None
        self.question_pool = []
        self.question_index = 0
        self.current_question = None
        self.shuffled_options = []

        # ---------- Счётчики ----------
        self.correct_count = 0
        self.wrong_count = 0

        # ---------- UI ----------
        self.build_pre_ui()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
            return False

        return True
    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def go_to_main_app(self):
        self.build_ui()
    def build_pre_ui(self):
        self.clear_ui()
        tk.Button(self.root, text="Выбрать файл", command=self.try_open_file).pack(pady=20)
        self.continue_btn = tk.Button(
            self.root,
            text="Продолжить",
            command=self.go_to_main_app,
            state="disabled"
        )
        self.continue_btn.pack(pady=10)

    def try_open_file(self):
        if self.open_file():
            self.continue_btn.config(state="normal")

    # ---------- UI ----------
    def build_ui(self):
        self.clear_ui()
        tk.Label(self.root, text="Выберите предмет:", font=("Arial", 12)).pack(pady=5)

        self.subject_var = tk.StringVar()
        tk.OptionMenu(self.root, self.subject_var, *self.data.keys()).pack()

        tk.Button(
            self.root,
            text="Начать попытку",
            command=self.start_subject
        ).pack(pady=10)

        # ---------- Панель статистики ----------
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=8)

        self.correct_label = tk.Label(
            stats_frame,
            text="Правильных: 0",
            font=("Arial", 12, "bold"),
            fg="green"
        )
        self.correct_label.pack(side="left", padx=15)

        self.wrong_label = tk.Label(
            stats_frame,
            text="Неправильных: 0",
            font=("Arial", 12, "bold"),
            fg="red"
        )
        self.wrong_label.pack(side="left", padx=15)

        self.percent_label = tk.Label(
            stats_frame,
            text="Процент: 0.0%",
            font=("Arial", 12, "bold")
        )
        self.percent_label.pack(side="left", padx=15)

        # ---------- Вопрос ----------
        self.question_label = tk.Label(
            self.root,
            text="",
            wraplength=680,
            justify="left",
            font=("Arial", 14)
        )
        self.question_label.pack(pady=20)

        # ---------- Кнопки ответов ----------
        self.answers_frame = tk.Frame(self.root)
        self.answers_frame.pack(fill="both", padx=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(
                self.answers_frame,
                text="",
                wraplength=820,  # 🔑 перенос текста
                justify="left",
                anchor="w",
                font=("Arial", 12),
                padx=10,
                pady=8,
                command=lambda i=i: self.check_answer(i)
            )
            btn.pack(anchor="w", fill="x", pady=5)
            self.buttons.append(btn)

        self.result_label = tk.Label(
            self.root,
            font=("Arial", 12),
            wraplength=850,
            justify="left"
        )
        self.result_label.pack(pady=10, padx=20)

        self.next_btn = tk.Button(
            self.root,
            text="Следующий вопрос",
            command=self.next_question,
            state="disabled"
        )
        self.next_btn.pack(pady=10)

        # ---------- Результат ----------
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # ---------- Следующий ----------
        self.next_btn = tk.Button(
            self.root,
            text="Следующий вопрос",
            command=self.next_question,
            state="disabled"
        )
        self.next_btn.pack(pady=10)

        # ---------- Вотерка ----------
        watermark = tk.Label(
            self.root,
            text="сделано Кикиславом",
            font=("Arial", 10, "italic"),
            fg="gray"
        )
        watermark.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)

    # ---------- Логика ----------
    def start_subject(self):
        subject = self.subject_var.get()
        if not subject:
            messagebox.showwarning("Ошибка", "Выберите предмет")
            return

        self.current_subject = subject
        self.question_pool = self.data[subject].copy()
        random.shuffle(self.question_pool)

        self.question_index = 0
        self.correct_count = 0
        self.wrong_count = 0

        self.update_stats()
        self.next_btn.config(state="normal")
        self.next_question()

    def next_question(self):
        if self.question_index >= len(self.question_pool):
            self.show_final_result()
            return

        self.current_question = self.question_pool[self.question_index]
        self.question_index += 1

        self.shuffled_options = self.current_question["options"].copy()
        random.shuffle(self.shuffled_options)

        self.question_label.config(text=self.current_question["question"])
        self.result_label.config(text="")

        for i, btn in enumerate(self.buttons):
            btn.config(
                text=self.shuffled_options[i],
                bg="SystemButtonFace",
                state="normal"
            )

    def check_answer(self, index):
        selected = self.shuffled_options[index]
        correct = self.current_question["correct"]

        for btn in self.buttons:
            btn.config(state="disabled")

        if selected == correct:
            self.correct_count += 1
            self.buttons[index].config(bg="lightgreen")
            self.result_label.config(text="✅ Правильно!", fg="green")
        else:
            self.wrong_count += 1
            self.buttons[index].config(bg="tomato")
            self.result_label.config(
                text=f"❌ Неправильно.\nПравильный ответ:\n{correct}",
                fg="red"
            )

        self.update_stats()

    def update_stats(self):
        total = self.correct_count + self.wrong_count
        percent = (self.correct_count / total * 100) if total > 0 else 0

        self.correct_label.config(text=f"Правильных: {self.correct_count}")
        self.wrong_label.config(text=f"Неправильных: {self.wrong_count}")
        self.percent_label.config(text=f"Процент: {percent:.1f}%")

    def show_final_result(self):
        total = self.correct_count + self.wrong_count
        percent = (self.correct_count / total * 100) if total > 0 else 0

        messagebox.showinfo(
            "Результат попытки",
            f"Предмет: {self.current_subject}\n\n"
            f"Всего вопросов: {total}\n"
            f"Правильных: {self.correct_count}\n"
            f"Неправильных: {self.wrong_count}\n"
            f"Процент правильных: {percent:.1f}%"
        )

        self.question_label.config(text="Попытка завершена")
        self.result_label.config(text="")
        self.next_btn.config(state="disabled")

        for btn in self.buttons:
            btn.config(text="", state="disabled")