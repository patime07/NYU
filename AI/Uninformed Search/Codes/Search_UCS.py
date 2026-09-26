tree = {
    "A": [("B", 2), ("C", 5)],
    "B": [("D", 3), ("E", 4)],
    "C": [("F", 1), ("G", 6)],
    "D": [("Goal", 2)],
    "E": [],
    "F": [("Goal", 1)],
    "G": [],
    "Goal": [] }

def ucs(grid):
    node = "A"
    cost_A = 0
    goal_node = "Goal"
    frontier = [(node,cost_A)]
    print(frontier)
    explored = set()

    total_cost = cost_A
    while True:
        if len(frontier) == 0:
            return print("Search Failed!")
        frontier.sort(key = lambda x: x[1]) # sort by cost
        node, parent_cost = frontier.pop(0) # pop lowest cost first
        if node == goal_node:
            return print("Solution found:", node)
        explored.add(node) # do not assign it back to explored or you get None

        frontier_nodes = [node for node,cost in frontier]
        for child,cost in tree[node]:
            child_cost = parent_cost + cost
            if child not in explored and child not in frontier_nodes:
                frontier.append((child,child_cost))
            elif child in frontier_nodes:
                for i, (frontier_node, frontier_cost) in enumerate(frontier):
                    if frontier_node == child and frontier_cost > child_cost:
                        frontier[i]= (child,child_cost)
        print(frontier)
ucs(tree)