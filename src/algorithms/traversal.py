"""Duyệt đồ thị: BFS (chiều rộng) & DFS (chiều sâu)"""
from typing import List, Dict, Set, Callable, Optional
from collections import deque
from src.core.graph import Graph


def bfs(graph: Graph, start: int) -> List[int]:
    """BFS - duyệt theo chiều rộng từ start, trả về thứ tự đỉnh"""
    if start not in graph.get_vertices():
        return []
    
    visited = set()
    queue = deque([start])
    result = []
    visited.add(start)
    
    while queue:
        current = queue.popleft()
        result.append(current)
        for neighbor in sorted(graph.get_neighbors(current)):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result


def dfs(graph: Graph, start: int) -> List[int]:
    """DFS - duyệt theo chiều sâu từ start, trả về thứ tự đỉnh"""
    if start not in graph.get_vertices():
        return []
    
    visited = set()
    stack = [start]
    result = []
    
    visited.add(start)
    
    while stack:
        current = stack.pop()
        result.append(current)
        for neighbor in reversed(sorted(graph.get_neighbors(current))):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    
    return result


def dfs_recursive(graph: Graph, start: int, 
                 visited: Optional[Set[int]] = None,
                 result: Optional[List[int]] = None) -> List[int]:
    """DFS đệ quy"""
    if visited is None:
        visited = set()
    if result is None:
        result = []
    
    if start in visited or start not in graph.get_vertices():
        return result
    
    visited.add(start)
    result.append(start)
    
    for neighbor in sorted(graph.get_neighbors(start)):
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, result)
    
    return result


def bfs_with_callback(graph: Graph, start: int, 
                     callback: Callable[[int, str], None]) -> List[int]:
    """BFS với callback(vertex, state) cho trực quan hóa"""
    if start not in graph.get_vertices():
        return []
    
    visited = set()
    queue = deque([start])
    result = []
    
    visited.add(start)
    callback(start, 'visiting')
    
    while queue:
        current = queue.popleft()
        result.append(current)
        callback(current, 'visited')
        
        for neighbor in sorted(graph.get_neighbors(current)):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                callback(neighbor, 'neighbor')
    
    return result


def dfs_with_callback(graph: Graph, start: int,
                     callback: Callable[[int, str], None]) -> List[int]:
    """DFS với callback(vertex, state) cho trực quan hóa"""
    if start not in graph.get_vertices():
        return []
    
    visited = set()
    stack = [start]
    result = []
    
    visited.add(start)
    callback(start, 'visiting')
    
    while stack:
        current = stack.pop()
        result.append(current)
        callback(current, 'visited')
        
        for neighbor in reversed(sorted(graph.get_neighbors(current))):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                callback(neighbor, 'neighbor')
    
    return result


def bfs_levels(graph: Graph, start: int) -> Dict[int, int]:
    """BFS trả về mức (level) của mỗi đỉnh: {vertex: level}"""
    if start not in graph.get_vertices():
        return {}
    
    levels = {start: 0}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        current_level = levels[current]
        
        for neighbor in graph.get_neighbors(current):
            if neighbor not in levels:
                levels[neighbor] = current_level + 1
                queue.append(neighbor)
    
    return levels


def bfs_shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
    """BFS tìm đường ngắn nhất (unweighted) - trả về path hoặc None"""
    if start not in graph.get_vertices() or end not in graph.get_vertices():
        return None
    if start == end:
        return [start]
    
    parent = {start: None}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parent[current]
            return list(reversed(path))
        
        for neighbor in graph.get_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None
