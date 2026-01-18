import json
import random
import tkinter as tk
from tkinter import messagebox
import textwrap

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Подготовка к тестам")
        self.root.geometry("700x550")

        # ---------- Загрузка данных ----------
        with open("questions.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

        # ---------- Состояние ----------
        self.current_subject = None
        self.question_pool = []
        self.question_index = 0
        self.current_question = None
        self.shuffled_options = []

        # ---------- UI ----------
        self.build_ui()

    # ---------- Вспомогательные функции ----------
    def wrap_text(self, text, width=60):
        return "\n".join(textwrap.wrap(text, width))

    # ---------- UI ----------
    def build_ui(self):
        # Выбор предмета
        tk.Label(self.root, text="Выберите предмет:", font=("Arial", 12)).pack(pady=5)
        self.subject_var = tk.StringVar()
        tk.OptionMenu(self.root, self.subject_var, *self.data.keys()).pack()
        tk.Button(self.root, text="Начать", command=self.start_subject).pack(pady=10)

        # Вопрос
        self.question_label = tk.Label(
            self.root,
            text="",
            wraplength=650,
            justify="left",
            font=("Arial", 14)
        )
        self.question_label.pack(pady=20)

        # Варианты ответов
        self.buttons = []
        for i in range(4):
            btn = tk.Button(
                self.root,
                text="",
                width=65,
                wraplength=600,
                justify="left",
                anchor="w",
                pady=8,
                command=lambda i=i: self.check_answer(i)
            )
            btn.pack(pady=5)
            self.buttons.append(btn)

        # Результат
        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 12),
            justify="left"
        )
        self.result_label.pack(pady=10)

        # Следующий вопрос
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

        self.next_btn.config(state="normal")
        self.next_question()

    def next_question(self):
        if not self.question_pool:
            return

        if self.question_index >= len(self.question_pool):
            random.shuffle(self.question_pool)
            self.question_index = 0
            messagebox.showinfo("Инфо", "Все вопросы пройдены. Начинаем заново.")

        self.current_question = self.question_pool[self.question_index]
        self.question_index += 1

        self.shuffled_options = self.current_question["options"].copy()
        random.shuffle(self.shuffled_options)

        self.question_label.config(text=self.current_question["question"])
        self.result_label.config(text="")

        for i, btn in enumerate(self.buttons):
            btn.config(
                text=self.wrap_text(self.shuffled_options[i]),
                bg="SystemButtonFace",
                state="normal"
            )

    def check_answer(self, index):
        selected = self.shuffled_options[index]
        correct = self.current_question["correct"]

        for btn in self.buttons:
            btn.config(state="disabled")

        if selected == correct:
            self.buttons[index].config(bg="lightgreen")
            self.result_label.config(text="✅ Правильно!", fg="green")
        else:
            self.buttons[index].config(bg="tomato")
            self.result_label.config(
                text=f"❌ Неправильно.\nПравильный ответ:\n{correct}",
                fg="red"
            )

# ---------- Запуск ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
