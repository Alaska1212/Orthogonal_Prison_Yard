import tkinter as tk
from tkinter import messagebox, filedialog

from logic import is_orthogonal_polygon, decompose_grid, find_cameras
from draw import draw_final, draw_visibility_overlap, draw_visibility_single

GRID_SIZE = 20


# ---------------- ДОПОМІЖНІ ФУНКЦІЇ ----------------

def snap_to_grid(x, y):
    gx = round(x / GRID_SIZE) * GRID_SIZE
    gy = round(y / GRID_SIZE) * GRID_SIZE
    return gx, gy


def process_and_draw(root, points, include_exterior):
    if len(points) < 4:
        messagebox.showerror("Помилка", "Потрібно мінімум 4 точки.")
        return

    if not is_orthogonal_polygon(points):
        messagebox.showerror("Помилка", "Багатокутник НЕ ортогональний!")
        return

    try:
        rectangles = decompose_grid(points,
                                    include_exterior=include_exterior,
                                    padding=40)

        # тепер find_cameras повертає і камери, і карту видимості
        cameras, visibility = find_cameras(points, rectangles)

        draw_visibility_overlap(points, rectangles, cameras, visibility)
        open_camera_control_window(root, points, rectangles,
                                   cameras, visibility)

    except Exception as e:
        messagebox.showerror("Помилка алгоритму", str(e))


def open_camera_control_window(root, points, rectangles,
                               cameras, visibility):
    win = tk.Toplevel(root)
    win.title("Керування камерами")
    win.geometry("300x400")

    tk.Label(win, text=f"Знайдено камер: {len(cameras)}",
             font=("Arial", 12, "bold")).pack(pady=10)

    tk.Button(
        win, text="Показати загальну карту (Overlap)",
        command=lambda: draw_visibility_overlap(points,
                                                rectangles,
                                                cameras,
                                                visibility),
        bg="#ddffdd", height=2
    ).pack(pady=5, fill='x', padx=20)

    tk.Label(win, text="Перегляд окремих камер:",
             font=("Arial", 10)).pack(pady=10)

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True)

    for i, cam in enumerate(cameras):
        tk.Button(
            frame,
            text=f"Камера #{i + 1} {cam}",
            command=lambda c=cam: draw_visibility_single(points,
                                                         rectangles,
                                                         c,
                                                         visibility)
        ).pack(pady=2, fill='x', padx=20)


# ---------------- РЕЖИМ МАЛЮВАННЯ ----------------

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.win = tk.Toplevel(root)
        self.win.title("Малювання плану")

        control_frame = tk.Frame(self.win, bg="#f0f0f0",
                                 bd=2, relief="groove")
        control_frame.pack(side=tk.TOP, fill="x", pady=5)

        self.var_exterior = tk.BooleanVar(value=True)
        cb = tk.Checkbutton(control_frame,
                            text="Включаючи зовнішній периметр",
                            variable=self.var_exterior,
                            bg="#f0f0f0", font=("Arial", 10))
        cb.pack(side=tk.LEFT, padx=10)

        btn_calc = tk.Button(control_frame, text="РОЗРАХУВАТИ",
                             command=self.finish,
                             bg="#4aa8ff", fg="white",
                             font=("Arial", 10, "bold"))
        btn_calc.pack(side=tk.LEFT, padx=10, pady=5)

        btn_clear = tk.Button(control_frame, text="Очистити",
                              command=self.clear_canvas)
        btn_clear.pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(self.win, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.BOTTOM)

        self.points = []
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.add_point)

    def draw_grid(self):
        self.canvas.delete("grid")
        for i in range(0, 600, GRID_SIZE):
            self.canvas.create_line(i, 0, i, 600,
                                    fill="#f0f0f0", tags="grid")
            self.canvas.create_line(0, i, 600, i,
                                    fill="#f0f0f0", tags="grid")

    def add_point(self, event):
        x, y = snap_to_grid(event.x, event.y)
        self.points.append((x, y))

        r = 4
        self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                fill="blue", tags="poly")

        if len(self.points) > 1:
            x1, y1 = self.points[-2]
            self.canvas.create_line(x1, y1, x, y,
                                    fill="black", width=2, tags="poly")

    def clear_canvas(self):
        self.points = []
        self.canvas.delete("poly")

    def finish(self):
        if len(self.points) < 3:
            return

        x1, y1 = self.points[0]
        x2, y2 = self.points[-1]
        self.canvas.create_line(x2, y2, x1, y1,
                                fill="black", width=2, tags="poly")

        actual_points = self.points[:]
        if len(actual_points) > 1 and actual_points[0] == actual_points[-1]:
            actual_points.pop()

        process_and_draw(self.root, actual_points,
                         self.var_exterior.get())


# ---------------- РЕЖИМ ФАЙЛУ ----------------

def read_points_from_file(filename):
    points = []
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) < 2:
                    parts = line.strip().split()
                if len(parts) >= 2:
                    points.append((int(parts[0]), int(parts[1])))
    except Exception as e:
        messagebox.showerror("Помилка читання файлу", str(e))
        return []
    return points


def start_file_mode(root):
    filename = filedialog.askopenfilename(
        title="Виберіть файл координат",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not filename:
        return

    points = read_points_from_file(filename)
    if not points:
        return

    include_ext = messagebox.askyesno(
        "Налаштування",
        "Включати зовнішній двір у розрахунок?"
    )

    process_and_draw(root, points, include_ext)


# ---------------- ГОЛОВНЕ МЕНЮ ----------------

def start_menu():
    root = tk.Tk()
    root.title("Prison Yard Solver v2.0")
    root.geometry("300x250")

    tk.Label(root, text="Задача тюремного двору",
             font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(
        root, text="✏️ Малювати план",
        font=("Arial", 12), width=25, height=2, bg="#e1f5fe",
        command=lambda: DrawingApp(root)
    ).pack(pady=5)

    tk.Button(
        root, text="📂 Відкрити з файлу",
        font=("Arial", 12), width=25, height=2, bg="#fff9c4",
        command=lambda: start_file_mode(root)
    ).pack(pady=5)

    tk.Label(root, text="(Ортогональні полігони)",
             fg="gray").pack(side=tk.BOTTOM, pady=10)

    root.mainloop()
