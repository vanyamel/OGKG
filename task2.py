# Created by vanyamel. 10/05/2024

import matplotlib.pyplot as plt

class RangeTree:
    def __init__(self, points):
        points = sorted(points, key=lambda point: point[0])
        self.root = self.build_tree(points)

    class Node:
        def __init__(self, points):
            self.points = sorted(points, key=lambda point: point[1])
            self.left = None
            self.right = None
            self.mid = None

    def build_tree(self, points):
        if not points:
            return None
        mid = len(points) // 2
        node = self.Node(points)
        node.mid = points[mid]
        node.left = self.build_tree(points[:mid])
        node.right = self.build_tree(points[mid+1:])
        return node

    def query(self, x1, x2, y1, y2):
        def range_query(node, x1, x2, y1, y2):
            if not node:
                return []
            results = []
            if x1 <= node.mid[0] <= x2 and y1 <= node.mid[1] <= y2:
                results.append(node.mid)
            if x1 <= node.mid[0]:
                results += range_query(node.left, x1, x2, y1, y2)
            if node.mid[0] <= x2:
                results += range_query(node.right, x1, x2, y1, y2)
            return results

        return range_query(self.root, x1, x2, y1, y2)

    def visualize(self, query_range=None):
        def plot_tree(node, ax, xlim, depth=0):
            if not node:
                return
            x, y = node.mid
            ax.plot(x, y, 'bo')
            if query_range and query_range[0] <= x <= query_range[1] and query_range[2] <= y <= query_range[3]:
                ax.plot(x, y, 'ro')
            if node.left:
                plot_tree(node.left, ax, (xlim[0], x), depth + 1)
            if node.right:
                plot_tree(node.right, ax, (x, xlim[1]), depth + 1)

        fig, ax = plt.subplots()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        if query_range:
            x1, x2, y1, y2 = query_range
            rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, edgecolor='r', facecolor='none', linestyle='--')
            ax.add_patch(rect)
        plot_tree(self.root, ax, (0, 10))
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Range Tree Visualization')
        plt.show()

points = [(2, 3), (4, 7), (5, 1), (6, 4), (7, 2), (8, 5),(5,4),(5,8)]
range_tree = RangeTree(points)
result = range_tree.query(1, 7, 2, 5)  #  [4, 7] x [2, 5]
print("Result of query:", result)
range_tree.visualize(query_range=(4, 7, 2, 5))
