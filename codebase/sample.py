"""
Sample Codebase for AI Interview + Code Assistant

Includes:
- LRU Cache implementation
- Binary Search
- Graph BFS
- REST API simulation
- Basic ML utility
"""

from collections import OrderedDict
from typing import List, Dict
import math


class LRUCache:
    """
    LRU Cache implementation using OrderedDict.
    Time Complexity:
        get: O(1)
        put: O(1)
    """

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def binary_search(arr: List[int], target: int) -> int:
    """
    Iterative binary search.
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Breadth First Search traversal.
    Time Complexity: O(V + E)
    """
    visited = set()
    queue = [start]
    order = []

    while queue:
        node = queue.pop(0)

        if node not in visited:
            visited.add(node)
            order.append(node)
            queue.extend(graph.get(node, []))

    return order


def compute_mse(y_true: List[float], y_pred: List[float]) -> float:
    """
    Mean Squared Error computation.
    Time Complexity: O(n)
    """
    if len(y_true) != len(y_pred):
        raise ValueError("Input lengths must match.")

    return sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)


class SimpleModel:
    """
    Simple linear regression model using gradient descent.
    """

    def __init__(self, lr: float = 0.01, epochs: int = 100):
        self.lr = lr
        self.epochs = epochs
        self.weight = 0
        self.bias = 0

    def fit(self, X: List[float], y: List[float]):
        n = len(X)

        for _ in range(self.epochs):
            y_pred = [self.weight * x + self.bias for x in X]

            dw = (-2 / n) * sum(x * (yi - ypi) for x, yi, ypi in zip(X, y, y_pred))
            db = (-2 / n) * sum(yi - ypi for yi, ypi in zip(y, y_pred))

            self.weight -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X: List[float]) -> List[float]:
        return [self.weight * x + self.bias for x in X]


def factorial(n: int) -> int:
    """
    Recursive factorial.
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n == 0:
        return 1
    return n * factorial(n - 1)
