from collections import Counter


# ============================
# 1. ОРТОГОНАЛЬНІСТЬ ПОЛІГОНА
# ============================

def is_orthogonal_polygon(points):
    n = len(points)
    if n < 4:
        return False

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        if not (x1 == x2 or y1 == y2):
            return False
    return True


# ============================
# 2. ТОЧКА ВСЕРЕДИНІ ПОЛІГОНА
# ============================

def is_point_inside(poly, p):
    x, y = p
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


# ============================
# 3. РОЗБИТТЯ НА ПРЯМОКУТНИКИ
# ============================

def decompose_grid(points, include_exterior=True, padding=40):
    """
    Розбиває простір на прямокутники по сітці з координат вершин.
    Якщо include_exterior=True — додає буфер навколо полігона.
    """
    xs = sorted(list(set([p[0] for p in points])))
    ys = sorted(list(set([p[1] for p in points])))

    if include_exterior:
        min_x, max_x = xs[0], xs[-1]
        min_y, max_y = ys[0], ys[-1]
        xs.insert(0, min_x - padding)
        xs.append(max_x + padding)
        ys.insert(0, min_y - padding)
        ys.append(max_y + padding)

    rectangles = []

    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            x1, x2 = xs[i], xs[i + 1]
            y1, y2 = ys[j], ys[j + 1]

            rect = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2

            if not include_exterior:
                # тільки внутрішні прямокутники
                if is_point_inside(points, (mid_x, mid_y)):
                    rectangles.append(rect)
            else:
                # внутрішні + зовнішні
                rectangles.append(rect)

    return rectangles


# ============================
# 4. ВИДИМІСТЬ ПО КОРИДОРАХ
# ============================

def can_see_center(poly, v, center, steps=8):
    """
    Камера в точці v бачить точку center,
    якщо вони на одній вертикалі або горизонталі
    і весь відрізок між ними лежить всередині полігона.
    """
    vx, vy = v
    cx, cy = center

    # тільки по коридору (по осі)
    if not (vx == cx or vy == cy):
        return False

    # перевіряємо промінь дискретно
    for i in range(1, steps):
        t = i / steps
        x = vx + (cx - vx) * t
        y = vy + (cy - vy) * t
        if not is_point_inside(poly, (x, y)):
            return False

    return True


# ============================
# 5. ПОШУК КАМЕР + КАРТА ВИДИМОСТІ
# ============================

def find_cameras(points, rectangles):
    """
    points     – вершини ортогонального багатокутника
    rectangles – список прямокутників (з decompose_grid)

    Повертає:
        cameras    – список вершин, де ставимо камери
        visibility – dict: camera -> список прямокутників, які вона бачить
    """

    # унікальні вершини полігона
    vertices = []
    seen = set()
    for p in points:
        if p not in seen:
            seen.add(p)
            vertices.append(p)

    # центри всіх прямокутників
    rect_centers = []
    for rect in rectangles:
        (x1, y1) = rect[0]
        (x2, y2) = rect[2]
        rect_centers.append(((x1 + x2) / 2, (y1 + y2) / 2))

    # індекси прямокутників, які лежать всередині полігона
    target_indices = set(
        i for i, c in enumerate(rect_centers)
        if is_point_inside(points, c)
    )

    # які прямокутники (з target_indices) бачить кожна вершина
    visible_by_vertex = {v: set() for v in vertices}
    for i in target_indices:
        center = rect_centers[i]
        for v in vertices:
            if can_see_center(points, v, center):
                visible_by_vertex[v].add(i)

    remaining = set(target_indices)
    cameras = []

    # жадібний hitting set
    while remaining:
        best_v = None
        best_cover = set()

        for v, covers in visible_by_vertex.items():
            cover = covers & remaining
            if len(cover) > len(best_cover):
                best_cover = cover
                best_v = v

        if not best_cover:
            # залишились прямокутники, яких не бачить жодна вершина
            break

        cameras.append(best_v)
        remaining -= best_cover

    # будуємо карту видимості тільки для вибраних камер
    visibility = {cam: [] for cam in cameras}
    for cam in cameras:
        for i in visible_by_vertex.get(cam, set()):
            visibility[cam].append(rectangles[i])

    return cameras, visibility
