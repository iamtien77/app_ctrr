"""Hàm tiện ích: validate, thống kê, random graph"""
import random
from typing import Dict, List, Tuple, Optional
from src.core.graph import Graph, GraphType
from src.utils.config import (
    RANDOM_GRAPH_MIN_VERTICES, RANDOM_GRAPH_MAX_VERTICES,
    RANDOM_GRAPH_EDGE_PROBABILITY, RANDOM_GRAPH_MIN_WEIGHT,
    RANDOM_GRAPH_MAX_WEIGHT, MAX_VERTICES, MAX_EDGES
)


def validate_graph(graph: Graph) -> Tuple[bool, str]:
    """Kiểm tra hợp lệ - trả về (valid, error_msg)"""
    if graph.vertex_count() == 0:
        return False, "Đồ thị không có đỉnh nào"
    if graph.vertex_count() > MAX_VERTICES:
        return False, f"Số lượng đỉnh vượt quá giới hạn ({MAX_VERTICES})"
    if graph.edge_count() > MAX_EDGES:
        return False, f"Số lượng cạnh vượt quá giới hạn ({MAX_EDGES})"
    
    for u, v, weight in graph.get_edges():
        if weight < 0:
            return False, f"Cạnh ({u}, {v}) có trọng số âm: {weight}"
    
    return True, "Đồ thị hợp lệ"


def get_graph_info(graph: Graph) -> Dict[str, any]:
    """Thống kê đồ thị - trả về dict chứa các thông tin"""
    vertices = graph.get_vertices()
    edges = graph.get_edges()
    degrees = {v: graph.get_degree(v) for v in vertices}
    
    min_degree = min(degrees.values()) if degrees else 0
    max_degree = max(degrees.values()) if degrees else 0
    avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
    total_weight = sum(weight for _, _, weight in edges)
    
    # Tìm trọng số nhỏ nhất và lớn nhất
    weights = [weight for _, _, weight in edges]
    min_weight = min(weights) if weights else 0
    max_weight = max(weights) if weights else 0
    
    return {
        'vertex_count': graph.vertex_count(),
        'edge_count': graph.edge_count(),
        'graph_type': 'Có hướng' if graph.is_directed() else 'Vô hướng',
        'vertices': vertices,
        'degrees': degrees,
        'min_degree': min_degree,
        'max_degree': max_degree,
        'avg_degree': round(avg_degree, 2),
        'total_weight': round(total_weight, 2),
        'min_weight': min_weight,
        'max_weight': max_weight,
        'is_connected': is_connected(graph),
        'isolated_vertices': find_isolated_vertices(graph)
    }


def generate_random_graph(
    num_vertices: Optional[int] = None,
    graph_type: GraphType = GraphType.UNDIRECTED,
    edge_probability: float = RANDOM_GRAPH_EDGE_PROBABILITY,
    min_weight: int = RANDOM_GRAPH_MIN_WEIGHT,
    max_weight: int = RANDOM_GRAPH_MAX_WEIGHT
) -> Graph:
    """
    Tạo đồ thị ngẫu nhiên
    Args:
        num_vertices: Số lượng đỉnh (None = ngẫu nhiên)
        graph_type: Loại đồ thị
        edge_probability: Xác suất tạo cạnh giữa hai đỉnh
        min_weight: Trọng số tối thiểu
        max_weight: Trọng số tối đa
    Returns:
        Đồ thị ngẫu nhiên
    """
    # Nếu không chỉ định số đỉnh, chọn ngẫu nhiên
    if num_vertices is None:
        num_vertices = random.randint(RANDOM_GRAPH_MIN_VERTICES, RANDOM_GRAPH_MAX_VERTICES)
    
    # Tạo đồ thị mới
    graph = Graph(graph_type)
    
    # Thêm các đỉnh
    for i in range(num_vertices):
        graph.add_vertex(i)
    
    # Thêm các cạnh ngẫu nhiên
    vertices = graph.get_vertices()
    for i, u in enumerate(vertices):
        for v in vertices[i+1:]:
            # Tạo cạnh với xác suất edge_probability
            if random.random() < edge_probability:
                weight = random.uniform(min_weight, max_weight)
                graph.add_edge(u, v, round(weight, 2))
    
    return graph


