"""Kiểm tra đồ thị 2 phía - tô màu bằng BFS"""
from typing import Dict, List, Tuple, Optional, Callable
from collections import deque
from src.core.graph import Graph


def is_bipartite(graph: Graph) -> bool:
    """Kiểm tra đồ thị 2 phía (chia làm 2 tập, cạnh chỉ nối giữa 2 tập)"""
    result, _ = is_bipartite_with_coloring(graph)
    return result


def is_bipartite_with_coloring(graph: Graph) -> Tuple[bool, Dict[int, int]]:
    """Kiểm tra & trả về (is_bipartite, {vertex: color})"""
    vertices = graph.get_vertices()
    if not vertices:
        return True, {}
    
    color = {v: -1 for v in vertices}  # -1: chưa tô, 0/1: màu
    
    for start in vertices:
        if color[start] == -1:
            queue = deque([start])
            color[start] = 0
            
            while queue:
                u = queue.popleft()
                current_color = color[u]
                next_color = 1 - current_color
                
                for v in graph.get_neighbors(u):
                    if color[v] == -1:
                        color[v] = next_color
                        queue.append(v)
                    elif color[v] == current_color:
                        # Đỉnh kề cùng màu => không phải đồ thị 2 phía
                        return False, {}
    
    return True, color


def get_bipartite_sets(graph: Graph) -> Tuple[bool, List[int], List[int]]:
    """
    Lấy 2 tập đỉnh của đồ thị 2 phía
    
    Args:
        graph: Đồ thị cần phân tích
    Returns:
        Tuple (là_đồ_thị_2_phía, tập_1, tập_2)
    """
    is_bip, coloring = is_bipartite_with_coloring(graph)
    
    if not is_bip:
        return False, [], []
    
    set1 = [v for v, c in coloring.items() if c == 0]
    set2 = [v for v, c in coloring.items() if c == 1]
    
    return True, sorted(set1), sorted(set2)


def is_bipartite_with_callback(graph: Graph, 
                               callback: Callable[[int, int, str], None]) -> Tuple[bool, Dict[int, int]]:
    """
    Kiểm tra đồ thị 2 phía với callback để trực quan hóa
    
    Args:
        graph: Đồ thị cần kiểm tra
        callback: Hàm callback(vertex, color, state)
                 state: 'coloring', 'conflict', 'done'
    Returns:
        Tuple (là_đồ_thị_2_phía, cách_tô_màu)
    """
    vertices = graph.get_vertices()
    
    if not vertices:
        return True, {}
    
    color = {v: -1 for v in vertices}
    
    for start in vertices:
        if color[start] == -1:
            queue = deque([start])
            color[start] = 0
            callback(start, 0, 'coloring')
            
            while queue:
                u = queue.popleft()
                current_color = color[u]
                next_color = 1 - current_color
                
                for v in graph.get_neighbors(u):
                    if color[v] == -1:
                        color[v] = next_color
                        callback(v, next_color, 'coloring')
                        queue.append(v)
                    elif color[v] == current_color:
                        callback(v, current_color, 'conflict')
                        return False, {}
    
    callback(-1, -1, 'done')
    return True, color


def find_odd_cycle(graph: Graph) -> Optional[List[int]]:
    """
    Tìm chu trình lẻ trong đồ thị (nếu không phải đồ thị 2 phía)
    
    Một đồ thị là 2 phía khi và chỉ khi không có chu trình lẻ
    
    Args:
        graph: Đồ thị cần tìm
    Returns:
        Chu trình lẻ nếu tìm thấy, None nếu không
    """
    vertices = graph.get_vertices()
    
    if not vertices:
        return None
    
    color = {v: -1 for v in vertices}
    parent = {v: None for v in vertices}
    
    for start in vertices:
        if color[start] == -1:
            queue = deque([start])
            color[start] = 0
            
            while queue:
                u = queue.popleft()
                current_color = color[u]
                next_color = 1 - current_color
                
                for v in graph.get_neighbors(u):
                    if color[v] == -1:
                        color[v] = next_color
                        parent[v] = u
                        queue.append(v)
                    elif color[v] == current_color:
                        # Tìm thấy chu trình lẻ, truy vết đường đi
                        cycle = [v]
                        
                        # Truy vết từ u về start
                        current = u
                        while current != start and current is not None:
                            cycle.append(current)
                            current = parent[current]
                        
                        # Truy vết từ v về start
                        current = v
                        reverse_path = []
                        while current != start and current is not None:
                            reverse_path.append(current)
                            current = parent[current]
                        
                        # Ghép 2 đường đi để tạo chu trình
                        if reverse_path:
                            cycle.extend(reversed(reverse_path[1:]))
                        
                        return cycle
    
    return None


def is_complete_bipartite(graph: Graph) -> bool:
    """
    Kiểm tra đồ thị có phải là đồ thị 2 phía đầy đủ hay không
    
    Đồ thị 2 phía đầy đủ: Mọi đỉnh ở tập 1 đều kề với mọi đỉnh ở tập 2
    
    Args:
        graph: Đồ thị cần kiểm tra
    Returns:
        True nếu là đồ thị 2 phía đầy đủ
    """
    is_bip, set1, set2 = get_bipartite_sets(graph)
    
    if not is_bip:
        return False
    
    # Kiểm tra mọi cặp đỉnh giữa 2 tập có cạnh nối không
    for u in set1:
        for v in set2:
            if not graph.has_edge(u, v):
                return False
    
    return True
