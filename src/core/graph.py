"""Cấu trúc đồ thị cơ bản - sử dụng danh sách kề"""
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum

class GraphType(Enum):
    """Loại đồ thị"""
    DIRECTED = "directed"
    UNDIRECTED = "undirected"

class Graph:
    """Lớp đồ thị - danh sách kề (adjacency list)"""
    
    def __init__(self, graph_type: GraphType = GraphType.UNDIRECTED):
        """Khởi tạo (graph_type: có hướng/vô hướng)"""
        self.graph_type = graph_type
        self._adjacency_list: Dict[int, Dict[int, float]] = {}  # {đỉnh: {đỉnh_kề: trọng_số}}
        
    def add_vertex(self, vertex: int):
        """
        Thêm một đỉnh vào đồ thị
        Args:
            vertex: Số hiệu đỉnh cần thêm
        """
        if vertex not in self._adjacency_list:
            self._adjacency_list[vertex] = {}
        
    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """
        Thêm một cạnh vào đồ thị
        Args:
            u: Đỉnh xuất phát
            v: Đỉnh đích
            weight: Trọng số của cạnh (mặc định là 1.0)
        """
        # Đảm bảo cả hai đỉnh đã tồn tại
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Thêm cạnh từ u đến v
        self._adjacency_list[u][v] = weight
        
        # Nếu là đồ thị vô hướng, thêm cạnh ngược lại từ v đến u
        if self.graph_type == GraphType.UNDIRECTED:
            self._adjacency_list[v][u] = weight
        
    def remove_vertex(self, vertex: int):
        """
        Xóa một đỉnh khỏi đồ thị
        Args:
            vertex: Số hiệu đỉnh cần xóa
        """
        if vertex not in self._adjacency_list:
            return
        
        # Xóa đỉnh khỏi danh sách kề
        del self._adjacency_list[vertex]
        
        # Xóa tất cả các cạnh đến đỉnh này
        for neighbors in self._adjacency_list.values():
            if vertex in neighbors:
                del neighbors[vertex]
        
    def remove_edge(self, u: int, v: int):
        """
        Xóa một cạnh khỏi đồ thị
        Args:
            u: Đỉnh xuất phát
            v: Đỉnh đích
        """
        if u in self._adjacency_list and v in self._adjacency_list[u]:
            del self._adjacency_list[u][v]
        
        # Nếu là đồ thị vô hướng, xóa cạnh ngược lại
        if self.graph_type == GraphType.UNDIRECTED:
            if v in self._adjacency_list and u in self._adjacency_list[v]:
                del self._adjacency_list[v][u]
        
    def get_vertices(self) -> List[int]:
        """
        Lấy danh sách tất cả các đỉnh
        Returns:
            Danh sách các đỉnh trong đồ thị
        """
        return list(self._adjacency_list.keys())
        
    def get_edges(self) -> List[Tuple[int, int, float]]:
        """
        Lấy danh sách tất cả các cạnh
        Returns:
            Danh sách các cạnh dạng (đỉnh_u, đỉnh_v, trọng_số)
        """
        edges = []
        visited = set()  # Tránh trùng lặp cạnh trong đồ thị vô hướng
        
        for u, neighbors in self._adjacency_list.items():
            for v, weight in neighbors.items():
                # Đối với đồ thị vô hướng, chỉ lưu một chiều của cạnh
                if self.graph_type == GraphType.UNDIRECTED:
                    edge = tuple(sorted([u, v]))
                    if edge not in visited:
                        edges.append((u, v, weight))
                        visited.add(edge)
                else:
                    edges.append((u, v, weight))
        
        return edges
        
    def has_edge(self, u: int, v: int) -> bool:
        """
        Kiểm tra xem cạnh có tồn tại hay không
        Args:
            u: Đỉnh xuất phát
            v: Đỉnh đích
        Returns:
            True nếu cạnh tồn tại, False nếu không
        """
        return u in self._adjacency_list and v in self._adjacency_list[u]
        
    def get_neighbors(self, vertex: int) -> List[int]:
        """
        Lấy danh sách các đỉnh kề với đỉnh cho trước
        Args:
            vertex: Đỉnh cần lấy danh sách kề
        Returns:
            Danh sách các đỉnh kề
        """
        if vertex not in self._adjacency_list:
            return []
        return list(self._adjacency_list[vertex].keys())
    
    def get_weight(self, u: int, v: int) -> Optional[float]:
        """
        Lấy trọng số của cạnh
        Args:
            u: Đỉnh xuất phát
            v: Đỉnh đích
        Returns:
            Trọng số của cạnh, None nếu cạnh không tồn tại
        """
        if self.has_edge(u, v):
            return self._adjacency_list[u][v]
        return None
    
    def get_adjacency_list(self) -> Dict[int, Dict[int, float]]:
        """
        Lấy danh sách kề của đồ thị
        Returns:
            Danh sách kề dạng dictionary
        """
        return self._adjacency_list.copy()
    
    def vertex_count(self) -> int:
        """
        Đếm số lượng đỉnh trong đồ thị
        Returns:
            Số lượng đỉnh
        """
        return len(self._adjacency_list)
    
    def edge_count(self) -> int:
        """
        Đếm số lượng cạnh trong đồ thị
        Returns:
            Số lượng cạnh
        """
        count = sum(len(neighbors) for neighbors in self._adjacency_list.values())
        # Đồ thị vô hướng đếm mỗi cạnh 2 lần, nên chia 2
        if self.graph_type == GraphType.UNDIRECTED:
            count //= 2
        return count
    
    def is_directed(self) -> bool:
        """
        Kiểm tra xem đồ thị có hướng hay không
        Returns:
            True nếu là đồ thị có hướng, False nếu không
        """
        return self.graph_type == GraphType.DIRECTED
    
    def get_degree(self, vertex: int) -> int:
        """
        Lấy bậc của đỉnh (số cạnh kết nối với đỉnh)
        Args:
            vertex: Đỉnh cần tính bậc
        Returns:
            Bậc của đỉnh
        """
        if vertex not in self._adjacency_list:
            return 0
        return len(self._adjacency_list[vertex])
    
    def clear(self):
        """Xóa toàn bộ đồ thị"""
        self._adjacency_list.clear()

