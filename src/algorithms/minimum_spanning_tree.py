"""Cây khung nhỏ nhất (MST): Prim & Kruskal"""
from typing import List, Tuple, Set, Dict, Callable, Optional
import heapq
from src.core.graph import Graph, GraphType


class UnionFind:
    """Union-Find (DSU) - kiểm tra chu trình cho Kruskal"""
    
    def __init__(self, vertices: List[int]):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, x: int) -> int:
        """Tìm gốc (với path compression)"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """Hợp nhất 2 tập (by rank) - trả về False nếu đã cùng tập"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True


def prim(graph: Graph, start: Optional[int] = None) -> Tuple[List[Tuple[int, int, float]], float]:
    """
    Thuật toán Prim tìm cây khung nhỏ nhất
    
    Thuật toán:
    1. Bắt đầu từ một đỉnh bất kỳ
    2. Lặp cho đến khi có đủ (n-1) cạnh:
       - Chọn cạnh có trọng số nhỏ nhất nối giữa cây và đỉnh ngoài cây
       - Thêm cạnh đó vào cây
    
    Args:
        graph: Đồ thị cần tìm MST (phải là đồ thị vô hướng, liên thông)
        start: Đỉnh bắt đầu (None = chọn ngẫu nhiên)
    Returns:
        Tuple (danh_sách_cạnh_MST, tổng_trọng_số)
    """
    if graph.is_directed():
        raise ValueError("Thuật toán Prim chỉ áp dụng cho đồ thị vô hướng")
    
    vertices = graph.get_vertices()
    if not vertices:
        return [], 0.0
    
    # Chọn đỉnh bắt đầu
    if start is None:
        start = vertices[0]
    
    mst_edges = []  # Các cạnh trong MST
    total_weight = 0.0  # Tổng trọng số
    
    visited = set([start])  # Tập đỉnh đã thăm
    # Hàng đợi ưu tiên: (trọng_số, đỉnh_u, đỉnh_v)
    pq = []
    
    # Thêm tất cả cạnh từ đỉnh bắt đầu vào heap
    for neighbor in graph.get_neighbors(start):
        weight = graph.get_weight(start, neighbor)
        heapq.heappush(pq, (weight, start, neighbor))
    
    # Lặp cho đến khi có đủ (n-1) cạnh
    while pq and len(mst_edges) < len(vertices) - 1:
        weight, u, v = heapq.heappop(pq)
        
        # Bỏ qua nếu đỉnh v đã trong cây
        if v in visited:
            continue
        
        # Thêm cạnh vào MST
        mst_edges.append((u, v, weight))
        total_weight += weight
        visited.add(v)
        
        # Thêm các cạnh từ v vào heap
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                w = graph.get_weight(v, neighbor)
                heapq.heappush(pq, (w, v, neighbor))
    
    return mst_edges, total_weight


def kruskal(graph: Graph) -> Tuple[List[Tuple[int, int, float]], float]:
    """
    Thuật toán Kruskal tìm cây khung nhỏ nhất
    
    Thuật toán:
    1. Sắp xếp tất cả các cạnh theo trọng số tăng dần
    2. Lặp qua các cạnh:
       - Nếu cạnh không tạo chu trình => thêm vào MST
       - Sử dụng Union-Find để kiểm tra chu trình
    
    Args:
        graph: Đồ thị cần tìm MST (phải là đồ thị vô hướng, liên thông)
    Returns:
        Tuple (danh_sách_cạnh_MST, tổng_trọng_số)
    """
    if graph.is_directed():
        raise ValueError("Thuật toán Kruskal chỉ áp dụng cho đồ thị vô hướng")
    
    vertices = graph.get_vertices()
    edges = graph.get_edges()
    
    if not vertices:
        return [], 0.0
    
    # Sắp xếp các cạnh theo trọng số tăng dần
    edges.sort(key=lambda e: e[2])
    
    # Khởi tạo Union-Find
    uf = UnionFind(vertices)
    
    mst_edges = []
    total_weight = 0.0
    
    # Duyệt các cạnh theo thứ tự tăng dần của trọng số
    for u, v, weight in edges:
        # Nếu thêm cạnh không tạo chu trình
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            # Đủ (n-1) cạnh => dừng
            if len(mst_edges) == len(vertices) - 1:
                break
    
    return mst_edges, total_weight


def prim_with_callback(graph: Graph, start: Optional[int], 
                      callback: Callable[[int, int, float, str], None]) -> Tuple[List[Tuple[int, int, float]], float]:
    """
    Thuật toán Prim với callback để trực quan hóa
    
    Args:
        graph: Đồ thị cần tìm MST
        start: Đỉnh bắt đầu
        callback: Hàm callback(u, v, weight, state)
                 state: 'considering', 'added', 'rejected'
    Returns:
        Tuple (danh_sách_cạnh_MST, tổng_trọng_số)
    """
    if graph.is_directed():
        raise ValueError("Thuật toán Prim chỉ áp dụng cho đồ thị vô hướng")
    
    vertices = graph.get_vertices()
    if not vertices:
        return [], 0.0
    
    if start is None:
        start = vertices[0]
    
    mst_edges = []
    total_weight = 0.0
    visited = set([start])
    pq = []
    
    # Thêm cạnh từ đỉnh bắt đầu
    for neighbor in graph.get_neighbors(start):
        weight = graph.get_weight(start, neighbor)
        heapq.heappush(pq, (weight, start, neighbor))
    
    while pq and len(mst_edges) < len(vertices) - 1:
        weight, u, v = heapq.heappop(pq)
        
        callback(u, v, weight, 'considering')
        
        if v in visited:
            callback(u, v, weight, 'rejected')
            continue
        
        # Thêm cạnh vào MST
        mst_edges.append((u, v, weight))
        total_weight += weight
        visited.add(v)
        callback(u, v, weight, 'added')
        
        # Thêm các cạnh mới
        for neighbor in graph.get_neighbors(v):
            if neighbor not in visited:
                w = graph.get_weight(v, neighbor)
                heapq.heappush(pq, (w, v, neighbor))
    
    return mst_edges, total_weight


def kruskal_with_callback(graph: Graph,
                         callback: Callable[[int, int, float, str], None]) -> Tuple[List[Tuple[int, int, float]], float]:
    """
    Thuật toán Kruskal với callback để trực quan hóa
    
    Args:
        graph: Đồ thị cần tìm MST
        callback: Hàm callback(u, v, weight, state)
                 state: 'considering', 'added', 'rejected'
    Returns:
        Tuple (danh_sách_cạnh_MST, tổng_trọng_số)
    """
    if graph.is_directed():
        raise ValueError("Thuật toán Kruskal chỉ áp dụng cho đồ thị vô hướng")
    
    vertices = graph.get_vertices()
    edges = graph.get_edges()
    
    if not vertices:
        return [], 0.0
    
    edges.sort(key=lambda e: e[2])
    uf = UnionFind(vertices)
    
    mst_edges = []
    total_weight = 0.0
    
    for u, v, weight in edges:
        callback(u, v, weight, 'considering')
        
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            callback(u, v, weight, 'added')
            
            if len(mst_edges) == len(vertices) - 1:
                break
        else:
            callback(u, v, weight, 'rejected')
    
    return mst_edges, total_weight
