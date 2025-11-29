"""Thuật toán Euler - chu trình & đường đi qua mỗi cạnh đúng 1 lần"""
from typing import List, Optional, Callable, Tuple
from collections import defaultdict
from src.core.graph import Graph


def is_eulerian(graph: Graph) -> str:
    """
    Kiểm tra Euler: 'cycle' (chu trình), 'path' (đường đi), 'none' (không có)
    - Vô hướng: cycle nếu tất cả bậc chẵn, path nếu 2 đỉnh bậc lẻ
    - Có hướng: cycle nếu bậc vào = bậc ra, path nếu 1 đỉnh out>in và 1 đỉnh in>out
    """
    vertices = graph.get_vertices()
    
    if not vertices or graph.edge_count() == 0:
        return 'none'
    
    if graph.is_directed():
        # Đồ thị có hướng
        in_degree = {v: 0 for v in vertices}
        out_degree = {v: 0 for v in vertices}
        
        for u, v, _ in graph.get_edges():
            out_degree[u] += 1
            in_degree[v] += 1
        
        start_vertices = 0  # Đỉnh có out > in
        end_vertices = 0    # Đỉnh có in > out
        
        for v in vertices:
            diff = out_degree[v] - in_degree[v]
            if diff > 1 or diff < -1:
                return 'none'
            if diff == 1:
                start_vertices += 1
            elif diff == -1:
                end_vertices += 1
        
        if start_vertices == 0 and end_vertices == 0:
            return 'cycle'
        if start_vertices == 1 and end_vertices == 1:
            return 'path'
        return 'none'
    
    else:
        # Đồ thị vô hướng
        odd_vertices = 0
        for v in vertices:
            if graph.get_degree(v) % 2 == 1:
                odd_vertices += 1
        
        if odd_vertices == 0:
            return 'cycle'
        elif odd_vertices == 2:
            return 'path'
        else:
            return 'none'


def fleury(graph: Graph, start: Optional[int] = None) -> Optional[List[Tuple[int, int]]]:
    """
    Thuật toán Fleury tìm đường đi Euler
    
    Thuật toán:
    1. Bắt đầu từ đỉnh có bậc lẻ (nếu có) hoặc đỉnh bất kỳ
    2. Chọn cạnh kế tiếp sao cho:
       - Không phải cầu (bridge) trừ khi không còn cạnh nào khác
    3. Xóa cạnh vừa đi và lặp lại cho đến hết cạnh
    
    Args:
        graph: Đồ thị cần tìm
        start: Đỉnh bắt đầu (None = tự động chọn)
    Returns:
        Danh sách các cạnh trong đường đi Euler, None nếu không tồn tại
    """
    euler_type = is_eulerian(graph)
    if euler_type == 'none':
        return None
    
    # Tạo bản sao đồ thị để không ảnh hưởng đồ thị gốc
    from src.utils.helpers import copy_graph
    temp_graph = copy_graph(graph)
    
    # Chọn đỉnh bắt đầu
    if start is None:
        vertices = temp_graph.get_vertices()
        if euler_type == 'path':
            # Chọn đỉnh có bậc lẻ
            for v in vertices:
                if temp_graph.get_degree(v) % 2 == 1:
                    start = v
                    break
        else:
            start = vertices[0]
    
    def is_bridge(u: int, v: int) -> bool:
        """Kiểm tra cạnh (u,v) có phải cầu không"""
        # Cầu là cạnh mà khi xóa sẽ làm tăng số thành phần liên thông
        # Đơn giản: nếu xóa cạnh mà v không còn đường đến u => là cầu
        if temp_graph.get_degree(u) == 1:
            return True
        
        temp_graph.remove_edge(u, v)
        
        # BFS để kiểm tra còn đường từ u đến v không
        from collections import deque
        visited = {u}
        queue = deque([u])
        found = False
        
        while queue:
            current = queue.popleft()
            if current == v:
                found = True
                break
            
            for neighbor in temp_graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        temp_graph.add_edge(u, v, 1.0)
        return not found
    
    path = []
    current = start
    
    while temp_graph.get_degree(current) > 0:
        neighbors = temp_graph.get_neighbors(current)
        
        # Tìm cạnh không phải cầu
        next_vertex = None
        for v in neighbors:
            if not is_bridge(current, v) or len(neighbors) == 1:
                next_vertex = v
                break
        
        if next_vertex is None:
            next_vertex = neighbors[0]
        
        path.append((current, next_vertex))
        temp_graph.remove_edge(current, next_vertex)
        current = next_vertex
    
    return path


def hierholzer(graph: Graph, start: Optional[int] = None) -> Optional[List[Tuple[int, int]]]:
    """
    Thuật toán Hierholzer tìm đường đi Euler (hiệu quả hơn Fleury)
    
    Thuật toán:
    1. Tạo chu trình con bất kỳ
    2. Nếu còn cạnh chưa đi:
       - Chọn đỉnh trong chu trình còn cạnh chưa đi
       - Tạo chu trình con mới từ đỉnh đó
       - Ghép chu trình con vào chu trình chính
    
    Args:
        graph: Đồ thị cần tìm
        start: Đỉnh bắt đầu
    Returns:
        Danh sách các cạnh trong đường đi Euler, None nếu không tồn tại
    """
    euler_type = is_eulerian(graph)
    if euler_type == 'none':
        return None
    
    # Chọn đỉnh bắt đầu
    if start is None:
        vertices = graph.get_vertices()
        if euler_type == 'path':
            for v in vertices:
                if graph.get_degree(v) % 2 == 1:
                    start = v
                    break
        else:
            start = vertices[0]
    
    # Tạo dictionary lưu các cạnh chưa thăm
    edges = defaultdict(list)
    for u, v, _ in graph.get_edges():
        edges[u].append(v)
        if not graph.is_directed():
            edges[v].append(u)
    
    # Stack và đường đi kết quả
    stack = [start]
    path = []
    
    while stack:
        current = stack[-1]
        
        if edges[current]:
            # Còn cạnh chưa đi từ current
            next_vertex = edges[current].pop()
            
            # Xóa cạnh ngược (đối với đồ thị vô hướng)
            if not graph.is_directed() and current in edges[next_vertex]:
                edges[next_vertex].remove(current)
            
            stack.append(next_vertex)
        else:
            # Không còn cạnh => thêm vào đường đi
            path.append(stack.pop())
    
    # Đảo ngược đường đi
    path.reverse()
    
    # Chuyển từ danh sách đỉnh sang danh sách cạnh
    edge_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    
    return edge_path


def fleury_with_callback(graph: Graph, start: Optional[int],
                        callback: Callable[[int, int], None]) -> Optional[List[Tuple[int, int]]]:
    """
    Fleury với callback để trực quan hóa
    
    Args:
        graph: Đồ thị
        start: Đỉnh bắt đầu
        callback: Hàm callback(u, v) được gọi khi đi qua cạnh (u, v)
    Returns:
        Đường đi Euler
    """
    result = fleury(graph, start)
    if result and callback:
        for u, v in result:
            callback(u, v)
    return result


def hierholzer_with_callback(graph: Graph, start: Optional[int],
                             callback: Callable[[int, int], None]) -> Optional[List[Tuple[int, int]]]:
    """
    Hierholzer với callback để trực quan hóa
    
    Args:
        graph: Đồ thị
        start: Đỉnh bắt đầu
        callback: Hàm callback(u, v) được gọi khi đi qua cạnh (u, v)
    Returns:
        Đường đi Euler
    """
    result = hierholzer(graph, start)
    if result and callback:
        for u, v in result:
            callback(u, v)
    return result
