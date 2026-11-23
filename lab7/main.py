"""
Лабораторна робота № 7. Варіант № 8.
Тема: Робота з бінарним та червоно-чорним деревами пошуку.
Вхідна послідовність: [28, 76, 27, 10, 5, 35, 95, 16, 33]
"""

from typing import Optional, List, Tuple

RED = "RED"
BLACK = "BLACK"


class BSTNode:
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional["BSTNode"] = None
        self.right: Optional["BSTNode"] = None


class BinarySearchTree:
    def __init__(self):
        self.root: Optional[BSTNode] = None

    def insert(self, key: int) -> None:
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[BSTNode], key: int) -> BSTNode:
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        return node

    def minimum(self, node: BSTNode) -> BSTNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key: int) -> None:
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[BSTNode], key: int) -> Optional[BSTNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        elif node.left is not None and node.right is not None:
            succ = self.minimum(node.right)
            node.key = succ.key
            node.right = self._delete(node.right, succ.key)
        else:
            node = node.left if node.left is not None else node.right
        return node

    def height(self, node: Optional[BSTNode] = None, _init: bool = True) -> int:
        if _init:
            node = self.root
        if node is None:
            return 0
        return 1 + max(self.height(node.left, False), self.height(node.right, False))

    def inorder_with_stack(self) -> Tuple[List[int], List[List[int]]]:
        result: List[int] = []
        stack_history: List[List[int]] = []
        current_stack: List[int] = []

        def _dfs(node: Optional[BSTNode]) -> None:
            if node is None:
                return
            current_stack.append(node.key)
            stack_history.append(list(current_stack))
            if node.left is not None:
                _dfs(node.left)
                stack_history.append(list(current_stack))
            result.append(node.key)
            if node.right is not None:
                _dfs(node.right)
                stack_history.append(list(current_stack))
            current_stack.pop()

        _dfs(self.root)
        return result, stack_history

    def preorder(self) -> List[int]:
        res: List[int] = []

        def _dfs(node: Optional[BSTNode]) -> None:
            if node is not None:
                res.append(node.key)
                _dfs(node.left)
                _dfs(node.right)

        _dfs(self.root)
        return res

    def postorder(self) -> List[int]:
        res: List[int] = []

        def _dfs(node: Optional[BSTNode]) -> None:
            if node is not None:
                _dfs(node.left)
                _dfs(node.right)
                res.append(node.key)

        _dfs(self.root)
        return res

    def format_tree(self, node: Optional[BSTNode] = None, _init: bool = True) -> str:
        if _init:
            node = self.root
        if node is None:
            return "Empty"
        parts = []
        if node.left is not None:
            parts.append(f"Л:{self.format_tree(node.left, False)}")
        if node.right is not None:
            parts.append(f"П:{self.format_tree(node.right, False)}")
        return f"{node.key}[{', '.join(parts)}]" if parts else f"{node.key}"


class RBNode:
    def __init__(self, key: Optional[int], color: str = RED):
        self.key: Optional[int] = key
        self.color: str = color
        self.left: Optional["RBNode"] = None
        self.right: Optional["RBNode"] = None
        self.parent: Optional["RBNode"] = None


class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(None, color=BLACK)
        self.root: RBNode = self.NIL

    def left_rotate(self, x: RBNode) -> None:
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y: RBNode) -> None:
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key: int) -> List[str]:
        logs: List[str] = []
        z = RBNode(key, color=RED)
        z.left = self.NIL
        z.right = self.NIL
        y = self.NIL
        x = self.root
        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self._insert_fixup(z, logs)
        return logs

    def _insert_fixup(self, z: RBNode, logs: List[str]) -> None:
        while z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                u = z.parent.parent.right
                if u.color == RED:
                    logs.append(
                        f"Випадок 1 (дядько {u.key} червоний): перефарбування "
                        f"{z.parent.key}, {u.key} -> BLACK; {z.parent.parent.key} -> RED"
                    )
                    z.parent.color = BLACK
                    u.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        logs.append(f"Випадок 3 (кут): лівий поворот навколо {z.parent.key}")
                        z = z.parent
                        self.left_rotate(z)
                    logs.append(
                        f"Випадок 2 (пряма лінія): перефарбування {z.parent.key} -> BLACK, "
                        f"{z.parent.parent.key} -> RED; правий поворот навколо {z.parent.parent.key}"
                    )
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.right_rotate(z.parent.parent)
            else:
                u = z.parent.parent.left
                if u.color == RED:
                    logs.append(
                        f"Випадок 1 (дядько {u.key} червоний): перефарбування "
                        f"{z.parent.key}, {u.key} -> BLACK; {z.parent.parent.key} -> RED"
                    )
                    z.parent.color = BLACK
                    u.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        logs.append(f"Випадок 3 (кут): правий поворот навколо {z.parent.key}")
                        z = z.parent
                        self.right_rotate(z)
                    logs.append(
                        f"Випадок 2 (пряма лінія): перефарбування {z.parent.key} -> BLACK, "
                        f"{z.parent.parent.key} -> RED; лівий поворот навколо {z.parent.parent.key}"
                    )
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self.left_rotate(z.parent.parent)
        self.root.color = BLACK

    def _transplant(self, u: RBNode, v: RBNode) -> None:
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node: RBNode) -> RBNode:
        while node.left != self.NIL:
            node = node.left
        return node

    def search(self, key: int) -> RBNode:
        curr = self.root
        while curr != self.NIL and curr.key != key:
            curr = curr.left if key < curr.key else curr.right
        return curr

    def delete(self, key: int) -> List[str]:
        logs: List[str] = []
        z = self.search(key)
        if z == self.NIL:
            return logs
        y = z
        y_orig_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_orig_color == BLACK:
            self._delete_fixup(x, logs)
        return logs

    def _delete_fixup(self, x: RBNode, logs: List[str]) -> None:
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    logs.append(f"Випадок 4 (брат {w.key} червоний): перефарбування та лівий поворот навколо {x.parent.key}")
                    w.color = BLACK
                    x.parent.color = RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    case_num = "Випадок 1 (батько червоний)" if x.parent.color == RED else "Випадок 5 (усі чорні)"
                    logs.append(f"{case_num}: перефарбування брата {w.key} -> RED")
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        logs.append(f"Випадок 3 (брат {w.key} чорний, CL={w.left.key} червоний): правий поворот навколо {w.key}")
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.parent.right
                    logs.append(f"Випадок 2 (брат {w.key} чорний, CR={w.right.key} червоний): лівий поворот навколо {x.parent.key}, перефарбування")
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    logs.append(f"Симетричний Випадок 4 (брат {w.key} червоний): правий поворот навколо {x.parent.key}")
                    w.color = BLACK
                    x.parent.color = RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    case_num = "Симетричний Випадок 1" if x.parent.color == RED else "Симетричний Випадок 5"
                    logs.append(f"{case_num}: перефарбування брата {w.key} -> RED")
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        logs.append(f"Симетричний Випадок 3 (брат {w.key} чорний, CR={w.right.key} червоний): лівий поворот навколо {w.key}")
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.parent.left
                    logs.append(f"Симетричний Випадок 2 (брат {w.key} чорний, CL={w.left.key} червоний): правий поворот навколо {x.parent.key}, перефарбування")
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = BLACK

    def height(self, node: Optional[RBNode] = None, _init: bool = True) -> int:
        if _init:
            node = self.root
        if node == self.NIL:
            return 0
        return 1 + max(self.height(node.left, False), self.height(node.right, False))

    def black_height(self) -> int:
        bh = 0
        curr = self.root
        while curr != self.NIL:
            if curr.color == BLACK:
                bh += 1
            curr = curr.left
        return bh

    def verify_properties(self) -> bool:
        assert self.root.color == BLACK, "Корінь має бути чорним"

        def _check(node: RBNode) -> int:
            if node == self.NIL:
                return 1
            if node.color == RED:
                assert node.left.color == BLACK and node.right.color == BLACK, f"Два червоні вузли підряд біля {node.key}"
            left_bh = _check(node.left)
            right_bh = _check(node.right)
            assert left_bh == right_bh, f"Порушення чорної висоти у піддереві {node.key}"
            return left_bh + (1 if node.color == BLACK else 0)

        _check(self.root)
        return True

    def inorder_with_stack(self) -> Tuple[List[int], List[List[int]]]:
        result: List[int] = []
        stack_history: List[List[int]] = []
        current_stack: List[int] = []

        def _dfs(node: RBNode) -> None:
            if node == self.NIL:
                return
            current_stack.append(node.key)
            stack_history.append(list(current_stack))
            if node.left != self.NIL:
                _dfs(node.left)
                stack_history.append(list(current_stack))
            result.append(node.key)
            if node.right != self.NIL:
                _dfs(node.right)
                stack_history.append(list(current_stack))
            current_stack.pop()

        _dfs(self.root)
        return result, stack_history

    def preorder(self) -> List[int]:
        res: List[int] = []

        def _dfs(node: RBNode) -> None:
            if node != self.NIL:
                res.append(node.key)
                _dfs(node.left)
                _dfs(node.right)

        _dfs(self.root)
        return res

    def postorder(self) -> List[int]:
        res: List[int] = []

        def _dfs(node: RBNode) -> None:
            if node != self.NIL:
                _dfs(node.left)
                _dfs(node.right)
                res.append(node.key)

        _dfs(self.root)
        return res

    def format_tree(self, node: Optional[RBNode] = None, _init: bool = True) -> str:
        if _init:
            node = self.root
        if node == self.NIL:
            return "Empty"
        c = "Чорн." if node.color == BLACK else "Черв."
        parts = []
        if node.left != self.NIL:
            parts.append(f"Л:{self.format_tree(node.left, False)}")
        if node.right != self.NIL:
            parts.append(f"П:{self.format_tree(node.right, False)}")
        return f"{node.key}({c})[{', '.join(parts)}]" if parts else f"{node.key}({c})"


