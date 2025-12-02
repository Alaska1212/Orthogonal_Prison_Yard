from scipy.spatial import Delaunay #я використовую триангуляцію Делоне, щоб розбити багатокутник
# на трикутники. це потрібно для алгоритму пошуку камер — ми шукаємо,
# які вершини покривають найбільше трикутників.

from collections import Counter #цей клас дає можливість легко порахувати,
# скільки разів кожна точка з’являється у всіх трикутниках.за його допомогою я знаходжу вершину,
# яка зустрічається найчастіше — саме її я вибираю як "камеру".


# ця функція перевіряє, чи є кожне ребро вертикальним або горизонтальним.
# тобто ми переконуємось, що багатокутник ортогональний.
def is_orthogonal_polygon(points):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        dx = x2 - x1
        dy = y2 - y1

        # якщо обидва зміщення не нульові — ребро косе → багатокутник не ортогональний
        if not (dx == 0 or dy == 0):
            return False
    return True


# тут я будую триангуляцію Делоне по заданих точках.
# результат — список трикутників (кожен трикутник це 3 вершини).
def delaunay_triangulation(points):
    tri = Delaunay(points)
    triangles = tri.simplices.tolist()
    return [[points[i] for i in triangle] for triangle in triangles]


# основна ідея: жадібно вибираємо ту вершину, яка входить у найбільшу кількість трикутників,
# бо вона "покриває" найбільшу площу. потім прибираємо всі трикутники, де ця точка присутня.
# повторюємо, поки трикутники не закінчаться.
def find_cameras(triangles):
    cameras = []
    remaining = triangles[:]  # копія, щоб не зіпсувати вхідні дані

    while remaining:
        # збираємо всі точки з усіх трикутників в один список
        all_points = [p for t in remaining for p in t]

        # знаходимо найбільш повторювану вершину
        most_common, _ = Counter(all_points).most_common(1)[0]
        cameras.append(most_common)

        # видаляємо трикутники, які вже покриває ця камера
        remaining = [t for t in remaining if most_common not in t]

    return cameras
