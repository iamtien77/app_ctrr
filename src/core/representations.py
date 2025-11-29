"""
Các lớp biểu diễn đồ thị: Ma trận kề, Danh sách kề, Danh sách cạnh
"""
from typing import List, Dict, Tuple
from src.core.graph import Graph, GraphType
import numpy as np


class AdjacencyMatrix:
    """
    Biểu diễn đồ thị bằng ma trận kề
    Ma trận kề là một ma trận 2 chiều, trong đó:
    - matrix[i][j] = trọng số của cạnh từ đỉnh i đến đỉnh j
    - matrix[i][j] = 0 nếu không có cạnh
    """
    
    def __init__(self, graph: Graph):
        """
        Khởi tạo ma trận kề từ đồ thị
        Args:
            graph: Đồ thị cần chuyển đổi
        """
        self.graph = graph
        self.vertices = sorted(graph.get_vertices())
        self.vertex_to_index = {v: i for i, v in enumerate(self.vertices)}
        self.matrix = self._build_matrix()
    
    def _build_matrix(self) -> List[List[float]]:
        """
        Xây dựng ma trận kề từ đồ thị
        Returns:
            Ma trận kề dạng danh sách 2 chiều
        """
        n = len(self.vertices)
        # Khởi tạo ma trận với giá trị 0
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Điền trọng số vào ma trận
        for u, v, weight in self.graph.get_edges():
            i = self.vertex_to_index[u]
            j = self.vertex_to_index[v]
            matrix[i][j] = weight
            
            # Đồ thị vô hướng thì ma trận đối xứng
            if not self.graph.is_directed():
                matrix[j][i] = weight
        
        return matrix
    
    def to_adjacency_list(self) -> 'AdjacencyList':
        """
        Chuyển đổi sang biểu diễn danh sách kề
        Returns:
            Đối tượng AdjacencyList
        """
        return AdjacencyList(self.graph)
    
    def to_edge_list(self) -> 'EdgeList':
        """
        Chuyển đổi sang biểu diễn danh sách cạnh
        Returns:
            Đối tượng EdgeList
        """
        return EdgeList(self.graph)
    
    def get_matrix(self) -> List[List[float]]:
        """
        Lấy ma trận kề
        Returns:
            Ma trận kề
        """
        return self.matrix
    
    def print_matrix(self):
        """In ma trận kề ra màn hình"""
        print("Ma trận kề:")
        print("   ", end="")
        for v in self.vertices:
            print(f"{v:4}", end="")
        print()
        
        for i, v in enumerate(self.vertices):
            print(f"{v:3}", end="")
            for j in range(len(self.vertices)):
                print(f"{self.matrix[i][j]:4.0f}", end="")
            print()


class AdjacencyList:
    """
    Biểu diễn đồ thị bằng danh sách kề
    Danh sách kề là một dictionary, trong đó:
    - Key: Đỉnh
    - Value: Dictionary các đỉnh kề và trọng số {đỉnh_kề: trọng_số}
    """
    
    def __init__(self, graph: Graph):
        """
        Khởi tạo danh sách kề từ đồ thị
        Args:
            graph: Đồ thị cần chuyển đổi
        """
        self.graph = graph
        self.adj_list = graph.get_adjacency_list()
    
    def to_adjacency_matrix(self) -> AdjacencyMatrix:
        """
        Chuyển đổi sang biểu diễn ma trận kề
        Returns:
            Đối tượng AdjacencyMatrix
        """
        return AdjacencyMatrix(self.graph)
    
    def to_edge_list(self) -> 'EdgeList':
        """
        Chuyển đổi sang biểu diễn danh sách cạnh
        Returns:
            Đối tượng EdgeList
        """
        return EdgeList(self.graph)
    
    def get_list(self) -> Dict[int, Dict[int, float]]:
        """
        Lấy danh sách kề
        Returns:
            Danh sách kề
        """
        return self.adj_list
    
    def print_list(self):
        """In danh sách kề ra màn hình"""
        print("Danh sách kề:")
        for vertex in sorted(self.adj_list.keys()):
            neighbors = self.adj_list[vertex]
            print(f"Đỉnh {vertex}: ", end="")
            for neighbor, weight in neighbors.items():
                print(f"({neighbor}, {weight}) ", end="")
            print()


class EdgeList:
    """
    Biểu diễn đồ thị bằng danh sách cạnh
    Danh sách cạnh là một list các tuple:
    - Mỗi tuple: (đỉnh_u, đỉnh_v, trọng_số)
    """
    
    def __init__(self, graph: Graph):
        """
        Khởi tạo danh sách cạnh từ đồ thị
        Args:
            graph: Đồ thị cần chuyển đổi
        """
        self.graph = graph
        self.edges = graph.get_edges()
    
    def to_adjacency_matrix(self) -> AdjacencyMatrix:
        """
        Chuyển đổi sang biểu diễn ma trận kề
        Returns:
            Đối tượng AdjacencyMatrix
        """
        return AdjacencyMatrix(self.graph)
    
    def to_adjacency_list(self) -> AdjacencyList:
        """
        Chuyển đổi sang biểu diễn danh sách kề
        Returns:
            Đối tượng AdjacencyList
        """
        return AdjacencyList(self.graph)
    
    def get_edges(self) -> List[Tuple[int, int, float]]:
        """
        Lấy danh sách cạnh
        Returns:
            Danh sách cạnh
        """
        return self.edges
    
    def print_edges(self):
        """In danh sách cạnh ra màn hình"""
        print("Danh sách cạnh:")
        for i, (u, v, weight) in enumerate(self.edges, 1):
            print(f"Cạnh {i}: ({u}, {v}) - Trọng số: {weight}")
    
    def sort_by_weight(self, ascending: bool = True):
        """
        Sắp xếp danh sách cạnh theo trọng số
        Args:
            ascending: True để sắp xếp tăng dần, False để giảm dần
        """
        self.edges.sort(key=lambda x: x[2], reverse=not ascending)


def convert_representation(graph: Graph, target_type: str):
    """
    Chuyển đổi đồ thị sang dạng biểu diễn khác
    Args:
        graph: Đồ thị cần chuyển đổi
        target_type: Loại biểu diễn mục tiêu ('matrix', 'list', 'edges')
    Returns:
        Đối tượng biểu diễn tương ứng
    """
    if target_type.lower() == 'matrix':
        return AdjacencyMatrix(graph)
    elif target_type.lower() == 'list':
        return AdjacencyList(graph)
    elif target_type.lower() == 'edges':
        return EdgeList(graph)
    else:
        raise ValueError(f"Loại biểu diễn không hợp lệ: {target_type}")
