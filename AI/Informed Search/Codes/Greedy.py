tree = {
    "A": [("B", 2), ("C", 5)], #estimated cost to reach the goal
    "B": [("D", 3), ("E", 4)],
    "C": [("F", 1), ("G", 6)],
    "D": [("Goal", 0)],
    "E": [],
    "F": [("Goal", 0)], # h(goal) always 0
    "G": [],
    "Goal": [] }

def greedy(grid):
    node = "A"
    cost_A = 10
    goal_node = "Goal"
    frontier = [(node,cost_A)]
    print(frontier)
    explored = set()

    total_cost = cost_A
    while True:
        if len(frontier) == 0:
            return print("Search Failed!")
        frontier.sort(key = lambda x: x[1]) # sort by cost
        node, parent_cost = frontier.pop(0) # pop lowest estimated cost first
        if node == goal_node:
            return print("Solution found:", node)
        explored.add(node) # do not assign it back to explored or you get None

        frontier_nodes = [node for node,cost in frontier]
        for child,child_cost in tree[node]:
            if child not in explored and child not in frontier_nodes:
                frontier.append((child,child_cost))
                
        print(frontier)
greedy(tree)

