"""
Trực quan hóa các thuật toán đồ thị từng bước
"""
from typing import List, Tuple, Dict, Callable, Optional
from src.core.graph import Graph
from src.visualization.graph_drawer import GraphDrawer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.algorithms.traversal import bfs_with_callback, dfs_with_callback
from src.algorithms.shortest_path import dijkstra_with_callback
from src.algorithms.bipartite import is_bipartite_with_callback
from src.algorithms.minimum_spanning_tree import prim_with_callback, kruskal_with_callback
from src.algorithms.max_flow import ford_fulkerson_with_callback
from src.algorithms.eulerian import fleury_with_callback, hierholzer_with_callback
from src.utils.config import DEFAULT_ANIMATION_INTERVAL


class AlgorithmVisualizer:
    """Lớp trực quan hóa các thuật toán từng bước"""
    
    def __init__(self, graph: Graph):
        """
        Khởi tạo visualizer
        
        Args:
            graph: Đồ thị cần trực quan hóa
        """
        self.graph = graph
        self.drawer = GraphDrawer()
        self.steps = []  # Lưu các bước của thuật toán
    
    def visualize_prim(self, start: Optional[int] = None, 
                      interval: int = DEFAULT_ANIMATION_INTERVAL):
        """
        Trực quan hóa thuật toán Prim
        
        Args:
            start: Đỉnh bắt đầu
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(u: int, v: int, weight: float, state: str):
            """Lưu từng bước của thuật toán"""
            self.steps.append(('edge', u, v, weight, state))
        
        # Chạy thuật toán với callback
        mst_edges, total_weight = prim_with_callback(self.graph, start, callback)
        
        # Hiển thị kết quả
        print(f"\nThuật toán Prim:")
        print(f"Tổng trọng số MST: {total_weight:.2f}")
        print(f"Các cạnh trong MST:")
        for u, v, w in mst_edges:
            print(f"  ({u}, {v}) - Trọng số: {w:.2f}")
        
        # Vẽ kết quả cuối
        mst_edge_list = [(u, v) for u, v, _ in mst_edges]
        self.drawer.draw_with_highlight(
            self.graph,
            highlight_edges=mst_edge_list,
            title=f"Cây khung nhỏ nhất (Prim) - Tổng: {total_weight:.2f}"
        )
        self.drawer.show()
    
    def visualize_kruskal(self, interval: int = DEFAULT_ANIMATION_INTERVAL):
        """
        Trực quan hóa thuật toán Kruskal
        
        Args:
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(u: int, v: int, weight: float, state: str):
            self.steps.append(('edge', u, v, weight, state))
        
        mst_edges, total_weight = kruskal_with_callback(self.graph, callback)
        
        print(f"\nThuật toán Kruskal:")
        print(f"Tổng trọng số MST: {total_weight:.2f}")
        print(f"Các cạnh trong MST:")
        for u, v, w in mst_edges:
            print(f"  ({u}, {v}) - Trọng số: {w:.2f}")
        
        mst_edge_list = [(u, v) for u, v, _ in mst_edges]
        self.drawer.draw_with_highlight(
            self.graph,
            highlight_edges=mst_edge_list,
            title=f"Cây khung nhỏ nhất (Kruskal) - Tổng: {total_weight:.2f}"
        )
        self.drawer.show()
    
    def visualize_ford_fulkerson(self, source: int, sink: int,
                                 interval: int = DEFAULT_ANIMATION_INTERVAL):
        """
        Trực quan hóa thuật toán Ford-Fulkerson
        
        Args:
            source: Đỉnh nguồn
            sink: Đỉnh đích
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(path: List[int], flow: float):
            self.steps.append(('path', path, flow))
        
        max_flow, flow_dict = ford_fulkerson_with_callback(
            self.graph, source, sink, callback
        )
        
        print(f"\nThuật toán Ford-Fulkerson:")
        print(f"Luồng cực đại từ {source} đến {sink}: {max_flow:.2f}")
        print(f"Số đường tăng luồng: {len(self.steps)}")
        
        # Vẽ kết quả với các cạnh có luồng
        flow_edges = [(u, v) for (u, v), f in flow_dict.items() if f > 0]
        
        # Tạo danh sách đỉnh với source đầu, sink cuối
        flow_vertices = set([source, sink])
        for u, v in flow_edges:
            flow_vertices.add(u)
            flow_vertices.add(v)
        
        # Sắp xếp: source đầu, sink cuối, các đỉnh khác ở giữa
        vertex_list = [source]
        for v in flow_vertices:
            if v != source and v != sink:
                vertex_list.append(v)
        if sink != source:
            vertex_list.append(sink)
        
        self.drawer.draw_with_highlight(
            self.graph,
            highlight_vertices=vertex_list,
            highlight_edges=flow_edges,
            title=f"Luồng cực đại (Ford-Fulkerson): {max_flow:.2f}"
        )
        self.drawer.show()
    
    def visualize_fleury(self, interval: int = DEFAULT_ANIMATION_INTERVAL):
        """
        Trực quan hóa thuật toán Fleury
        
        Args:
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(u: int, v: int):
            self.steps.append(('edge', u, v))
        
        result = fleury_with_callback(self.graph, None, callback)
        
        if result:
            print(f"\nThuật toán Fleury:")
            print(f"Đường đi Euler gồm {len(result)} cạnh")
            print("Đường đi:", " → ".join([f"({u},{v})" for u, v in result]))
            
            # Trích xuất danh sách đỉnh theo thứ tự từ danh sách cạnh
            vertex_path = []
            if result:
                vertex_path.append(result[0][0])  # Đỉnh đầu tiên
                for u, v in result:
                    vertex_path.append(v)
            
            # Tạo dictionary với số thứ tự cho mỗi cạnh
            edge_order = {result[i]: i+1 for i in range(len(result))}
            
            self.drawer.draw_with_highlight(
                self.graph,
                highlight_vertices=vertex_path,
                highlight_edges=result,
                edge_order=edge_order,
                title="Đường đi Euler (Fleury)"
            )
            self.drawer.show()
        else:
            print("Đồ thị không có đường đi Euler")
    
    def visualize_hierholzer(self, interval: int = DEFAULT_ANIMATION_INTERVAL):
        """
        Trực quan hóa thuật toán Hierholzer
        
        Args:
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(u: int, v: int):
            self.steps.append(('edge', u, v))
        
        result = hierholzer_with_callback(self.graph, None, callback)
        
        if result:
            print(f"\nThuật toán Hierholzer:")
            print(f"Đường đi Euler gồm {len(result)} cạnh")
            print("Đường đi:", " → ".join([f"({u},{v})" for u, v in result]))
            
            # Trích xuất danh sách đỉnh theo thứ tự từ danh sách cạnh
            vertex_path = []
            if result:
                vertex_path.append(result[0][0])  # Đỉnh đầu tiên
                for u, v in result:
                    vertex_path.append(v)
            
            # Tạo dictionary với số thứ tự cho mỗi cạnh
            edge_order = {result[i]: i+1 for i in range(len(result))}
            
            self.drawer.draw_with_highlight(
                self.graph,
                highlight_vertices=vertex_path,
                highlight_edges=result,
                edge_order=edge_order,
                title="Đường đi Euler (Hierholzer)"
            )
            self.drawer.show()
        else:
            print("Đồ thị không có đường đi Euler")
    
    def visualize_bfs(self, start: int, interval: int = 500):
        """
        Trực quan hóa duyệt BFS
        
        Args:
            start: Đỉnh bắt đầu
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(vertex: int, state: str):
            self.steps.append(('vertex', vertex, state))
        
        result = bfs_with_callback(self.graph, start, callback)
        
        print(f"\nDuyệt BFS từ đỉnh {start}:")
        print("Thứ tự:", " → ".join(map(str, result)))
        
        self.drawer.draw_with_highlight(
            self.graph,
            highlight_vertices=result,
            title=f"Duyệt BFS từ đỉnh {start}"
        )
        self.drawer.show()
    
    def visualize_dfs(self, start: int, interval: int = 500):
        """
        Trực quan hóa duyệt DFS
        
        Args:
            start: Đỉnh bắt đầu
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(vertex: int, state: str):
            self.steps.append(('vertex', vertex, state))
        
        result = dfs_with_callback(self.graph, start, callback)
        
        print(f"\nDuyệt DFS từ đỉnh {start}:")
        print("Thứ tự:", " → ".join(map(str, result)))
        
        self.drawer.draw_with_highlight(
            self.graph,
            highlight_vertices=result,
            title=f"Duyệt DFS từ đỉnh {start}"
        )
        self.drawer.show()
    
    def visualize_shortest_path(self, start: int, end: int,
                               interval: int = 500):
        """
        Trực quan hóa tìm đường đi ngắn nhất
        
        Args:
            start: Đỉnh bắt đầu
            end: Đỉnh kết thúc
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(vertex: int, distance: float, state: str):
            self.steps.append(('vertex', vertex, distance, state))
        
        distances, parent = dijkstra_with_callback(self.graph, start, callback)
        
        # Truy vết đường đi
        if distances[end] != float('inf'):
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            
            print(f"\nĐường đi ngắn nhất từ {start} đến {end}:")
            print("Đường đi:", " → ".join(map(str, path)))
            print(f"Độ dài: {distances[end]:.2f}")
            
            # Tạo danh sách cạnh và số thứ tự
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            edge_order = {path_edges[i]: i+1 for i in range(len(path_edges))}
            
            self.drawer.draw_with_highlight(
                self.graph,
                highlight_vertices=path,
                highlight_edges=path_edges,
                edge_order=edge_order,
                title=f"Đường đi ngắn nhất: {start} → {end} (độ dài: {distances[end]:.2f})"
            )
            self.drawer.show()
        else:
            print(f"Không tìm thấy đường đi từ {start} đến {end}")
    
    def visualize_bipartite_check(self, interval: int = 500):
        """
        Trực quan hóa kiểm tra đồ thị 2 phía
        
        Args:
            interval: Khoảng thời gian giữa các bước (ms)
        """
        self.steps = []
        
        def callback(vertex: int, color: int, state: str):
            self.steps.append(('vertex', vertex, color, state))
        
        is_bip, coloring = is_bipartite_with_callback(self.graph, callback)
        
        if is_bip:
            print("\nKiểm tra đồ thị 2 phía:")
            print("Kết quả: Là đồ thị 2 phía")
            
            set1 = [v for v, c in coloring.items() if c == 0]
            set2 = [v for v, c in coloring.items() if c == 1]
            
            print(f"Tập 1: {sorted(set1)}")
            print(f"Tập 2: {sorted(set2)}")
            
            # Vẽ với 2 màu khác nhau (chỉ highlight tập 1)
            self.drawer.draw_with_highlight(
                self.graph,
                highlight_vertices=set1,
                title="Đồ thị 2 phía (Tập 1: Cam, Tập 2: Xanh)"
            )
            self.drawer.show()
        else:
            print("\nKiểm tra đồ thị 2 phía:")
            print("Kết quả: KHÔNG phải đồ thị 2 phía")
