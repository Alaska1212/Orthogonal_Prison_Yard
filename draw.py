import matplotlib.pyplot as plt #tkinter — стандартна графічна бібліотека Python.
# це те, що створює вікна програми, кнопки, полотно для малювання тощо.


# малювання полігона та камер на підсумковій картинці
def draw_final(points, cameras):
    # додаю першу точку наприкінці, щоб замкнути контур
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]

    cam_x = [p[0] for p in cameras]
    cam_y = [p[1] for p in cameras]

    plt.figure(figsize=(7, 6))
    plt.plot(xs, ys, color='gray', linewidth=1.6)  # обводка полігона
    plt.scatter(xs[:-1], ys[:-1], color='#4aa8ff', s=50, label='Вершини')
    plt.scatter(cam_x, cam_y, color='black', marker='s', s=90, label='Камери')

    plt.title("Orthogonal Prison Yard")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend()
    plt.show()


# тут я показую, які трикутники бачить кожна камера.
# кожній камері — свій колір.
def draw_visibility(points, triangles, cameras):
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]

    plt.figure(figsize=(7, 6))
    plt.plot(xs, ys, color='gray', linewidth=1.6)

    # підготовлені різні кольори для камер
    colors = ["#ff9999", "#99ff99", "#9999ff", "#ffcc99",
              "#cc99ff", "#99ffcc", "#ff99cc", "#66ccff"]

    # перебираю всі камери
    for cam_index, cam in enumerate(cameras):
        color = colors[cam_index % len(colors)]

        # закрашую трикутники, де присутня ця камера
        for tri in triangles:
            if cam in tri:
                tx = [tri[0][0], tri[1][0], tri[2][0]]
                ty = [tri[0][1], tri[1][1], tri[2][1]]
                plt.fill(tx, ty, color=color, alpha=0.35)

    plt.scatter(xs[:-1], ys[:-1], color='#4aa8ff', s=50)  # вершини
    plt.scatter([c[0] for c in cameras], [c[1] for c in cameras],
                color='black', marker='s', s=90)  # камери

    plt.title("Зони видимості камер")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()


# те саме, але для однієї конкретної камери
def draw_visibility_single(points, triangles, camera):
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]

    plt.figure(figsize=(7, 6))
    plt.plot(xs, ys, color='gray', linewidth=1.6)

    color = "#ffcc66"  # фіксований колір для видимості однієї камери

    for tri in triangles:
        if camera in tri:
            tx = [tri[0][0], tri[1][0], tri[2][0]]
            ty = [tri[0][1], tri[1][1], tri[2][1]]
            plt.fill(tx, ty, color=color, alpha=0.45)

    plt.scatter(xs[:-1], ys[:-1], color='#4aa8ff', s=50)
    plt.scatter([camera[0]], [camera[1]], marker='s', color='black', s=120)

    plt.title(f"Видимість вибраної камери {camera}")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()
