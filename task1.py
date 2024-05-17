# Created by vanyamel. 10/05/2024

class Chain:
    def __init__(self, points):
        self.points = sorted(points, key=lambda p: p[1])

    def __getitem__(self, idx):
        return self.points[idx]

    def __len__(self):
        return len(self.points)

def point_left_of_segment(p, seg):
    (x, y) = p
    ((x1, y1), (x2, y2)) = seg
    return (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) > 0

def locate_point_in_chain(chain, point):
    low, high = 0, len(chain) - 1
    while low < high:
        mid = (low + high) // 2
        if chain[mid][1] <= point[1] <= chain[mid + 1][1]:
            return mid
        elif point[1] < chain[mid][1]:
            high = mid
        else:
            low = mid + 1
    return low

def locate_point(chains, point):
    x, y = point
    low, high = 0, len(chains) - 1
    while low < high:
        mid = (low + high) // 2
        chain = chains[mid]
        if chain[0][0] <= x <= chain[-1][0]:
            chain_idx = mid
            segment_idx = locate_point_in_chain(chains[chain_idx], point)
            seg = (chains[chain_idx][segment_idx], chains[chain_idx][segment_idx + 1])
            if point_left_of_segment(point, seg):
                high = mid
            else:
                low = mid + 1
        elif x < chain[0][0]:
            high = mid
        else:
            low = mid + 1
    return low, locate_point_in_chain(chains[low], point)

chains = [
    Chain([(1, 1), (1, 3), (1, 5)]),
    Chain([(3, 1), (3, 3), (3, 5)]),
    Chain([(5, 1), (5, 3), (5, 5)]),
]

point = (10, 20)
chain_idx, segment_idx = locate_point(chains, point)
print(f"Point {point} is in chain {chain_idx} at segment {segment_idx}.")
