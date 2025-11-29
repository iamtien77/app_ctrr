"""
Vẽ và trực quan hóa đồ thị
"""
import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Tuple, Dict, Optional
from src.core.graph import Graph, GraphType
from src.utils.config import (
    VERTEX_COLOR, VERTEX_HIGHLIGHT_COLOR, EDGE_COLOR, EDGE_HIGHLIGHT_COLOR,
    PATH_COLOR, VERTEX_SIZE, EDGE_WIDTH, EDGE_HIGHLIGHT_WIDTH,
    VERTEX_FONT_SIZE, EDGE_FONT_SIZE, DEFAULT_LAYOUT
)


class GraphDrawer:
    """Lớp vẽ và trực quan hóa đồ thị"""
    
    def __init__(self):
        """Khởi tạo GraphDrawer"""
        self.fig = None
        self.ax = None
    
    def _convert_to_networkx(self, graph: Graph) -> nx.Graph:
        """
        Chuyển đổi Graph sang NetworkX Graph
        
        Args:
            graph: Đồ thị cần chuyển đổi
        Returns:
            Đồ thị NetworkX
        """
        if graph.is_directed():
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        
        # Thêm các đỉnh
        G.add_nodes_from(graph.get_vertices())
        
        # Thêm các cạnh với trọng số
        for u, v, weight in graph.get_edges():
            G.add_edge(u, v, weight=weight)
        
        return G
    
    def _get_layout(self, G: nx.Graph, layout: str = DEFAULT_LAYOUT) -> Dict:
        """
        Lấy bố cục vị trí các đỉnh
        
        Args:
            G: Đồ thị NetworkX
            layout: Loại bố cục (spring, circular, random, shell, spectral)
        Returns:
            Dictionary {đỉnh: (x, y)}
        """
        if layout == "spring":
            return nx.spring_layout(G)
        elif layout == "circular":
            return nx.circular_layout(G)
        elif layout == "random":
            return nx.random_layout(G)
        elif layout == "shell":
            return nx.shell_layout(G)
        elif layout == "spectral":
            return nx.spectral_layout(G)
        else:
            return nx.spring_layout(G)
    
    def draw_graph(self, graph: Graph, layout: str = DEFAULT_LAYOUT, 
                   show_labels: bool = True, show_weights: bool = True,
                   title: str = "Đồ thị"):
        """
        Vẽ đồ thị cơ bản
        
        Args:
            graph: Đồ thị cần vẽ
            layout: Thuật toán bố cục (spring, circular, etc.)
            show_labels: Hiển thị nhãn đỉnh
            show_weights: Hiển thị trọng số cạnh
            title: Tiêu đề đồ thị
        """
        # Chuyển sang NetworkX
        G = self._convert_to_networkx(graph)
        
        # Tạo figure và axes
        if self.fig is None:
            self.fig, self.ax = plt.subplots(figsize=(10, 8))
        else:
            self.ax.clear()
        
        # Lấy bố cục
        pos = self._get_layout(G, layout)
        
        # Vẽ các cạnh
        nx.draw_networkx_edges(G, pos, ax=self.ax, 
                              edge_color=EDGE_COLOR,
                              width=EDGE_WIDTH,
                              arrows=graph.is_directed(),
                              arrowsize=20)
        
        # Vẽ các đỉnh
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                              node_color=VERTEX_COLOR,
                              node_size=VERTEX_SIZE)
        
        # Vẽ nhãn đỉnh
        if show_labels:
            nx.draw_networkx_labels(G, pos, ax=self.ax,
                                   font_size=VERTEX_FONT_SIZE,
                                   font_color='white',
                                   font_weight='bold')
        
        # Vẽ trọng số cạnh
        if show_weights:
            edge_labels = nx.get_edge_attributes(G, 'weight')
            edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}
            nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=self.ax,
                                        font_size=EDGE_FONT_SIZE)
        
        self.ax.set_title(title, fontsize=16, fontweight='bold')
        self.ax.axis('off')
        plt.tight_layout()
    
    def draw_with_highlight(self, graph: Graph, 
                          highlight_vertices: List[int] = None,
                          highlight_edges: List[Tuple[int, int]] = None,
                          edge_order: Dict[Tuple[int, int], int] = None,
                          layout: str = DEFAULT_LAYOUT,
                          title: str = "Đồ thị với đánh dấu"):
        """
        Vẽ đồ thị với các đỉnh và cạnh được tô sáng
        
        Args:
            graph: Đồ thị cần vẽ
            highlight_vertices: Danh sách đỉnh cần tô sáng (đỉnh đầu là START, cuối là END)
            highlight_edges: Danh sách cạnh cần tô sáng
            edge_order: Dictionary {(u,v): số_thứ_tự} để hiển thị thứ tự đi qua cạnh
            layout: Thuật toán bố cục
            title: Tiêu đề
        """
        if highlight_vertices is None:
            highlight_vertices = []
        if highlight_edges is None:
            highlight_edges = []
        if edge_order is None:
            edge_order = {}
        
        G = self._convert_to_networkx(graph)
        
        if self.fig is None:
            self.fig, self.ax = plt.subplots(figsize=(10, 8))
        else:
            self.ax.clear()
        
        pos = self._get_layout(G, layout)
        
        # Vẽ các cạnh thường
        all_edges = list(G.edges())
        normal_edges = [e for e in all_edges if e not in highlight_edges 
                       and (e[1], e[0]) not in highlight_edges]
        
        if normal_edges:
            nx.draw_networkx_edges(G, pos, edgelist=normal_edges, ax=self.ax,
                                  edge_color='gray',
                                  width=EDGE_WIDTH,
                                  alpha=0.4,
                                  arrows=graph.is_directed(),
                                  arrowsize=15)
        
        # Vẽ các cạnh được tô sáng
        if highlight_edges:
            nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, ax=self.ax,
                                  edge_color='#FF3333',
                                  width=EDGE_HIGHLIGHT_WIDTH * 1.5,
                                  alpha=0.9,
                                  arrows=graph.is_directed(),
                                  arrowsize=20)
        
        # Vẽ các đỉnh với màu sắc khác nhau
        normal_vertices = [v for v in G.nodes() if v not in highlight_vertices]
        
        if normal_vertices:
            nx.draw_networkx_nodes(G, pos, nodelist=normal_vertices, ax=self.ax,
                                  node_color='#ADD8E6',
                                  node_size=VERTEX_SIZE,
                                  edgecolors='black',
                                  linewidths=2)
        
        # Vẽ đỉnh highlight với màu khác nhau cho START, END, và trung gian
        if highlight_vertices:
            for i, vertex in enumerate(highlight_vertices):
                if i == 0:
                    # ĐIỂM ĐẦU (START)
                    color = '#00CC44'
                    size = VERTEX_SIZE * 1.4
                    linewidth = 4
                elif i == len(highlight_vertices) - 1 and len(highlight_vertices) > 1:
                    # ĐIỂM CUỐI (END)
                    color = '#FF3333'
                    size = VERTEX_SIZE * 1.4
                    linewidth = 4
                else:
                    # ĐIỂM TRUNG GIAN
                    color = '#FFD700'
                    size = VERTEX_SIZE * 1.1
                    linewidth = 2.5
                
                nx.draw_networkx_nodes(G, pos, nodelist=[vertex], ax=self.ax,
                                      node_color=color,
                                      node_size=size,
                                      edgecolors='black',
                                      linewidths=linewidth)
        
        # Vẽ nhãn
        nx.draw_networkx_labels(G, pos, ax=self.ax,
                               font_size=VERTEX_FONT_SIZE,
                               font_color='black',
                               font_weight='bold')
        
        # Thêm nhãn START/END
        if highlight_vertices and len(highlight_vertices) > 0:
            start_node = highlight_vertices[0]
            start_pos = pos[start_node]
            self.ax.text(start_pos[0], start_pos[1] + 0.15, 'START',
                       ha='center', va='bottom', fontsize=11,
                       fontweight='bold', color='darkgreen',
                       bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                               edgecolor='darkgreen', linewidth=2.5, alpha=0.95))
            
            if len(highlight_vertices) > 1:
                end_node = highlight_vertices[-1]
                if start_node != end_node:
                    end_pos = pos[end_node]
                    self.ax.text(end_pos[0], end_pos[1] + 0.15, 'END',
                               ha='center', va='bottom', fontsize=11,
                               fontweight='bold', color='darkred',
                               bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                                       edgecolor='darkred', linewidth=2.5, alpha=0.95))
        
        # Vẽ trọng số cạnh
        edge_labels = nx.get_edge_attributes(G, 'weight')
        edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=self.ax,
                                    font_size=EDGE_FONT_SIZE)
        
        # Vẽ số thứ tự trên các cạnh highlight
        if edge_order:
            order_labels = {}
            for edge, order in edge_order.items():
                # Tính vị trí offset để không đè lên trọng số
                u, v = edge
                if (u, v) in pos and (v, u) in pos or v in pos:
                    # Vị trí cho số thứ tự (offset về phía ngoài)
                    order_labels[edge] = f"[{order}]"
            
            # Vẽ số thứ tự với màu khác và offset
            for edge, label in order_labels.items():
                u, v = edge
                x = (pos[u][0] + pos[v][0]) / 2
                y = (pos[u][1] + pos[v][1]) / 2
                
                # Tính vector vuông góc để offset
                dx = pos[v][0] - pos[u][0]
                dy = pos[v][1] - pos[u][1]
                length = (dx**2 + dy**2)**0.5
                if length > 0:
                    offset_x = -dy / length * 0.08  # Offset vuông góc
                    offset_y = dx / length * 0.08
                else:
                    offset_x = offset_y = 0
                
                self.ax.text(x + offset_x, y + offset_y, label,
                           ha='center', va='center',
                           fontsize=10, fontweight='bold',
                           color='white',
                           bbox=dict(boxstyle='circle,pad=0.3',
                                   facecolor='#FF6600',
                                   edgecolor='black',
                                   linewidth=2,
                                   alpha=0.95))
        
        # Thêm chú thích
        if highlight_vertices and len(highlight_vertices) > 0:
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='#00CC44', edgecolor='black', linewidth=2, label='Điểm đầu (START)'),
            ]
            if len(highlight_vertices) > 1:
                legend_elements.append(Patch(facecolor='#FF3333', edgecolor='black', linewidth=2, label='Điểm cuối (END)'))
            if len(highlight_vertices) > 2:
                legend_elements.insert(1, Patch(facecolor='#FFD700', edgecolor='black', linewidth=2, label='Điểm trung gian'))
            
            self.ax.legend(handles=legend_elements, loc='upper right',
                         fontsize=10, framealpha=0.95, edgecolor='black')
        
        self.ax.set_title(title, fontsize=16, fontweight='bold')
        self.ax.axis('off')
        plt.tight_layout()
    
    def draw_path(self, graph: Graph, path: List[int], 
                 layout: str = DEFAULT_LAYOUT,
                 title: str = "Đồ thị với đường đi"):
        """
        Vẽ đồ thị với đường đi được tô sáng
        
        Args:
            graph: Đồ thị cần vẽ
            path: Danh sách các đỉnh trong đường đi
            layout: Thuật toán bố cục
            title: Tiêu đề
        """
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        self.draw_with_highlight(graph, 
                                highlight_vertices=path,
                                highlight_edges=path_edges,
                                layout=layout,
                                title=title)
    
    def save_graph_image(self, graph: Graph, filepath: str,
                        layout: str = DEFAULT_LAYOUT,
                        dpi: int = 300):
        """
        Lưu hình ảnh đồ thị ra file
        
        Args:
            graph: Đồ thị cần lưu
            filepath: Đường dẫn file
            layout: Thuật toán bố cục
            dpi: Độ phân giải
        """
        self.draw_graph(graph, layout=layout)
        plt.savefig(filepath, dpi=dpi, bbox_inches='tight')
        print(f"Đã lưu hình ảnh đồ thị vào: {filepath}")
    
    def show(self):
        """Hiển thị đồ thị"""
        plt.show()
    
    def close(self):
        """Đóng figure"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
