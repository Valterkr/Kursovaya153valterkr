import tkinter as tk
from tkinter import messagebox
import numpy as np

def solve_iteration_method(A, b, tol=1e-10, max_iterations=1000):
    n = len(b)
    x = np.zeros_like(b)
    for _ in range(max_iterations):
        x_new = np.copy(x)
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i + 1:], x[i + 1:])
            x_new[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new
    raise ValueError("Метод не сходится")

class MatrixSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор матрицы")
        self.center_window(600, 400)

        self.dimension_label = tk.Label(root, text="Введите размерность матрицы:")
        self.dimension_label.pack(pady=5)

        self.dimension_entry = tk.Entry(root)
        self.dimension_entry.pack(pady=5)

        self.dimension_button = tk.Button(root, text="Задать размер", command=self.set_dimension)
        self.dimension_button.pack(pady=5)

        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def set_dimension(self):
        try:
            self.dimension = int(self.dimension_entry.get())
            if self.dimension <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите допустимое положительное целое число для решения.")
            return

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []
        self.vector_entries = []

        matrix_label = tk.Label(self.scrollable_frame, text="Введите матрицу A:")
        matrix_label.pack(pady=5)

        self.matrix_frame = tk.Frame(self.scrollable_frame)
        self.matrix_frame.pack(pady=5)

        for i in range(self.dimension):
            row_entries = []
            for j in range(self.dimension):
                entry = tk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        self.vector_label = tk.Label(self.scrollable_frame, text="Введите вектор b:")
        self.vector_label.pack(pady=5)

        self.vector_frame = tk.Frame(self.scrollable_frame)
        self.vector_frame.pack(pady=5)

        for i in range(self.dimension):
            entry = tk.Entry(self.vector_frame, width=5)
            entry.grid(row=i, column=0, padx=5, pady=5)
            self.vector_entries.append(entry)

        self.solve_button = tk.Button(self.scrollable_frame, text="Решить", command=self.solve_matrix)
        self.solve_button.pack(pady=10)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        new_width = 300 + self.dimension * 50
        new_height = 200 + self.dimension * 30
        self.center_window(min(new_width, 1200), min(new_height, 800))  # Ограничиваем размер окна

    def solve_matrix(self):
        try:
            A = np.array([[float(self.matrix_entries[i][j].get()) for j in range(self.dimension)] for i in range(self.dimension)])
            b = np.array([float(self.vector_entries[i].get()) for i in range(self.dimension)])
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите допустимые числа.")
            return

        try:
            solution = solve_iteration_method(A, b)
            solution_str = "Solution:\n" + "\n".join([f"x{i+1} = {solution[i]}" for i in range(self.dimension)])
            messagebox.showinfo("Solution", solution_str)
        except ValueError as e:
            messagebox.showerror("Convergence Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixSolverApp(root)
    root.mainloop()
