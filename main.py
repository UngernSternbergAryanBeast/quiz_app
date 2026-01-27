import tkinter as tk

from app import QuizApp



# ---------- Запуск ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
