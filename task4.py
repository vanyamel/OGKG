# Created by vanyamel. 10/05/2024

import heapq
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SiteEvent:
    def __init__(self, point):
        self.point = point

    def __lt__(self, other):
        return self.point.y < other.point.y

class CircleEvent:
    def __init__(self, point, arc):
        self.point = point
        self.arc = arc

    def __lt__(self, other):
        return self.point.y < other.point.y

class Arc:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None

def fortune(points):
    events = [SiteEvent(point) for point in points]
    heapq.heapify(events)
    arc = None
    while events:
        event = heapq.heappop(events)
        if isinstance(event, SiteEvent):
            handle_site_event(event, arc, events)
        else:
            handle_circle_event(event, arc)

def handle_site_event(event, arc, events):
    new_arc = Arc(event.point)
    if arc is None:
        arc = new_arc
    else:
        prev_arc = None
        current_arc = arc
        while current_arc is not None and current_arc.point.x < event.point.x:
            prev_arc = current_arc
            current_arc = current_arc.right

        if prev_arc is None:
            arc.left = new_arc
        else:
            prev_arc.right = new_arc
            new_arc.left = prev_arc

        new_arc.right = current_arc
        if current_arc is not None:
            current_arc.left = new_arc

        if prev_arc is not None:
            check_circle_event(prev_arc, events)
        check_circle_event(new_arc, events)
        if current_arc is not None:
            check_circle_event(current_arc, events)

def check_circle_event(arc, events):
    if arc.left is None or arc.right is None:
        return
    if not is_valid_circle_event(arc):
        return
    # Calculate the circle event point
    circle_event_point = calculate_circle_event_point(arc)
    # Create a CircleEvent object
    circle_event = CircleEvent(circle_event_point, arc)
    # Add the circle event to the events list
    heapq.heappush(events, circle_event)

def is_valid_circle_event(arc):
    return arc.left is not None and arc.right is not None

def calculate_circle_event_point(arc):
    left = arc.left.point
    right = arc.right.point
    mid = arc.point

    x1, y1 = left.x, left.y
    x2, y2 = mid.x, mid.y
    x3, y3 = right.x, right.y

    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if d == 0:
        return None

    ux = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (y1 - y2)) / d
    uy = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (x2 - x1)) / d

    radius = math.sqrt((x1 - ux) ** 2 + (y1 - uy) ** 2)

    if uy + radius <= 0:
        return None

    return Point(ux, uy + radius)

def handle_circle_event(event, arc):
    if event.arc is None:
        return
    arc = event.arc
    if arc.left is not None:
        arc.left.right = arc.right
    if arc.right is not None:
        arc.right.left = arc.left
    if arc.left is not None and arc.right is not None:
        check_circle_event(arc.left)
        check_circle_event(arc.right)

np.random.seed(0)
points = np.random.rand(10, 2)

fortune([Point(p[0], p[1]) for p in points])

vor = Voronoi(points)
voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=2)
plt.plot(points[:,0], points[:,1], 'ro')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Вороного діаграма')
plt.axis('equal')
plt.show()
