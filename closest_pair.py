import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.ion()


def gather_points_manually():
    f = plt.figure()
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.grid()
    points = plt.ginput(-1)
    plt.close(f)
    return np.array(points)

def gather_points_random():
    return np.random.uniform(-1, 1, size=(30, 2))


def dist(points):
    if points.shape[0] == 1:
        return np.inf
    return np.sqrt(((points[0] - points[1])**2).sum())

def plot(solution_data):
    ax = solution_data['figure'].axes[0]
    ax.set_aspect('equal')
    ax.clear()
    ax.axvline(solution_data['median_line'], ls='--')
    d = solution_data['d']
    if d != 0:
        rect = patches.Rectangle((solution_data['median_line']-d,-1),
                                 2*d, 2,
                                 linewidth=0,facecolor='purple', alpha=0.5)
        ax.add_patch(rect)
    mi, ma = solution_data['min'], solution_data['max']
    rect2 = patches.Rectangle((mi,-1),
                             ma- mi, 2,
                             linewidth=0,facecolor='orange', alpha=0.5)
    ax.add_patch(rect2)
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.scatter(solution_data['points'][:, 0], solution_data['points'][:, 1], zorder=5)
    ax.grid()
    if solution_data['checking'] is not False:
        checking = solution_data['checking']
        best_s = solution_data['best_s']
        strip = solution_data['strip']
        ax.scatter(strip[:, 0], strip[:, 1], color='red', zorder=6)
        ax.scatter(checking[:, 0], checking[:, 1], color='green', zorder=7)
        plt.pause(1)
    else:
        plt.pause(1)

def solve(points, solution_data):
    n = len(points)
    if n <= 2:  # Base case
        return points
    else:
        mid_point = (n + 1)//2
        boundary = (points[mid_point - 1, 0] + points[mid_point, 0]) / 2
        solution_data['d'] = 0
        solution_data['median_line'] = boundary
        solution_data['min'] = points[0, 0]
        solution_data['max'] = points[-1, 0]
        solution_data['checking'] = False
        plot(solution_data)
        p1, p2 = points[:mid_point], points[mid_point:]
        s1 = solve(points[:mid_point], solution_data)
        s2 = solve(points[mid_point:], solution_data)
        d1, d2 = dist(s1), dist(s2)

        if d2 < d1:  # Ensure that s1 and d1 contain the best solutions
            s1, s2 = s2, s1
            d1, d2 = d2, d1
        d, s = d1, s1

        solution_data['d'] = d
        solution_data['median_line'] = boundary
        solution_data['min'] = points[0, 0]
        solution_data['max'] = points[-1, 0]
        solution_data['checking'] = False
        solution_data['best_s'] = s
        plot(solution_data)

        x_coords = points[:, 0]
        strip_start = np.searchsorted(x_coords, boundary - d, 'left')
        strip_end = np.searchsorted(x_coords, boundary + d, 'right')
        strip = points[strip_start:strip_end]
        solution_data['strip'] = strip
        print("checking a strip with", len(strip))
        y_order = np.argsort(strip[:, 1])

        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if strip[y_order[j], 1] - strip[y_order[i], 1] > d:
                    break
                solution_data['checking'] = np.array([strip[y_order[j]], strip[y_order[i]]])
                plot(solution_data)
                new_d = dist(np.array([strip[y_order[j]], strip[y_order[i]]]))
                if new_d < d:
                    d = new_d
                    s = np.array([strip[y_order[j]], strip[y_order[i]]])
        return s


points = gather_points_manually()
if len(points) == 0:
    points = gather_points_random()
x_order = np.argsort(points[:, 0])
sorted_x = points[x_order]
f = plt.figure()
plt.scatter(points[:, 0], points[:, 1])
plt.grid()
plt.waitforbuttonpress()
solution_data = {
    'points': points,
    'd': 0,
    'best_solution': None,
    'median_line': 0,
    'min': 0,
    'max': 0,
    'figure': f
}
solution = solve(sorted_x, solution_data)
plt.scatter(solution[:, 0], solution[:, 1])
plt.waitforbuttonpress()
