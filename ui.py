import tkinter as tk #графічна бібліотека для створення кнопок, вікон і тд.
from tkinter import messagebox, filedialog

#messagebox потрібен для виведення вікон з помилками (наприклад "полігон не ортогональний").
#filedialog дозволяє обирати файл з точками у режимі "зчитати з файлу".

from laba.triangle.logic import is_orthogonal_polygon, delaunay_triangulation, find_cameras
from laba.triangle.draw import draw_final, draw_visibility, draw_visibility_single

GRID_SIZE = 20  # розмір клітинки для сітки

# ця функція притягує координати до найближчої клітинки сітки
def snap_to_grid(x, y):
    gx = round(x / GRID_SIZE) * GRID_SIZE
    gy = round(y / GRID_SIZE) * GRID_SIZE
    return gx, gy


# окреме вікно, де користувач може вибрати, яку камеру візуалізувати окремо
def select_camera_menu(root, points, triangles, cameras):
    win = tk.Toplevel(root)
    win.title("Вибір камери")

    tk.Label(win, text="Оберіть камеру:", font=("Arial", 12)).pack(pady=10)

    for cam in cameras:
        tk.Button(
            win,
            text=f"Камера {cam}",
            width=30,
            command=lambda c=cam: draw_visibility_single(points, triangles, c)
        ).pack(pady=4)

class DrawingApp:
    def __init__(self, root):
        self.root = root

        # окреме вікно для малювання
        self.win = tk.Toplevel(root)
        self.win.title("Малювання багатокутника")

        self.canvas = tk.Canvas(self.win, width=600, height=600, bg="white")
        self.canvas.pack()

        self.points = []  # список вершин багатокутника

        self.draw_grid()  # малюю сітку
        self.canvas.bind("<Button-1>", self.add_point)  # клік додає точку

        tk.Button(self.win, text="Завершити", command=self.finish).pack(pady=10)

    # малюю сітку
    def draw_grid(self):
        for i in range(0, 600, GRID_SIZE):
            self.canvas.create_line(i, 0, i, 600, fill="#e0e0e0")
            self.canvas.create_line(0, i, 600, i, fill="#e0e0e0")

    # додаю нову вершину
    def add_point(self, event):
        x, y = snap_to_grid(event.x, event.y)
        self.points.append((x, y))

        # малюю маленьке коло у точці
        r = 4
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="blue")

        # якщо це не перша точка — проводжу лінію
        if len(self.points) > 1:
            x1, y1 = self.points[-2]
            self.canvas.create_line(x1, y1, x, y, fill="black", width=2)

    # завершуємо малювання полігона
    def finish(self):
        if len(self.points) < 4:
            messagebox.showerror("Помилка", "Потрібно мінімум 4 точки.")
            return

        # замкнути полігон останньою лінією
        x1, y1 = self.points[0]
        x2, y2 = self.points[-1]
        self.canvas.create_line(x2, y2, x1, y1, fill="black", width=2)

        # перевірка: полігон ортогональний чи ні
        if not is_orthogonal_polygon(self.points):
            messagebox.showerror("Помилка", "Багатокутник НЕ ортогональний!")
            return

        # триангуляція → пошук камер → візуалізація
        triangles = delaunay_triangulation(self.points)
        cameras = find_cameras(triangles)

        draw_final(self.points, cameras)
        draw_visibility(self.points, triangles, cameras)
        select_camera_menu(self.root, self.points, triangles, cameras)

def read_points_from_file(filename):
    points = []
    with open(filename, "r") as f:
        for line in f:
            x, y = map(int, line.strip().split(","))
            points.append((x, y))
    return points

def start_file_mode(root):
    filename = filedialog.askopenfilename(
        title="Виберіть файл", filetypes=[("Text files", "*.txt")]
    )
    if not filename:
        return

    points = read_points_from_file(filename)

    if not is_orthogonal_polygon(points):
        messagebox.showerror("Помилка", "Багатокутник НЕ ортогональний!")
        return

    triangles = delaunay_triangulation(points)
    cameras = find_cameras(triangles)

    draw_final(points, cameras)
    draw_visibility(points, triangles, cameras)
    select_camera_menu(root, points, triangles, cameras)


def start_menu():
    root = tk.Tk()
    root.title("Виберіть режим")

    tk.Label(root, text="Оберіть режим:", font=("Arial", 12)).pack(pady=10)

    tk.Button(
        root, text="Малювати мишкою", width=30,
        command=lambda: DrawingApp(root)
    ).pack(pady=5)

    tk.Button(
        root, text="Зчитати з файла", width=30,
        command=lambda: start_file_mode(root)
    ).pack(pady=5)

    root.mainloop()
