import heapq
import math

INF = math.inf

# Варіант № 8 (w(2, 5) = 3 задано згідно з приміткою в методичці)
EDGES = [
    (1, 2, 2), (1, 3, 5), (1, 4, 1), (1, 7, 7),
    (2, 4, 3), (2, 5, 3), (3, 5, 2), (3, 6, 4),
    (3, 7, 4), (4, 5, 5), (4, 6, 4), (4, 7, 9),
    (5, 6, 3), (6, 8, 1), (7, 8, 6)
]
N = 8


def build_graph(n: int, edges: list):
    adj = {i: [] for i in range(1, n + 1)}
    matrix = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
        matrix[u - 1][v - 1] = w
        matrix[v - 1][u - 1] = w
    return adj, matrix


def dijkstra(adj: dict, start: int):
    dist = {v: INF for v in adj}
    pred = {v: -1 for v in adj}
    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                pred[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, pred


def reconstruct_path(pred: dict, start: int, target: int) -> str:
    path = []
    curr = target
    while curr != -1:
        path.append(str(curr))
        if curr == start:
            break
        curr = pred[curr]
    return " -> ".join(reversed(path))


def floyd_warshall(weight_matrix: list):
    n = len(weight_matrix)
    dist = [row[:] for row in weight_matrix]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


if __name__ == "__main__":
    adj_list, w_matrix = build_graph(N, EDGES)

    dijkstra_dist, dijkstra_pred = dijkstra(adj_list, 1)
    print("1. РЕЗУЛЬТАТИ АЛГОРИТМУ ДЕЙКСТРИ (СТАРТОВА ВЕРШИНА = 1)")
    print(f"{'Вершина':<10} | {'Вага':<8} | {'Найкоротший шлях'}")
    print("-" * 45)
    for v in range(2, N + 1):
        print(f"{v:<10} | {dijkstra_dist[v]:<8} | {reconstruct_path(dijkstra_pred, 1, v)}")

    floyd_matrix = floyd_warshall(w_matrix)
    print("\n2. МАТРИЦЯ НАЙКОРОТШИХ ВІДСТАНЕЙ ФЛОЙДА D^(8)")
    header = "     " + "".join(f"{j:>4}" for j in range(1, N + 1))
    print(header)
    print("-" * len(header))
    for i in range(N):
        row_str = "".join(f"{int(val):>4}" if val != INF else "   ∞" for val in floyd_matrix[i])
        print(f"{i + 1:>2} | {row_str}")

    dijkstra_row = [dijkstra_dist[v] for v in range(1, N + 1)]
    floyd_row_1 = [int(x) for x in floyd_matrix[0]]
    assert dijkstra_row == floyd_row_1
    print("\n3. ПЕРЕВІРКА ЗБІГУ РЕЗУЛЬТАТІВ:")
    print(f"Дейкстра (від 1): {dijkstra_row}")
    print(f"Флойд (рядок 1):  {floyd_row_1}")
    print("Висновок перевірки: результати ручної та програмної побудови повністю збігаються.")
