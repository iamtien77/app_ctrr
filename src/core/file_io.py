"""
Module xử lý đọc/ghi file cho đồ thị
Hỗ trợ định dạng JSON và TXT
"""
import json
from typing import Dict, Any
from src.core.graph import Graph, GraphType


def save_graph(graph: Graph, filepath: str, format: str = 'json'):
    """
    Lưu đồ thị vào file
    Args:
        graph: Đồ thị cần lưu
        filepath: Đường dẫn file
        format: Định dạng file ('json' hoặc 'txt')
    """
    if format.lower() == 'json':
        export_to_json(graph, filepath)
    elif format.lower() == 'txt':
        export_to_txt(graph, filepath)
    else:
        raise ValueError(f"Định dạng không hỗ trợ: {format}")


def load_graph(filepath: str, format: str = None) -> Graph:
    """
    Tải đồ thị từ file
    Args:
        filepath: Đường dẫn file
        format: Định dạng file ('json' hoặc 'txt'), None để tự động phát hiện
    Returns:
        Đối tượng Graph
    """
    # Tự động phát hiện định dạng từ phần mở rộng file
    if format is None:
        if filepath.lower().endswith('.json'):
            format = 'json'
        elif filepath.lower().endswith('.txt'):
            format = 'txt'
        else:
            # Thử đọc JSON trước, nếu lỗi thì thử TXT
            try:
                return import_from_json(filepath)
            except:
                return import_from_txt(filepath)
    
    if format.lower() == 'json':
        return import_from_json(filepath)
    elif format.lower() == 'txt':
        return import_from_txt(filepath)
    else:
        raise ValueError(f"Định dạng không hỗ trợ: {format}")


def export_to_json(graph: Graph, filepath: str):
    """
    Xuất đồ thị ra file JSON
    Args:
        graph: Đồ thị cần xuất
        filepath: Đường dẫn file JSON
    """
    # Chuẩn bị dữ liệu để lưu
    data = {
        'graph_type': graph.graph_type.value,
        'vertices': graph.get_vertices(),
        'edges': [
            {
                'source': u,
                'target': v,
                'weight': weight
            }
            for u, v, weight in graph.get_edges()
        ]
    }
    
    # Ghi vào file JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def import_from_json(filepath: str) -> Graph:
    """
    Nhập đồ thị từ file JSON
    Args:
        filepath: Đường dẫn file JSON
    Returns:
        Đối tượng Graph
    """
    # Đọc file JSON
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Tạo đồ thị mới
    graph_type = GraphType(data['graph_type'])
    graph = Graph(graph_type)
    
    # Thêm các đỉnh
    for vertex in data['vertices']:
        graph.add_vertex(vertex)
    
    # Thêm các cạnh
    for edge in data['edges']:
        graph.add_edge(
            edge['source'],
            edge['target'],
            edge.get('weight', 1.0)
        )
    
    return graph


def export_to_txt(graph: Graph, filepath: str):
    """
    Xuất đồ thị ra file TXT
    Định dạng:
    - Dòng 1: Loại đồ thị (DIRECTED hoặc UNDIRECTED)
    - Dòng 2: Số lượng đỉnh
    - Dòng 3: Danh sách đỉnh
    - Các dòng tiếp theo: Mỗi cạnh trên một dòng (u v weight)
    
    Args:
        graph: Đồ thị cần xuất
        filepath: Đường dẫn file TXT
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        # Ghi loại đồ thị
        f.write(f"{graph.graph_type.value.upper()}\n")
        
        # Ghi số lượng đỉnh
        vertices = graph.get_vertices()
        f.write(f"{len(vertices)}\n")
        
        # Ghi danh sách đỉnh
        f.write(" ".join(map(str, sorted(vertices))) + "\n")
        
        # Ghi các cạnh
        edges = graph.get_edges()
        f.write(f"{len(edges)}\n")
        for u, v, weight in edges:
            f.write(f"{u} {v} {weight}\n")


def import_from_txt(filepath: str) -> Graph:
    """
    Nhập đồ thị từ file TXT
    Args:
        filepath: Đường dẫn file TXT
    Returns:
        Đối tượng Graph
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('#')]
    
    if not lines:
        raise ValueError("File rỗng hoặc chỉ chứa comment")
    
    # Đọc loại đồ thị
    graph_type_str = lines[0].lower()
    graph_type = GraphType.DIRECTED if graph_type_str == 'directed' else GraphType.UNDIRECTED
    
    # Tạo đồ thị mới
    graph = Graph(graph_type)
    
    idx = 1
    # Đọc đỉnh (có thể là số hoặc chữ)
    vertices = []
    while idx < len(lines) and not any(c in lines[idx] for c in [' ', '\t']):
        vertex_str = lines[idx]
        try:
            vertex = int(vertex_str)
        except ValueError:
            vertex = vertex_str
        vertices.append(vertex)
        graph.add_vertex(vertex)
        idx += 1
    
    # Đọc các cạnh (format: u v weight hoặc u v)
    while idx < len(lines):
        parts = lines[idx].split()
        if len(parts) >= 2:
            try:
                u = int(parts[0])
            except ValueError:
                u = parts[0]
            
            try:
                v = int(parts[1])
            except ValueError:
                v = parts[1]
            
            weight = float(parts[2]) if len(parts) > 2 else 1.0
            graph.add_edge(u, v, weight)
        idx += 1
    
    return graph


def graph_to_dict(graph: Graph) -> Dict[str, Any]:
    """
    Chuyển đổi đồ thị thành dictionary
    Args:
        graph: Đồ thị cần chuyển đổi
    Returns:
        Dictionary chứa thông tin đồ thị
    """
    return {
        'graph_type': graph.graph_type.value,
        'vertices': graph.get_vertices(),
        'edges': [
            {'source': u, 'target': v, 'weight': weight}
            for u, v, weight in graph.get_edges()
        ],
        'vertex_count': graph.vertex_count(),
        'edge_count': graph.edge_count()
    }


def dict_to_graph(data: Dict[str, Any]) -> Graph:
    """
    Tạo đồ thị từ dictionary
    Args:
        data: Dictionary chứa thông tin đồ thị
    Returns:
        Đối tượng Graph
    """
    graph_type = GraphType(data['graph_type'])
    graph = Graph(graph_type)
    
    for vertex in data['vertices']:
        graph.add_vertex(vertex)
    
    for edge in data['edges']:
        graph.add_edge(
            edge['source'],
            edge['target'],
            edge.get('weight', 1.0)
        )
    
    return graph
