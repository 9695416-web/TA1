class DisjointSetUnion:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1
            return True
        return False


def kruskal(vertices, edges):
    sorted_edges = sorted(edges, key=lambda x: x[2])
    dsu = DisjointSetUnion(vertices)
    mst = []
    total_cost = 0

    print("Покроковий хід алгоритму Крускала")
    step = 1
    for u, v, w in sorted_edges:
        if dsu.find(u) != dsu.find(v):
            dsu.union(u, v)
            mst.append((u, v, w))
            total_cost += w
            print(f"Крок {step}: Ребро ({u}, {v}) вагою {w} -> Додано до МКД")
            if len(mst) == len(vertices) - 1:
                break
        else:
            print(f"Крок {step}: Ребро ({u}, {v}) вагою {w} -> Пропущено (утворює цикл)")
        step += 1

    return mst, total_cost


def prim(vertices, edges, start_vertex=1):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = {start_vertex}
    mst = []
    total_cost = 0

    print("\nПокроковий хід алгоритму Пріма")
    step = 1
    while len(visited) < len(vertices):
        min_edge = None
        min_weight = float('inf')

        for u in visited:
            for v, w in adj[u]:
                if v not in visited and w < min_weight:
                    min_weight = w
                    min_edge = (u, v, w)

        if min_edge:
            u, v, w = min_edge
            visited.add(v)
            mst.append((u, v, w))
            total_cost += w
            print(f"Крок {step}: Приєднано вершину {v} через ребро ({u}, {v}) з вагою {w}")
            step += 1

    return mst, total_cost


if __name__ == "__main__":
    V = [1, 2, 3, 4, 5, 6, 7, 8]
    E = [
        (1, 4, 1),
        (6, 8, 1),
        (1, 2, 2),
        (3, 5, 2),
        (2, 4, 3),
        (5, 6, 3),
        (3, 6, 4),
        (3, 7, 4),
        (4, 6, 4),
        (1, 3, 5),
        (4, 5, 5),
        (7, 8, 6),
        (1, 7, 7),
        (4, 7, 9)
    ]

    mst_kruskal, cost_kruskal = kruskal(V, E)
    mst_prim, cost_prim = prim(V, E, start_vertex=1)

    print("\n")
    print("Результат:")
    print(f"Вага МКД (Крускал): {cost_kruskal}")
    print("Ребра МКД (Крускал):", mst_kruskal)
    print(f"Вага МКД (Прім): {cost_prim}")
    print("Ребра МКД (Прім):", mst_prim)
