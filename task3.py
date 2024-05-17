# Created by vanyamel. 10/05/2024
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest_pair(points):
    if len(points) <= 1:
        return float('inf'), None, None
    elif len(points) == 2:
        return distance(points[0], points[1]), points[0], points[1]
    points.sort()

    mid = len(points) // 2
    left_half = points[:mid]
    right_half = points[mid:]

    left_distance, left_point1, left_point2 = closest_pair(left_half)
    right_distance, right_point1, right_point2 = closest_pair(right_half)

    if left_distance < right_distance:
        min_distance = left_distance
        min_point1, min_point2 = left_point1, left_point2
    else:
        min_distance = right_distance
        min_point1, min_point2 = right_point1, right_point2

    mid_x = points[mid][0]
    strip = [point for point in points if abs(point[0] - mid_x) < min_distance]

    strip.sort(key=lambda x: x[1])

    for i in range(len(strip)):
        for j in range(i+1, len(strip)):
            if strip[j][1] - strip[i][1] >= min_distance:
                break
            d = distance(strip[i], strip[j])
            if d < min_distance:
                min_distance = d
                min_point1, min_point2 = strip[i], strip[j]

    return min_distance, min_point1, min_point2

points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4), ()]
min_dist, point1, point2 = closest_pair(points)
print("Найближча пара точок:", point1, point2)
print("Відстань між ними:", min_dist)