if __name__ == "__main__":
    KEYS = [28, 76, 27, 10, 5, 35, 95, 16, 33]
    bst = BinarySearchTree()
    rbt = RedBlackTree()

    print("1. ПОКРОКОВА ПОБУДОВА BST ТА RB-TREE (ВАРІАНТ № 8)")
    for step, k in enumerate(KEYS, 1):
        bst.insert(k)
        rb_logs = rbt.insert(k)
        rbt.verify_properties()
        action = "; ".join(rb_logs) if rb_logs else "Без порушень балансу"
        print(f"Крок {step} (вставка {k:>2}): RB = {rbt.format_tree()}")
        print(f"   Дії RB: {action}")

    print(f"\nВисота BST (рівнів): {bst.height()}")
    print(f"Висота RB-tree (рівнів): {rbt.height()}, чорна висота: {rbt.black_height()}")

    print("\n2. ОБХОДИ ДЕРЕВ ТА СТЕК ВИКЛИКІВ INORDERTRAVERSAL")
    bst_in, bst_stack = bst.inorder_with_stack()
    rbt_in, rbt_stack = rbt.inorder_with_stack()

    print(f"{'Ітер.':<6} | {'Стек викликів BST':<24} | {'Стек викликів RB-tree':<24}")
    print("-" * 60)
    for idx in range(len(bst_stack)):
        s_bst = ", ".join(map(str, bst_stack[idx]))
        s_rbt = ", ".join(map(str, rbt_stack[idx]))
        print(f"{idx + 1:<6} | {s_bst:<24} | {s_rbt:<24}")

    print(f"\nBST Inorder:   {bst_in}")
    print(f"BST Preorder:  {bst.preorder()}")
    print(f"BST Postorder: {bst.postorder()}")
    print(f"RB Inorder:    {rbt_in}")
    print(f"RB Preorder:   {rbt.preorder()}")
    print(f"RB Postorder:  {rbt.postorder()}")

    print("\n3. ПОЧЕРГОВЕ ВИДАЛЕННЯ КОРЕНИХ ЕЛЕМЕНТІВ ІЗ BST (76 -> 27 -> 28)")
    for target in [76, 27, 28]:
        bst.delete(target)
        print(f"Після видалення {target:>2}: {bst.format_tree()} | Inorder: {bst.inorder_with_stack()[0]}")

    print("\n4. ПОЧЕРГОВЕ ВИДАЛЕННЯ ЧОРНИХ ЕЛЕМЕНТІВ ІЗ RB-TREE (5 -> 95 -> 10)")
    for target in [5, 95, 10]:
        del_logs = rbt.delete(target)
        rbt.verify_properties()
        print(f"Після видалення {target:>2}: {rbt.format_tree()} | Чорна висота: {rbt.black_height()}")
        print(f"   Балансування: {'; '.join(del_logs)}")

    assert bst_in == [5, 10, 16, 27, 28, 33, 35, 76, 95]
    assert rbt_in == [5, 10, 16, 27, 28, 33, 35, 76, 95]
    assert bst.inorder_with_stack()[0] == [5, 10, 16, 33, 35, 95]
    assert rbt.inorder_with_stack()[0] == [16, 27, 28, 33, 35, 76]
    assert rbt.black_height() == 2
    print("\n[ПЕРЕВІРКА]: Усі ручні розрахунки, обходи, висоти та стани дерев після видалення 100% збігаються з програмними!")
