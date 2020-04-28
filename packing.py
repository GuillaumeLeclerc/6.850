from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--radius", "-r", type=float, default=0.1,
                    help="The radius of the circles")
parser.add_argument("--grid", "-g", type=float, default=0.5,
                    help="The width of the grid")
parser.add_argument("--random", action='store_true',
                    help="Chose 30 points at random instead of manual input")
args = parser.parse_args()


plt.ion()

R = args.radius
G = args.grid


def solve_local(points):
    pass

def setup_axes():
    ax = plt.gca()
    ax.xaxis.set_major_locator(MultipleLocator(G))
    ax.yaxis.set_major_locator(MultipleLocator(G))
    ax.set_aspect('equal')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid()

def gather_points_manually():
    f = plt.figure()
    setup_axes()
    points = plt.ginput(-1)
    plt.close(f)
    return np.array(points)

def gather_points_random():
    return np.random.uniform(-1, 1, size=(30, 2))


def dist(points):
    if points.shape[0] == 1:
        return np.inf
    return np.sqrt(((points[0] - points[1])**2).sum())

def plot_circles(points, statuses):
    plt.close()
    f = plt.figure()
    for point, status in zip(points, statuses):
        if status == 2:
            artist = plt.Circle(point, R, facecolor=(0, 1, 0, 0.7), edgecolor=(0, 0, 0, 1))
        else:
            alpha = 0.3 if status == 1 else 1
            artist = plt.Circle(point, R, facecolor=(1, 0, 0, 0.7*alpha), edgecolor=(0, 0, 0, alpha))
        plt.gca().add_artist(artist)
    setup_axes()

def is_hitting_grid(point):
    x_low, y_low = np.floor((point - R) / G).astype(int)
    x_high, y_high = np.floor((point + R) / G).astype(int)
    return x_low != x_high or y_low != y_high

def filter_points(points, statuses):
    for i, point in enumerate(points):
        if is_hitting_grid(point):
            statuses[i] = 1

def bucketize(points, statuses):
    buckets = defaultdict(list)
    for point, status in zip(points, statuses):
        if status == 0:
            center = np.floor(point / G).astype(int).astype(float) * G
            buckets[tuple(center)].append(point)
    return buckets


def brute_solve_recurse(taken, options, incompatibility_sets):
    results = []
    for option in options:
        results.append(brute_solve_recurse(taken | set([option]), options - incompatibility_sets[option], incompatibility_sets))
    return max(results, default=taken, key=len)


def brute_solve(points):
    distance_matrix = np.sqrt(((points[:, None] - points[None, :])**2).sum(2))
    incompatibilities = distance_matrix <= 2 * R
    incompatibility_sets = [set(list(np.nonzero(incompatibilities[i])[0])) for i in range(len(points))]
    left = set(range(len(points)))
    solution = brute_solve_recurse(set(), left, incompatibility_sets)
    return set(tuple(points[x]) for x in solution)

def update_status(points, solution, statuses):
    for i, point in enumerate(points):
        if tuple(point) in solution:
            statuses[i] = 2


if args.random:
    points = gather_points_random()
else:
    points = gather_points_manually()
statuses = np.zeros(len(points))
plot_circles(points, statuses)
plt.waitforbuttonpress()
filter_points(points, statuses)
plot_circles(points, statuses)
plt.waitforbuttonpress()
buckets = bucketize(points, statuses)
full_solution = set()
for bucket in buckets.values():
    local_solution = brute_solve(np.array(bucket))
    for s in local_solution:
        full_solution.add(s)
    local_statuses = np.copy(statuses)
    update_status(points, local_solution, local_statuses)
    plot_circles(points, local_statuses)
    plt.waitforbuttonpress()
update_status(points, full_solution, statuses)
plot_circles(points, statuses)
plt.waitforbuttonpress()
