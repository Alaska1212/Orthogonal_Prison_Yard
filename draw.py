import matplotlib.pyplot as plt


def draw_final(points, cameras):
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]

    cam_x = [p[0] for p in cameras]
    cam_y = [p[1] for p in cameras]

    plt.figure(figsize=(8, 7))
    plt.plot(xs, ys, color='black', linewidth=3, zorder=10)

    if cameras:
        plt.scatter(cam_x, cam_y, color='red', marker='D', s=80,
                    label='Камери', zorder=11)

    plt.title("Розміщення камер")
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.3)
    if cameras:
        plt.legend()
    plt.show()


def draw_visibility_overlap(points, rectangles, cameras, visibility):
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]

    plt.figure(figsize=(8, 7))

    colors = ["#FF9999", "#99FF99", "#9999FF",
              "#FFFF99", "#99FFFF", "#FF99FF"]

    # малюємо зони видимості для кожної камери
    for i, cam in enumerate(cameras):
        color = colors[i % len(colors)]
        rects = visibility.get(cam, [])
        for rect in rects:
            rx = [p[0] for p in rect] + [rect[0][0]]
            ry = [p[1] for p in rect] + [rect[0][1]]
            plt.fill(rx, ry, color=color, alpha=0.35, edgecolor=None)

    # контур полігона
    plt.plot(xs, ys, color='black', linewidth=3, zorder=20)

    # камери
    if cameras:
        cam_x = [c[0] for c in cameras]
        cam_y = [c[1] for c in cameras]
        plt.scatter(cam_x, cam_y, color='black', marker='D',
                    s=60, zorder=21, label="Камери")

    plt.title("Зони видимості з накладанням (Overlap)")
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.3)
    if cameras:
        plt.legend()
    plt.show()


def draw_visibility_single(points, rectangles, camera, visibility):
    xs = [p[0] for p in points] + [points[0][0]]
    ys = [p[1] for p in points] + [points[0][1]]

    plt.figure(figsize=(8, 7))
    plt.plot(xs, ys, color='black', linewidth=3, zorder=10)

    color = "#ffcc66"
    rects = visibility.get(camera, [])

    count = 0
    for rect in rects:
        rx = [p[0] for p in rect] + [rect[0][0]]
        ry = [p[1] for p in rect] + [rect[0][1]]
        plt.fill(rx, ry, color=color, alpha=0.6,
                 edgecolor='white')
        count += 1

    plt.scatter([camera[0]], [camera[1]], marker='D',
                color='red', s=100, zorder=11)

    plt.title(f"Одна камера бачить {count} блоків")
    plt.axis('equal')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.show()
