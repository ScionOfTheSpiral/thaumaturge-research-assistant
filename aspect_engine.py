from collections import defaultdict, deque

class AspectLibrary:
    def __init__(self, aspect_data):
        self.primal_aspects = set(
            aspect_data["primal_aspects"]
        )
        self.combinations = dict(
            aspect_data["combinations"]
        )
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = defaultdict(set)

        for aspect in self.primal_aspects:
            graph[aspect]

        for compound, ingredients in self.combinations.items():
            for ingredient in ingredients:
                graph[compound].add(ingredient)
                graph[ingredient].add(compound)
    
        return dict(graph)

    def _connected(self, start, target):
        seen, stack = {start}, [start]
        while stack: 
            node = stack.pop()
            if node == target: 
                return True
            for n in self.graph[node]:
                if n not in seen:
                    seen.add(n)
                    stack.append(n)
        return False

    def ingredients(self, aspect):
        return self.combinations.get(aspect)

    def neighbors(self, aspect):
        return self.graph.get(aspect, set())

    def all_aspects(self):
        return self.primal_aspects | set(self.combinations)

    def pathfinding(self, start, target, min_spaces=3):
        if min_spaces < 0:
            raise ValueError("min_spaces must be a non-negative")
        if start not in self.graph or target not in self.graph:
            return None

        # Remove the Core Aspects
        min_edges = min_spaces + 1
        max_edges = min_edges + 2 * len(self.graph)

        # Fast exit if elements are not connected
        if not self._connected(start, target):
            return None

        # Search (aspect, distance)
        queue = deque([(start, [start])])
        visited = {(start, 0)}

        while queue:
            current, path = queue.popleft()
            edges = len(path) - 1

            if current == target and edges >= min_edges:
                return path
            if edges >= max_edges:
                continue 

            for neighbor in sorted(self.graph[current]):
                state = (neighbor, edges + 1)
                if state not in visited:
                    visited.add(state)
                    queue.append((neighbor, path + [neighbor]))

        return None