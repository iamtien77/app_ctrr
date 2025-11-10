"""
Base Graph class and data structures
"""
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum

class GraphType(Enum):
    """Graph type enumeration"""
    DIRECTED = "directed"
    UNDIRECTED = "undirected"

class Graph:
    """
    Base Graph class supporting multiple representations
    """
    def __init__(self, graph_type: GraphType = GraphType.UNDIRECTED):
        """
        Initialize graph
        Args:
            graph_type: Type of graph (directed or undirected)
        """
        pass
        
    def add_vertex(self, vertex: int):
        """Add a vertex to the graph"""
        pass
        
    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """Add an edge to the graph"""
        pass
        
    def remove_vertex(self, vertex: int):
        """Remove a vertex from the graph"""
        pass
        
    def remove_edge(self, u: int, v: int):
        """Remove an edge from the graph"""
        pass
        
    def get_vertices(self) -> List[int]:
        """Get all vertices"""
        pass
        
    def get_edges(self) -> List[Tuple[int, int, float]]:
        """Get all edges"""
        pass
        
    def has_edge(self, u: int, v: int) -> bool:
        """Check if edge exists"""
        pass
        
    def get_neighbors(self, vertex: int) -> List[int]:
        """Get neighbors of a vertex"""
        pass

