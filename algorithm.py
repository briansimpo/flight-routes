from collections import defaultdict


class Graph:
    def __init__(self, airports):
        """
        Initialize the graph with a given set of airports.

        Args:
            airports (dict): A dictionary where keys are airport codes 
                             and values are unique indices for each airport.
        """
        self.airports = airports  # Dictionary of airports
        self.vertices = len(airports)  # Automatically handle the number of vertices
        self.graph = defaultdict(list)  # Adjacency list
    
    def add_edge(self, from_airport, to_airport):
        """
        Add a directed edge from one airport to another.

        Args:
            from_airport (str): The starting airport code.
            to_airport (str): The destination airport code.
        """
        self.graph[from_airport].append(to_airport)
    
    def add_routes(self, routes):
        """
        Add multiple directed routes (bulk routes) to the graph.

        Args:
            routes (list of tuple): A list of tuples where each tuple 
                                    contains a pair of airport codes (from, to).
        """
        for from_airport, to_airport in routes:
            self.add_edge(self.airports[from_airport], self.airports[to_airport])  # Use airport dict to get vertex index
    
    def _depth_first_search(self, vertex, visited, stack):
        """
        Perform a depth-first search to determine the finish order of vertices.

        Args:
            vertex (int): The current vertex index.
            visited (list): A list to track visited vertices.
            stack (list): A stack to store the finish order of vertices.
        """
        visited[vertex] = True
        for neighbor in self.graph[vertex]:
            if not visited[neighbor]:
                self._depth_first_search(neighbor, visited, stack)
        stack.append(vertex)
    
    def _transpose_graph(self):
        """
        Reverse the graph (transpose).

        Returns:
            Graph: A new graph instance representing the transposed graph.
        """
        transposed_graph = Graph(self.airports)  # Pass the airports dict
        for from_airport in self.graph:
            for to_airport in self.graph[from_airport]:
                transposed_graph.add_edge(to_airport, from_airport)
        return transposed_graph
    
    def _depth_first_search_transposed(self, vertex, visited, component):
        """
        Perform a depth-first search on the transposed graph to find strongly connected components.

        Args:
            vertex (int): The current vertex index.
            visited (list): A list to track visited vertices.
            component (list): A list to store the current strongly connected component.
        """
        visited[vertex] = True
        component.append(vertex)
        for neighbor in self.graph[vertex]:
            if not visited[neighbor]:
                self._depth_first_search_transposed(neighbor, visited, component)
    
    def find_strongly_connected_components(self):
        """
        Find all strongly connected components (SCCs) in the graph.

        Returns:
            list: A list of strongly connected components, where each component 
                  is represented as a list of vertices (airport indices).
        """
        stack = []
        visited = [False] * self.vertices
        
        # First DFS pass to fill the stack with finish times
        for i in range(self.vertices):
            if not visited[i]:
                self._depth_first_search(i, visited, stack)
        
        # Get the transposed graph
        transposed_graph = self._transpose_graph()
        
        # Reset visited array for the second pass
        visited = [False] * self.vertices
        sccs = []  # List of all SCCs
        
        # Process all vertices in the order of decreasing finish times
        while stack:
            vertex = stack.pop()
            if not visited[vertex]:
                component = []
                transposed_graph._depth_first_search_transposed(vertex, visited, component)
                sccs.append(component)
        
        return sccs
    
    def build_compressed_graph_from_sccs(self, sccs):
        """
        Build a compressed graph from strongly connected components (SCCs).

        Args:
            sccs (list): A list of strongly connected components.

        Returns:
            defaultdict: A dictionary representing the compressed graph,
                         where keys are SCC indices and values are sets of connected SCC indices.
        """
        scc_map = {}
        for idx, scc in enumerate(sccs):
            for airport in scc:
                scc_map[airport] = idx
        
        compressed_graph = defaultdict(set)
        
        for from_airport in self.graph:
            for to_airport in self.graph[from_airport]:
                if scc_map[from_airport] != scc_map[to_airport]:  # Only add routes between different SCCs
                    compressed_graph[scc_map[from_airport]].add(scc_map[to_airport])
        
        return compressed_graph
    
    def calculate_routes_needed(self, compressed_graph, start_scc):
        """
        Calculate the number of additional routes needed to connect the graph.

        Args:
            compressed_graph (defaultdict): The compressed graph representation.
            start_scc (int): The index of the starting strongly connected component.

        Returns:
            int: The number of additional routes needed.
        """
        in_degree = defaultdict(int)

        # Calculate in-degrees
        for u in compressed_graph:
            for v in compressed_graph[u]:
                in_degree[v] += 1

        # Count nodes with in-degree = 0 excluding the start_scc
        zero_in_degree_count = 0
        for node in range(len(compressed_graph)):
            if node != start_scc and in_degree[node] == 0:
                zero_in_degree_count += 1

        return zero_in_degree_count

    def find_minimum_additional_routes(self, start_airport):
        """
        Find the minimum number of additional routes needed from a given airport.

        Args:
            start_airport (str): The airport code to start from.

        Returns:
            int: The minimum number of additional routes needed to connect the graph.
        """
        # Step 1: Find Strongly Connected Components (SCCs)
        sccs = self.find_strongly_connected_components()
        
        # Step 2: Build compressed graph from SCCs
        compressed_graph = self.build_compressed_graph_from_sccs(sccs)
        
        # Step 3: Determine the starting SCC
        start_scc = next(i for i, scc in enumerate(sccs) if self.airports[start_airport] in scc)
        
        # Step 4: Calculate additional routes needed
        additional_routes_needed = self.calculate_routes_needed(compressed_graph, start_scc)
        
        return additional_routes_needed
