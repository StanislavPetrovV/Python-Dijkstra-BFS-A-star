import pygame as pg
from heapq import *


def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]


cols, rows = 23, 13
TILE = 70

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# grid
grid = ['22222222222222222222212',
        '22222292222911112244412',
        '22444422211112911444412',
        '24444444212777771444912',
        '24444444219777771244112',
        '92444444212777791192144',
        '22229444212777779111144',
        '11111112212777772771122',
        '27722211112777772771244',
        '27722777712222772221244',
        '22292777711144429221244',
        '22922777222144422211944',
        '22222777229111111119222']
grid = [[int(char) for char in string ] for string in grid]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = (0, 7)
goal = (22, 7)
queue = []
heappush(queue, (0, start))
cost_visited = {start: 0}
visited = {start: None}

bg = pg.image.load('img/2.png').convert()
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))

while True:
    # fill screen
    sc.blit(bg, (0, 0))
    # draw BFS work
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y), 1) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(*xy)) for _, xy in queue]
    pg.draw.circle(sc, pg.Color('purple'), *get_circle(*goal))

    # Dijkstra logic
    if queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            queue = []
            continue

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            neigh_cost, neigh_node = next_node
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                heappush(queue, (new_cost, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node

    # draw path
    path_head, path_segment = cur_node, cur_node
    while path_segment:
        pg.draw.circle(sc, pg.Color('brown'), *get_circle(*path_segment))
        path_segment = visited[path_segment]
    pg.draw.circle(sc, pg.Color('blue'), *get_circle(*start))
    pg.draw.circle(sc, pg.Color('magenta'), *get_circle(*path_head))
    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(7)