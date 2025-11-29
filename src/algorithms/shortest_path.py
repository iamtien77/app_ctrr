"""Đường đi ngắn nhất: Dijkstra, Bellman-Ford, Floyd-Warshall"""
from typing import Dict, List, Optional, Tuple, Callable
import heapq
from src.core.graph import Graph
from src.utils.config import INFINITY


def dijkstra(graph: Graph, start: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """Dijkstra - tìm đường ngắn nhất từ start, trả về (distances, parent)"""
    vertices = graph.get_vertices()
    distances = {v: INFINITY for v in vertices}
    parent = {v: None for v in vertices}
    distances[start] = 0
    
    pq = [(0, start)]  # Priority queue: (distance, vertex)
    visited = set()
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        
        for v in graph.get_neighbors(u):
            weight = graph.get_weight(u, v)
            new_dist = current_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))
    
    return distances, parent


def bellman_ford(graph: Graph, start: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool]:
    """
    Thuật toán Bellman-Ford tìm đường đi ngắn nhất (hỗ trợ trọng số âm)
    
    Thuật toán:
    1. Khởi tạo khoảng cách tất cả đỉnh = vô cực, trừ đỉnh start = 0
    2. Lặp (n-1) lần (n = số đỉnh):
       - Với mỗi cạnh (u, v, w):
         Nếu distance[u] + w < distance[v]
         => Cập nhật distance[v] và parent[v] = u
    3. Kiểm tra chu trình âm: nếu còn cập nhật được => có chu trình âm
    
    Args:
        graph: Đồ thị cần tìm
        start: Đỉnh bắt đầu
    Returns:
        Tuple (khoảng_cách, đỉnh_cha, có_chu_trình_âm)
    """
    vertices = graph.get_vertices()
    edges = graph.get_edges()
    
    # Khởi tạo
    distances = {v: INFINITY for v in vertices}
    parent = {v: None for v in vertices}
    distances[start] = 0
    
    # Lặp (n-1) lần
    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, weight in edges:
            if distances[u] != INFINITY and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                parent[v] = u
                updated = True
        
        # Nếu không có cập nhật nào, dừng sớm
        if not updated:
            break
    
    # Kiểm tra chu trình âm
    has_negative_cycle = False
    for u, v, weight in edges:
        if distances[u] != INFINITY and distances[u] + weight < distances[v]:
            has_negative_cycle = True
            break
    
    return distances, parent, has_negative_cycle


def floyd_warshall(graph: Graph) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], Optional[int]]]:
    """
    Thuật toán Floyd-Warshall tìm đường đi ngắn nhất giữa tất cả các cặp đỉnh
    
    Thuật toán:
    1. Khởi tạo ma trận khoảng cách:
       - dist[i][i] = 0
       - dist[i][j] = weight(i,j) nếu có cạnh
       - dist[i][j] = vô cực nếu không có cạnh
    2. Với mỗi đỉnh k làm đỉnh trung gian:
       - Với mỗi cặp đỉnh (i, j):
         Nếu dist[i][k] + dist[k][j] < dist[i][j]
         => Cập nhật dist[i][j] và next[i][j] = next[i][k]
    
    Args:
        graph: Đồ thị cần tìm
    Returns:
        Tuple (khoảng_cách, đỉnh_kế_tiếp)
        - khoảng_cách: {(u, v): khoảng_cách_ngắn_nhất}
        - đỉnh_kế_tiếp: {(u, v): đỉnh_kế_tiếp_trong_đường_đi}
    """
    vertices = graph.get_vertices()
    
    # Khởi tạo ma trận khoảng cách
    dist = {}
    next_vertex = {}
    
    # Khởi tạo
    for u in vertices:
        for v in vertices:
            if u == v:
                dist[(u, v)] = 0
                next_vertex[(u, v)] = v
            else:
                dist[(u, v)] = INFINITY
                next_vertex[(u, v)] = None
    
    # Cập nhật khoảng cách ban đầu từ các cạnh
    for u, v, weight in graph.get_edges():
        dist[(u, v)] = weight
        next_vertex[(u, v)] = v
    
    # Thuật toán Floyd-Warshall
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[(i, k)] + dist[(k, j)] < dist[(i, j)]:
                    dist[(i, j)] = dist[(i, k)] + dist[(k, j)]
                    next_vertex[(i, j)] = next_vertex[(i, k)]
    
    return dist, next_vertex


def get_path_from_parent(parent: Dict[int, Optional[int]], start: int, end: int) -> Optional[List[int]]:
    """
    Truy vết đường đi từ dictionary đỉnh cha
    
    Args:
        parent: Dictionary {đỉnh: đỉnh_cha}
        start: Đỉnh bắt đầu
        end: Đỉnh kết thúc
    Returns:
        Danh sách các đỉnh trong đường đi, None nếu không tìm thấy
    """
    if parent.get(end) is None and start != end:
        return None
    
    path = []
    current = end
    
    while current is not None:
        path.append(current)
        if current == start:
            break
        current = parent.get(current)
    
    if path[-1] != start:
        return None
    
    return list(reversed(path))


def dijkstra_with_callback(graph: Graph, start: int, 
                          callback: Callable[[int, float, str], None]) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
    """
    Dijkstra với callback để trực quan hóa
    
    Args:
        graph: Đồ thị cần tìm
        start: Đỉnh bắt đầu
        callback: Hàm callback(vertex, distance, state)
    Returns:
        Tuple (khoảng_cách, đỉnh_cha)
    """
    vertices = graph.get_vertices()
    distances = {v: INFINITY for v in vertices}
    parent = {v: None for v in vertices}
    distances[start] = 0
    
    pq = [(0, start)]
    visited = set()
    
    callback(start, 0, 'start')
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if u in visited:
            continue
        
        visited.add(u)
        callback(u, current_dist, 'visited')
        
        for v in graph.get_neighbors(u):
            weight = graph.get_weight(u, v)
            new_dist = current_dist + weight
            
            if new_dist < distances[v]:
                distances[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))
                callback(v, new_dist, 'updated')
    
    return distances, parent


def find_shortest_path(graph: Graph, start: int, end: int) -> Tuple[Optional[List[int]], float]:
    """
    Tìm đường đi ngắn nhất từ start đến end
    
    Args:
        graph: Đồ thị
        start: Đỉnh bắt đầu
        end: Đỉnh kết thúc
    Returns:
        Tuple (đường_đi, độ_dài)
    """
    distances, parent = dijkstra(graph, start)
    
    if distances[end] == INFINITY:
        return None, INFINITY
    
    path = get_path_from_parent(parent, start, end)
    return path, distances[end]
