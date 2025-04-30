import heapq

class Node:
    """A node class for Dijkstra Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = float('inf')  # distance from start node

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.g < other.g

def dijkstra(maze, start, end):
    """Returns the shortest path from start to end using Dijkstra's algorithm"""
    
    # Create start and end nodes
    start_node = Node(None, start)
    start_node.g = 0
    end_node = Node(None, end)

    # Initialize both open list and closed list
    open_list = []
    closed_list = []

    # Heapify the open list and add the start node
    heapq.heappush(open_list, start_node)

    # Adjacent squares (movement directions)
    adjacent_squares = ((0, 1), (0, -1), (1, 0), (-1, 0))

    # Loop until you find the end
    while open_list:
        # Pop the node with the smallest distance
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []
        for new_position in adjacent_squares:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range and walkable terrain
            if (0 <= node_position[0] < len(maze)) and (0 <= node_position[1] < len(maze[0])):
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Calculate the G cost
            tentative_g_cost = current_node.g + 1

            # Child is already in the open list
            if add_to_open(open_list, child):
                # Check if this path is better than the one already found
                if tentative_g_cost < child.g:
                    child.g = tentative_g_cost
                    child.parent = current_node
                    heapq.heappush(open_list, child)
            else:
                child.g = tentative_g_cost
                child.parent = current_node
                heapq.heappush(open_list, child)

    return None

def return_path(current_node):
    """ Returns the path from the start node to the current_node"""
    path = []
    current = current_node
    while current:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path

def add_to_open(open_list, child):
    for node in open_list:
        if child == node:
            return True
    return False

# Define a 5x5 maze
maze = [[0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0]]

start = (0, 0)
end = (4, 4)

path = dijkstra(maze, start, end)
print(path)
