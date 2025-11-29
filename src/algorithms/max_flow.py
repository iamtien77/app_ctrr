"""Luồng cực đại: Ford-Fulkerson & Edmonds-Karp"""
from typing import Dict, List, Tuple, Optional, Callable
from collections import deque
from src.core.graph import Graph, GraphType
from src.utils.config import INFINITY


def ford_fulkerson(graph: Graph, source: int, sink: int) -> Tuple[float, Dict[Tuple[int, int], float]]:
    """Ford-Fulkerson - tìm luồng max từ source đến sink, trả về (max_flow, flow_dict)"""
    # Đồ thị phần dư (residual)
    residual = {}
    vertices = graph.get_vertices()
    
    for v in vertices:
        residual[v] = {}
    
    for u, v, capacity in graph.get_edges():
        residual[u][v] = capacity
        if v not in residual:
            residual[v] = {}
        if u not in residual[v]:
            residual[v][u] = 0
    
    def bfs_find_path(src: int, dst: int) -> Optional[List[int]]:
        """BFS tìm đường tăng luồng"""
        if src == dst:
            return [src]
        
        visited = {src}
        queue = deque([src])
        parent = {src: None}
        
        while queue:
            u = queue.popleft()
            
            for v in residual.get(u, {}):
                if v not in visited and residual[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
                    
                    if v == dst:
                        # Truy vết đường đi
                        path = []
                        current = dst
                        while current is not None:
                            path.append(current)
                            current = parent[current]
                        return list(reversed(path))
        
        return None
    
    max_flow = 0.0
    flow = {}  # Luồng trên mỗi cạnh
    
    # Khởi tạo luồng = 0
    for u, v, _ in graph.get_edges():
        flow[(u, v)] = 0.0
    
    # Tìm đường tăng luồng
    while True:
        path = bfs_find_path(source, sink)
        
        if path is None:
            break  # Không còn đường tăng luồng
        
        # Tìm dung lượng tối thiểu trên đường đi (bottleneck)
        path_flow = INFINITY
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            path_flow = min(path_flow, residual[u][v])
        
        # Cập nhật luồng và đồ thị phần dư
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            
            # Tăng luồng
            if (u, v) in flow:
                flow[(u, v)] += path_flow
            elif (v, u) in flow:
                flow[(v, u)] -= path_flow
            
            # Cập nhật đồ thị phần dư
            residual[u][v] -= path_flow
            residual[v][u] = residual.get(v, {}).get(u, 0) + path_flow
        
        max_flow += path_flow
    
    return max_flow, flow


def edmonds_karp(graph: Graph, source: int, sink: int) -> Tuple[float, Dict[Tuple[int, int], float]]:
    """
    Thuật toán Edmonds-Karp (biến thể của Ford-Fulkerson sử dụng BFS)
    
    Args:
        graph: Đồ thị (có hướng, trọng số là dung lượng)
        source: Đỉnh nguồn
        sink: Đỉnh đích
    Returns:
        Tuple (luồng_cực_đại, luồng_trên_mỗi_cạnh)
    """
    # Edmonds-Karp giống Ford-Fulkerson nhưng luôn dùng BFS
    # Implementation ở trên đã dùng BFS nên giống Edmonds-Karp
    return ford_fulkerson(graph, source, sink)


def ford_fulkerson_with_callback(graph: Graph, source: int, sink: int,
                                 callback: Callable[[List[int], float], None]) -> Tuple[float, Dict[Tuple[int, int], float]]:
    """
    Ford-Fulkerson với callback để trực quan hóa
    
    Args:
        graph: Đồ thị
        source: Đỉnh nguồn
        sink: Đỉnh đích
        callback: Hàm callback(path, flow) được gọi mỗi lần tìm được đường tăng luồng
    Returns:
        Tuple (luồng_cực_đại, luồng_trên_mỗi_cạnh)
    """
    # Tương tự ford_fulkerson nhưng có callback
    residual = {}
    vertices = graph.get_vertices()
    
    for v in vertices:
        residual[v] = {}
    
    for u, v, capacity in graph.get_edges():
        residual[u][v] = capacity
        if v not in residual:
            residual[v] = {}
        if u not in residual[v]:
            residual[v][u] = 0
    
    def bfs_find_path(src: int, dst: int) -> Optional[List[int]]:
        if src == dst:
            return [src]
        
        visited = {src}
        queue = deque([src])
        parent = {src: None}
        
        while queue:
            u = queue.popleft()
            
            for v in residual.get(u, {}):
                if v not in visited and residual[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
                    
                    if v == dst:
                        path = []
                        current = dst
                        while current is not None:
                            path.append(current)
                            current = parent[current]
                        return list(reversed(path))
        
        return None
    
    max_flow = 0.0
    flow = {}
    
    for u, v, _ in graph.get_edges():
        flow[(u, v)] = 0.0
    
    while True:
        path = bfs_find_path(source, sink)
        
        if path is None:
            break
        
        path_flow = INFINITY
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            path_flow = min(path_flow, residual[u][v])
        
        # Gọi callback
        callback(path, path_flow)
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            
            if (u, v) in flow:
                flow[(u, v)] += path_flow
            elif (v, u) in flow:
                flow[(v, u)] -= path_flow
            
            residual[u][v] -= path_flow
            residual[v][u] = residual.get(v, {}).get(u, 0) + path_flow
        
        max_flow += path_flow
    
    return max_flow, flow


def find_min_cut(graph: Graph, source: int, sink: int) -> Tuple[List[int], List[int]]:
    """
    Tìm cắt nhỏ nhất (minimum cut) từ kết quả luồng cực đại
    
    Args:
        graph: Đồ thị
        source: Đỉnh nguồn
        sink: Đỉnh đích
    Returns:
        Tuple (tập_nguồn, tập_đích) - 2 tập đỉnh được phân chia bởi cắt nhỏ nhất
    """
    max_flow, flow = ford_fulkerson(graph, source, sink)
    
    # Xây dựng đồ thị phần dư
    residual = {}
    vertices = graph.get_vertices()
    
    for v in vertices:
        residual[v] = {}
    
    for u, v, capacity in graph.get_edges():
        actual_flow = flow.get((u, v), 0.0)
        residual[u][v] = capacity - actual_flow
        if v not in residual:
            residual[v] = {}
        residual[v][u] = actual_flow
    
    # BFS từ source trong đồ thị phần dư
    visited = {source}
    queue = deque([source])
    
    while queue:
        u = queue.popleft()
        for v in residual.get(u, {}):
            if v not in visited and residual[u][v] > 0:
                visited.add(v)
                queue.append(v)
    
    # Tập nguồn: các đỉnh đến được từ source
    # Tập đích: các đỉnh còn lại
    source_set = list(visited)
    sink_set = [v for v in vertices if v not in visited]
    
    return source_set, sink_set
