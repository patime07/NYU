tree = {
    "A" : ["B", "C"],
    "B" : ["D", "E"],
    "C" : ["F", "G"],
    "D" : [],
    "E" : [],
    "F" : [],
    "G" : []
}

def bfs(grid):
    node = "A"
    goal_node = "G"
    if node == goal_node:
        return print("Solution found:", node)
    frontier = []
    frontier.append(node)
    explored = set()
    i = 0
    print(f'Step {i}:')
    print(f'Frontier: {frontier}')
    print(f'Explored Set: {explored}\n')

    while True:
        i += 1
        if len(frontier) == 0:
            print("Search Failed!")
        node = frontier.pop(0)
        explored.add(node) # do not assign it back to explored or you get None
        for child in tree[node]:
            if child not in explored and child not in frontier:
                if child == goal_node:
                    print(f'Step {i}:')
                    print(f'Frontier: {frontier}')
                    print(f'Explored Set: {explored}\n')

                    return print("Solution found:", child)

                frontier.append(child)
                
        print(f'Step {i}:')
        print(f'Frontier: {frontier}')
        print(f'Explored Set: {explored}\n')

bfs(tree)