def copy_graph(graph: Graph) -> Graph:
    """
    Sao chép đồ thị
    Args:
        graph: Đồ thị cần sao chép
    Returns:
        Đồ thị mới (bản sao)
    """
    # Tạo đồ thị mới cùng loại
    new_graph = Graph(graph.graph_type)
    
    # Sao chép các đỉnh
    for vertex in graph.get_vertices():
        new_graph.add_vertex(vertex)
    
    # Sao chép các cạnh
    for u, v, weight in graph.get_edges():
        new_graph.add_edge(u, v, weight)
    
    return new_graph


def is_connected(graph: Graph) -> bool:
    """
    Kiểm tra đồ thị có liên thông hay không (dùng BFS)
    Args:
        graph: Đồ thị cần kiểm tra
    Returns:
        True nếu đồ thị liên thông, False nếu không
    """
    vertices = graph.get_vertices()
    if not vertices:
        return True
    
    # BFS từ đỉnh đầu tiên
    visited = set()
    queue = [vertices[0]]
    visited.add(vertices[0])
    
    while queue:
        current = queue.pop(0)
        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # Đồ thị liên thông nếu thăm được tất cả các đỉnh
    return len(visited) == len(vertices)


def find_isolated_vertices(graph: Graph) -> List[int]:
    """
    Tìm các đỉnh cô lập (không có cạnh nào)
    Args:
        graph: Đồ thị cần kiểm tra
    Returns:
        Danh sách các đỉnh cô lập
    """
    isolated = []
    for vertex in graph.get_vertices():
        if graph.get_degree(vertex) == 0:
            isolated.append(vertex)
    return isolated


def get_connected_components(graph: Graph) -> List[List[int]]:
    """
    Tìm các thành phần liên thông của đồ thị
    Args:
        graph: Đồ thị cần phân tích
    Returns:
        Danh sách các thành phần liên thông
    """
    vertices = graph.get_vertices()
    visited = set()
    components = []
    
    for vertex in vertices:
        if vertex not in visited:
            # BFS từ đỉnh chưa thăm
            component = []
            queue = [vertex]
            visited.add(vertex)
            
            while queue:
                current = queue.pop(0)
                component.append(current)
                
                for neighbor in graph.get_neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(sorted(component))
    
    return components


def reverse_graph(graph: Graph) -> Graph:
    """
    Đảo ngược hướng của tất cả các cạnh (chỉ áp dụng cho đồ thị có hướng)
    Args:
        graph: Đồ thị cần đảo ngược
    Returns:
        Đồ thị đảo ngược
    """
    if not graph.is_directed():
        return copy_graph(graph)
    
    reversed_graph = Graph(GraphType.DIRECTED)
    
    # Thêm các đỉnh
    for vertex in graph.get_vertices():
        reversed_graph.add_vertex(vertex)
    
    # Đảo ngược các cạnh
    for u, v, weight in graph.get_edges():
        reversed_graph.add_edge(v, u, weight)
    
    return reversed_graph


def format_path(path: List[int]) -> str:
    """
    Định dạng đường đi thành chuỗi dễ đọc
    Args:
        path: Danh sách các đỉnh trong đường đi
    Returns:
        Chuỗi biểu diễn đường đi
    """
    if not path:
        return "Không có đường đi"
    return " → ".join(map(str, path))


def calculate_path_weight(graph: Graph, path: List[int]) -> float:
    """
    Tính tổng trọng số của đường đi
    Args:
        graph: Đồ thị
        path: Danh sách các đỉnh trong đường đi
    Returns:
        Tổng trọng số
    """
    if len(path) < 2:
        return 0.0
    
    total_weight = 0.0
    for i in range(len(path) - 1):
        weight = graph.get_weight(path[i], path[i + 1])
        if weight is not None:
            total_weight += weight
    
    return total_weight
