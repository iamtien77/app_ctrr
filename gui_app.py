"""GUI ứng dụng quản lý đồ thị - tkinter & matplotlib"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import networkx as nx

from src.core.graph import Graph, GraphType
from src.algorithms.traversal import bfs, dfs
from src.algorithms.shortest_path import dijkstra, bellman_ford, find_shortest_path
from src.algorithms.bipartite import is_bipartite, get_bipartite_sets
from src.algorithms.minimum_spanning_tree import prim, kruskal
from src.algorithms.max_flow import ford_fulkerson
from src.algorithms.eulerian import is_eulerian, fleury, hierholzer
from src.core.representations import AdjacencyMatrix, AdjacencyList, EdgeList
from src.core.file_io import save_graph, load_graph
from src.utils.helpers import get_graph_info, generate_random_graph
from src.utils.config import WINDOW_TITLE
from src.visualization.algorithm_visualizer import AlgorithmVisualizer


class GraphGUI:
    """Giao diện chính ứng dụng đồ thị"""
    
    def __init__(self, root):
        """Khởi tạo GUI (root: cửa sổ tkinter)"""
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry("1400x900")
        self.root.configure(bg='#E6F3FF')  # Màu xanh nhạt
        
        self.graph = Graph(GraphType.UNDIRECTED)  # Đồ thị hiện tại
        self.pos = {}  # Vị trí các đỉnh (để kéo thả)
        self.dragging_node = None  # Đỉnh đang được kéo
        
        # Trạng thái thu/mở panel
        self.left_panel_visible = True
        self.right_panel_visible = True
        
        self.create_widgets()
        self.update_graph_display()
        
    def create_widgets(self):
        """Tạo các widget giao diện"""
        # Cấu hình root
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # PanedWindow chính ngang (horizontal)
        self.main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, 
                                         sashwidth=8, sashrelief=tk.RAISED,
                                         bg='#4A90E2')
        self.main_paned.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Panel trái (điều khiển)
        self.left_frame = tk.Frame(self.main_paned, bg='#E6F3FF')
        self.create_control_panel(self.left_frame)
        self.main_paned.add(self.left_frame, minsize=200, width=300)
        
        # Panel giữa (đồ thị)
        self.center_frame = tk.Frame(self.main_paned, bg='#E6F3FF')
        self.create_graph_panel(self.center_frame)
        self.main_paned.add(self.center_frame, minsize=400, width=700)
        
        # Panel phải (thông tin)
        self.right_frame = tk.Frame(self.main_paned, bg='#E6F3FF')
        self.create_info_panel(self.right_frame)
        self.main_paned.add(self.right_frame, minsize=200, width=300)
        
        self.create_toggle_buttons()  # Nút thu/mở
        
    def create_control_panel(self, parent):
        """Tạo panel điều khiển (trái)"""
        # Cấu hình parent
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        # Tạo frame chứa với thanh cuộn
        self.control_outer = ttk.LabelFrame(parent, text="Điều khiển", padding="5")
        self.control_outer.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Canvas và scrollbar
        canvas = tk.Canvas(self.control_outer, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.control_outer, orient="vertical", command=canvas.yview)
        
        # Frame chứa nội dung bên trong canvas
        control_frame = ttk.Frame(canvas)
        
        # Cấu hình canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar và canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Tạo window trong canvas
        canvas_frame = canvas.create_window((0, 0), window=control_frame, anchor="nw")
        
        # Hàm cập nhật scroll region
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Cập nhật width của frame bên trong để khớp với canvas
            canvas.itemconfig(canvas_frame, width=canvas.winfo_width())
        
        control_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        # Bind scroll bằng chuột
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # === Tạo đồ thị ===
        ttk.Label(control_frame, text="Tạo đồ thị:", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        ttk.Label(control_frame, text="Loại:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.graph_type_var = tk.StringVar(value="undirected")
        ttk.Radiobutton(control_frame, text="Vô hướng", variable=self.graph_type_var, value="undirected").grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(control_frame, text="Có hướng", variable=self.graph_type_var, value="directed").grid(row=2, column=1, sticky=tk.W)
        
        ttk.Button(control_frame, text="Tạo đồ thị mới", command=self.new_graph, width=20).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(control_frame, text="Tạo đồ thị ngẫu nhiên", command=self.random_graph, width=20).grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # === Thêm đỉnh/cạnh ===
        ttk.Label(control_frame, text="Thêm đỉnh/cạnh:", font=('Arial', 10, 'bold')).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(control_frame, text="Đỉnh:").grid(row=7, column=0, sticky=tk.W, pady=2)
        self.vertex_entry = ttk.Entry(control_frame, width=15)
        self.vertex_entry.grid(row=7, column=1, pady=2)
        ttk.Button(control_frame, text="Thêm đỉnh", command=self.add_vertex, width=20).grid(row=8, column=0, columnspan=2, pady=2)
        
        ttk.Label(control_frame, text="Cạnh (u,v,w):").grid(row=9, column=0, sticky=tk.W, pady=2)
        edge_frame = ttk.Frame(control_frame)
        edge_frame.grid(row=10, column=0, columnspan=2, pady=2)
        
        self.edge_u = ttk.Entry(edge_frame, width=5)
        self.edge_u.pack(side=tk.LEFT, padx=2)
        ttk.Label(edge_frame, text="→").pack(side=tk.LEFT)
        self.edge_v = ttk.Entry(edge_frame, width=5)
        self.edge_v.pack(side=tk.LEFT, padx=2)
        ttk.Label(edge_frame, text="w:").pack(side=tk.LEFT)
        self.edge_w = ttk.Entry(edge_frame, width=5)
        self.edge_w.pack(side=tk.LEFT, padx=2)
        self.edge_w.insert(0, "1")
        
        ttk.Button(control_frame, text="Thêm cạnh", command=self.add_edge, width=20).grid(row=11, column=0, columnspan=2, pady=2)
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=12, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # === Thuật toán ===
        ttk.Label(control_frame, text="Thuật toán:", font=('Arial', 10, 'bold')).grid(row=13, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        algorithms = [
            ("Duyệt BFS", self.run_bfs),
            ("Duyệt DFS", self.run_dfs),
            ("Đường đi ngắn nhất", self.run_shortest_path),
            ("Kiểm tra 2 phía", self.run_bipartite),
            ("Cây khung nhỏ nhất", self.run_mst),
            ("Luồng cực đại", self.run_max_flow),
            ("Đường đi Euler", self.run_euler),
        ]
        
        row = 14
        for name, command in algorithms:
            ttk.Button(control_frame, text=name, command=command, width=20).grid(row=row, column=0, columnspan=2, pady=2)
            row += 1
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # === Trực quan hóa nâng cao ===
        ttk.Label(control_frame, text="Trực quan hóa:", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        row += 1
        
        viz_algorithms = [
            ("Visualize Prim", self.visualize_prim),
            ("Visualize Kruskal", self.visualize_kruskal),
            ("Visualize Ford-Fulkerson", self.visualize_ford_fulkerson),
            ("Visualize Fleury", self.visualize_fleury),
            ("Visualize Hierholzer", self.visualize_hierholzer),
        ]
        
        for name, command in viz_algorithms:
            ttk.Button(control_frame, text=name, command=command, width=20).grid(row=row, column=0, columnspan=2, pady=2)
            row += 1
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # === Biểu diễn đồ thị ===
        ttk.Label(control_frame, text="Biểu diễn:", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        row += 1
        ttk.Button(control_frame, text="Xem biểu diễn", command=self.show_representations, width=20).grid(row=row, column=0, columnspan=2, pady=2)
        row += 1
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # === Lưu/Tải file ===
        ttk.Label(control_frame, text="File:", font=('Arial', 10, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        row += 1
        ttk.Button(control_frame, text="Lưu đồ thị", command=self.save_graph_file, width=20).grid(row=row, column=0, columnspan=2, pady=2)
        row += 1
        ttk.Button(control_frame, text="Tải đồ thị", command=self.load_graph_file, width=20).grid(row=row, column=0, columnspan=2, pady=2)
        
    def create_graph_panel(self, parent):
        """Tạo panel vẽ đồ thị (giữa)"""
        # Cấu hình parent
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        graph_frame = ttk.LabelFrame(parent, text="Đồ thị", padding="10")
        graph_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        # Matplotlib figure & canvas
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Kết nối sự kiện chuột để kéo thả đỉnh
        self.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        
        toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        toolbar.update()
        
    def create_toggle_buttons(self):
        """Tạo nút thu/mở panel"""
        # Nút thu/mở panel trái
        self.left_toggle_btn = tk.Button(self.left_frame, text="◀", command=self.toggle_left_panel,
                                        bg='#4A90E2', fg='white', font=('Arial', 10, 'bold'),
                                        width=2, relief=tk.RAISED)
        self.left_toggle_btn.place(x=5, y=5)
        
        # Nút thu/mở panel phải
        self.right_toggle_btn = tk.Button(self.right_frame, text="▶", command=self.toggle_right_panel,
                                         bg='#4A90E2', fg='white', font=('Arial', 10, 'bold'),
                                         width=2, relief=tk.RAISED)
        self.right_toggle_btn.place(relx=1.0, x=-30, y=5)
    
    def toggle_left_panel(self):
        """Thu/mở panel trái"""
        if self.left_panel_visible:
            self.main_paned.forget(self.left_frame)
            self.left_toggle_btn.place_forget()
            self.left_toggle_btn = tk.Button(self.center_frame, text="▶", command=self.toggle_left_panel,
                                            bg='#4A90E2', fg='white', font=('Arial', 10, 'bold'),
                                            width=2, relief=tk.RAISED)
            self.left_toggle_btn.place(x=5, y=5)
        else:
            # Thêm lại panel trái vào vị trí đầu tiên
            panes = list(self.main_paned.panes())
            self.main_paned.add(self.left_frame, before=panes[0] if panes else None)
            self.left_toggle_btn.place_forget()
            self.left_toggle_btn = tk.Button(self.left_frame, text="◀", command=self.toggle_left_panel,
                                            bg='#4A90E2', fg='white', font=('Arial', 10, 'bold'),
                                            width=2, relief=tk.RAISED)
            self.left_toggle_btn.place(x=5, y=5)
        self.left_panel_visible = not self.left_panel_visible
    
    def toggle_right_panel(self):
        """Thu/mở panel phải"""
        if self.right_panel_visible:
            self.main_paned.forget(self.right_frame)
            self.right_toggle_btn.place_forget()
            self.right_toggle_btn = tk.Button(self.center_frame, text="◀", command=self.toggle_right_panel,
                                             bg='#4A90E2', fg='white', font=('Arial', 10, 'bold'),
                                             width=2, relief=tk.RAISED)
            self.right_toggle_btn.place(relx=1.0, x=-30, y=5)
        else:
            self.main_paned.add(self.right_frame)
            self.right_toggle_btn.place_forget()
            self.right_toggle_btn = tk.Button(self.right_frame, text="▶", command=self.toggle_right_panel,
                                             bg='#4A90E2', fg='white', font=('Arial', 10, 'bold'),
                                             width=2, relief=tk.RAISED)
            self.right_toggle_btn.place(relx=1.0, x=-30, y=5)
        self.right_panel_visible = not self.right_panel_visible
    
    def create_info_panel(self, parent):
        """Tạo panel thông tin & kết quả (phải)"""
        # Cấu hình parent
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        self.info_outer = ttk.LabelFrame(parent, text="Thông tin & Kết quả", padding="10")
        self.info_outer.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        info_frame = self.info_outer
        self.info_outer.columnconfigure(0, weight=1)
        self.info_outer.rowconfigure(1, weight=1)
        
        ttk.Label(self.info_outer, text="Thông tin đồ thị:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.info_text = scrolledtext.ScrolledText(self.info_outer, width=35, height=10, wrap=tk.WORD)
        self.info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Kết quả thuật toán
        ttk.Label(self.info_outer, text="Kết quả:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.result_text = scrolledtext.ScrolledText(self.info_outer, width=35, height=15, wrap=tk.WORD)
        self.result_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def new_graph(self):
        """Tạo đồ thị mới rỗng"""
        graph_type = GraphType.DIRECTED if self.graph_type_var.get() == "directed" else GraphType.UNDIRECTED
        self.graph = Graph(graph_type)
        self.update_graph_display()
        self.log_result("Đã tạo đồ thị mới")
        
    def random_graph(self):
        """Tạo đồ thị ngẫu nhiên"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tạo đồ thị ngẫu nhiên")
        dialog.geometry("350x220")
        
        ttk.Label(dialog, text="Số đỉnh:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        vertices_entry = ttk.Entry(dialog, width=15)
        vertices_entry.insert(0, "10")
        vertices_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Xác suất cạnh (0-1):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        prob_entry = ttk.Entry(dialog, width=15)
        prob_entry.insert(0, "0.3")
        prob_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Tùy chọn loại tên đỉnh
        ttk.Label(dialog, text="Tên đỉnh:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        vertex_type_var = tk.StringVar(value="number")
        ttk.Radiobutton(dialog, text="Số (0, 1, 2...)", variable=vertex_type_var, value="number").grid(row=2, column=1, sticky=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Chữ hoa (A, B, C...)", variable=vertex_type_var, value="upper").grid(row=3, column=1, sticky=tk.W, padx=10)
        ttk.Radiobutton(dialog, text="Chữ thường (a, b, c...)", variable=vertex_type_var, value="lower").grid(row=4, column=1, sticky=tk.W, padx=10)
        
        def create():
            try:
                num_vertices = int(vertices_entry.get())
                edge_prob = float(prob_entry.get())
                vertex_type = vertex_type_var.get()
                
                if num_vertices <= 0 or edge_prob < 0 or edge_prob > 1:
                    messagebox.showerror("Lỗi", "Giá trị không hợp lệ!")
                    return
                
                if vertex_type in ["upper", "lower"] and num_vertices > 26:
                    messagebox.showerror("Lỗi", "Tên chữ cái chỉ hỗ trợ tối đa 26 đỉnh!")
                    return
                
                graph_type = GraphType.DIRECTED if self.graph_type_var.get() == "directed" else GraphType.UNDIRECTED
                self.graph = Graph(graph_type)
                
                # Tạo danh sách tên đỉnh
                if vertex_type == "upper":
                    vertices = [chr(65 + i) for i in range(num_vertices)]  # A, B, C...
                elif vertex_type == "lower":
                    vertices = [chr(97 + i) for i in range(num_vertices)]  # a, b, c...
                else:
                    vertices = list(range(num_vertices))  # 0, 1, 2...
                
                # Thêm đỉnh
                for v in vertices:
                    self.graph.add_vertex(v)
                
                # Thêm cạnh ngẫu nhiên
                import random
                for i, u in enumerate(vertices):
                    for j, v in enumerate(vertices):
                        if i < j or (graph_type == GraphType.DIRECTED and i != j):
                            if random.random() < edge_prob:
                                weight = round(random.uniform(1, 10), 1)
                                self.graph.add_edge(u, v, weight)
                
                self.update_graph_display()
                vertex_name = {"number": "số", "upper": "chữ hoa", "lower": "chữ thường"}[vertex_type]
                self.log_result(f"Đã tạo đồ thị ngẫu nhiên với {num_vertices} đỉnh ({vertex_name})")
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
        
        ttk.Button(dialog, text="Tạo", command=create).grid(row=5, column=0, columnspan=2, pady=15)
        
    def add_vertex(self):
        """Thêm đỉnh (chấp nhận số hoặc chữ)"""
        try:
            vertex_str = self.vertex_entry.get().strip()
            if not vertex_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên đỉnh!")
                return
            
            # Tự động chuyển: số -> int, chữ -> string
            try:
                vertex = int(vertex_str)
            except ValueError:
                vertex = vertex_str
            
            self.graph.add_vertex(vertex)
            self.update_graph_display()
            self.log_result(f"Đã thêm đỉnh {vertex}")
            self.vertex_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def add_edge(self):
        """Thêm cạnh (chấp nhận số hoặc chữ)"""
        try:
            u_str = self.edge_u.get().strip()
            v_str = self.edge_v.get().strip()
            
            if not u_str or not v_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh đầu và đỉnh cuối!")
                return
            
            # Tự động chuyển: số -> int, chữ -> string
            try:
                u = int(u_str)
            except ValueError:
                u = u_str
            
            try:
                v = int(v_str)
            except ValueError:
                v = v_str
            
            w = float(self.edge_w.get())
            
            self.graph.add_edge(u, v, w)
            self.update_graph_display()
            self.log_result(f"Đã thêm cạnh ({u}, {v}) với trọng số {w}")
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ cho trọng số!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def update_graph_display(self, highlight_path=None, highlight_edges=None):
        """Vẽ lại đồ thị (highlight_path: đỉnh, highlight_edges: cạnh)"""
        self.ax.clear()
        
        if self.graph.vertex_count() == 0:
            self.ax.text(0.5, 0.5, 'Đồ thị rỗng', 
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform=self.ax.transAxes,
                        fontsize=14)
        else:
            # Chuyển đổi sang NetworkX
            G = nx.DiGraph() if self.graph.graph_type == GraphType.DIRECTED else nx.Graph()
            
            for vertex in self.graph.get_vertices():
                G.add_node(vertex)
            
            for u, v, w in self.graph.get_edges():
                G.add_edge(u, v, weight=w)
            
            # Layout tối ưu theo số đỉnh - DÃN RỘNG TỐI ĐA
            num_nodes = G.number_of_nodes()
            
            # Sử dụng vị trí đã lưu nếu có, nếu không tạo mới
            if not self.pos or set(G.nodes()) != set(self.pos.keys()):
                if num_nodes > 50:
                    # Nhiều đỉnh: kamada_kawai với scale lớn
                    try:
                        self.pos = nx.kamada_kawai_layout(G, scale=5)
                    except:
                        self.pos = nx.spring_layout(G, k=10/num_nodes**0.5, iterations=150, seed=42)
                elif num_nodes > 15:
                    # Trung bình: spring với k rất lớn để dãn rộng
                    self.pos = nx.spring_layout(G, k=5, iterations=100, seed=42)
                else:
                    # Ít đỉnh: circular hoặc spring dãn rộng
                    if num_nodes <= 10:
                        self.pos = nx.circular_layout(G, scale=2)  # Bố trí tròn đều
                    else:
                        self.pos = nx.spring_layout(G, k=4, iterations=80, seed=42)
            
            pos = self.pos
            
            # Vẽ các cạnh
            all_edges = list(G.edges())
            
            # Cạnh thường
            normal_edges = all_edges
            if highlight_edges:
                normal_edges = [(u, v) for u, v in all_edges if (u, v) not in highlight_edges and (v, u) not in highlight_edges]
            
            # Độ dày cạnh tự động
            edge_width = 1.5 if num_nodes > 20 else 2
            
            # Vẽ cạnh thường (mờ hơn khi nhiều đỉnh)
            if normal_edges:
                alpha = 0.4 if num_nodes > 20 else 0.6
                nx.draw_networkx_edges(G, pos, edgelist=normal_edges, ax=self.ax,
                                      arrows=self.graph.graph_type == GraphType.DIRECTED,
                                      edge_color='gray', width=edge_width, alpha=alpha,
                                      arrowsize=15, arrowstyle='->', connectionstyle='arc3,rad=0.1')
            
            # Vẽ cạnh highlight (nổi bật)
            if highlight_edges:
                nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, ax=self.ax,
                                      arrows=self.graph.graph_type == GraphType.DIRECTED,
                                      edge_color='red', width=edge_width*2, alpha=0.9,
                                      arrowsize=20, arrowstyle='->', connectionstyle='arc3,rad=0.1')
            
            # Màu đỉnh: XANH LÁ ĐẬM(đầu), ĐỎ ĐẬM(cuối), VÀNG(giữa), XANH NHẠT(thường)
            node_colors = []
            node_sizes = []
            node_borders = []
            
            # Kích thước đỉnh & font tự động
            base_node_size = max(300, min(1000, 6000 // num_nodes))
            font_size = max(9, min(16, 140 // num_nodes**0.5))
            
            for node in G.nodes():
                if highlight_path and node in highlight_path:
                    if node == highlight_path[0]:
                        # ĐIỂM ĐẦU: Xanh lá đậm, kích thước lớn hơn, viền dày
                        node_colors.append('#00CC44')  # Xanh lá sáng
                        node_sizes.append(base_node_size * 1.3)
                        node_borders.append(4)
                    elif node == highlight_path[-1]:
                        # ĐIỂM CUỐI: Đỏ đậm, kích thước lớn hơn, viền dày
                        node_colors.append('#FF3333')  # Đỏ sáng
                        node_sizes.append(base_node_size * 1.3)
                        node_borders.append(4)
                    else:
                        # ĐIỂM TRUNG GIAN: Vàng
                        node_colors.append('#FFD700')  # Vàng gold
                        node_sizes.append(base_node_size)
                        node_borders.append(2.5)
                else:
                    # ĐIỂM THƯỜNG: Xanh nhạt
                    node_colors.append('#ADD8E6')  # Xanh nhạt
                    node_sizes.append(base_node_size)
                    node_borders.append(2)
            
            # Vẽ đỉnh với kích thước và viền khác nhau
            for i, node in enumerate(G.nodes()):
                nx.draw_networkx_nodes(G, pos, nodelist=[node], ax=self.ax,
                                      node_color=[node_colors[i]],
                                      node_size=node_sizes[i],
                                      edgecolors='black',
                                      linewidths=node_borders[i],
                                      alpha=0.95)
            
            nx.draw_networkx_labels(G, pos, ax=self.ax,
                                   font_size=int(font_size),
                                   font_weight='bold')
            
            # Thêm nhãn START/END cho điểm đầu và cuối
            if highlight_path and len(highlight_path) > 0:
                start_node = highlight_path[0]
                end_node = highlight_path[-1]
                
                # Nhãn START
                start_pos = pos[start_node]
                self.ax.text(start_pos[0], start_pos[1] + 0.15, 'START', 
                           ha='center', va='bottom', fontsize=int(font_size * 0.8),
                           fontweight='bold', color='darkgreen',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                   edgecolor='darkgreen', linewidth=2, alpha=0.9))
                
                # Nhãn END (chỉ nếu khác START)
                if start_node != end_node:
                    end_pos = pos[end_node]
                    self.ax.text(end_pos[0], end_pos[1] + 0.15, 'END',
                               ha='center', va='bottom', fontsize=int(font_size * 0.8),
                               fontweight='bold', color='darkred',
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                       edgecolor='darkred', linewidth=2, alpha=0.9))
            
            # Trọng số cạnh (ẩn nếu quá nhiều)
            if num_nodes <= 30:
                edge_labels = nx.get_edge_attributes(G, 'weight')
                edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}
                edge_font_size = max(6, min(10, 100 // num_nodes**0.5))
                nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=self.ax, font_size=int(edge_font_size))
            
            # Thêm chú thích nếu có highlight
            if highlight_path and len(highlight_path) > 0:
                from matplotlib.patches import Patch
                legend_elements = [
                    Patch(facecolor='#00CC44', edgecolor='black', linewidth=2, label='Điểm đầu'),
                    Patch(facecolor='#FF3333', edgecolor='black', linewidth=2, label='Điểm cuối'),
                ]
                if len(highlight_path) > 2:
                    legend_elements.insert(1, Patch(facecolor='#FFD700', edgecolor='black', linewidth=2, label='Điểm trung gian'))
                
                self.ax.legend(handles=legend_elements, loc='upper right', 
                             fontsize=10, framealpha=0.9, edgecolor='black')
        
        self.ax.axis('off')
        self.canvas.draw()
        self.update_info()
    
    def update_info(self):
        """Cập nhật thông tin đồ thị"""
        self.info_text.delete(1.0, tk.END)
        
        if self.graph.vertex_count() == 0:
            self.info_text.insert(tk.END, "Đồ thị rỗng\n")
            return
        
        info = get_graph_info(self.graph)
        
        info_str = f"""Loại: {info['graph_type']}
Số đỉnh: {info['vertex_count']}
Số cạnh: {info['edge_count']}
Bậc TB: {info['avg_degree']:.2f}
Bậc min: {info['min_degree']}
Bậc max: {info['max_degree']}
Tổng trọng số: {info['total_weight']:.2f}
Liên thông: {'Có' if info['is_connected'] else 'Không'}
"""
        
        if info['isolated_vertices']:
            info_str += f"\nĐỉnh cô lập: {info['isolated_vertices']}"
        
        self.info_text.insert(tk.END, info_str)
    
    def log_result(self, message):
        """Ghi kết quả vào text box"""
        self.result_text.insert(tk.END, f"\n{'='*40}\n{message}\n")
        self.result_text.see(tk.END)
    
    def get_start_vertex(self):
        """Hỏi người dùng chọn đỉnh bắt đầu"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Chọn đỉnh")
        dialog.geometry("250x100")
        
        ttk.Label(dialog, text="Nhập đỉnh bắt đầu:").pack(pady=10)
        entry = ttk.Entry(dialog)
        entry.pack(pady=5)
        
        result = [None]
        
        def ok():
            vertex_str = entry.get().strip()
            if not vertex_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên đỉnh!")
                return
            
            # Thử chuyển sang số, nếu không được thì giữ nguyên chuỗi
            try:
                vertex = int(vertex_str)
            except ValueError:
                vertex = vertex_str
            
            if vertex not in self.graph.get_vertices():
                messagebox.showerror("Lỗi", "Đỉnh không tồn tại!")
                return
            
            result[0] = vertex
            dialog.destroy()
        
        ttk.Button(dialog, text="OK", command=ok).pack(pady=5)
        dialog.wait_window()
        
        return result[0]
    
    def run_bfs(self):
        """Duyệt BFS và hiển thị đường đi"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        start = self.get_start_vertex()
        if start is not None:
            result = bfs(self.graph, start)
            self.log_result(f"BFS từ đỉnh {start}:\n{' → '.join(map(str, result))}")
            
            # Tạo danh sách cạnh highlight theo thứ tự duyệt
            highlight_edges = []
            for i in range(len(result) - 1):
                highlight_edges.append((result[i], result[i + 1]))
            
            # Cập nhật hiển thị với highlight
            self.update_graph_display(highlight_path=result, highlight_edges=highlight_edges)
    
    def run_dfs(self):
        """Duyệt DFS và hiển thị đường đi"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        start = self.get_start_vertex()
        if start is not None:
            result = dfs(self.graph, start)
            self.log_result(f"DFS từ đỉnh {start}:\n{' → '.join(map(str, result))}")
            
            # Tạo danh sách cạnh highlight theo thứ tự duyệt
            highlight_edges = []
            for i in range(len(result) - 1):
                highlight_edges.append((result[i], result[i + 1]))
            
            # Cập nhật hiển thị với highlight
            self.update_graph_display(highlight_path=result, highlight_edges=highlight_edges)
    
    def run_shortest_path(self):
        """Tìm đường đi ngắn nhất và hiển thị"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Đường đi ngắn nhất")
        dialog.geometry("250x150")
        
        ttk.Label(dialog, text="Đỉnh nguồn:").grid(row=0, column=0, padx=10, pady=10)
        start_entry = ttk.Entry(dialog)
        start_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Đỉnh đích:").grid(row=1, column=0, padx=10, pady=10)
        end_entry = ttk.Entry(dialog)
        end_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def find():
            start_str = start_entry.get().strip()
            end_str = end_entry.get().strip()
            
            if not start_str or not end_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh nguồn và đích!")
                return
            
            # Thử chuyển sang số, nếu không được thì giữ nguyên chuỗi
            try:
                start = int(start_str)
            except ValueError:
                start = start_str
            
            try:
                end = int(end_str)
            except ValueError:
                end = end_str
            
            if start not in self.graph.get_vertices() or end not in self.graph.get_vertices():
                messagebox.showerror("Lỗi", "Đỉnh không tồn tại!")
                return
            
            path, distance = find_shortest_path(self.graph, start, end)
            
            if path:
                result = f"Đường đi ngắn nhất từ {start} đến {end}:\n"
                result += f"Đường đi: {' → '.join(map(str, path))}\n"
                result += f"Độ dài: {distance:.2f}"
                self.log_result(result)
                
                # Tạo danh sách cạnh highlight
                highlight_edges = []
                for i in range(len(path) - 1):
                    highlight_edges.append((path[i], path[i + 1]))
                
                # Cập nhật hiển thị với highlight
                self.update_graph_display(highlight_path=path, highlight_edges=highlight_edges)
            else:
                self.log_result(f"Không tìm thấy đường đi từ {start} đến {end}")
            
            dialog.destroy()
        
        ttk.Button(dialog, text="Tìm", command=find).grid(row=2, column=0, columnspan=2, pady=10)
    
    def run_bipartite(self):
        """Kiểm tra đồ thị 2 phía"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        is_bip = is_bipartite(self.graph)
        
        result = f"Đồ thị {'LÀ' if is_bip else 'KHÔNG PHẢI'} đồ thị 2 phía\n"
        
        if is_bip:
            _, set1, set2 = get_bipartite_sets(self.graph)
            result += f"\nTập 1: {set1}\n"
            result += f"Tập 2: {set2}"
        
        self.log_result(result)
    
    def run_mst(self):
        """Tìm cây khung nhỏ nhất (Prim/Kruskal)"""
        if self.graph.graph_type == GraphType.DIRECTED:
            messagebox.showwarning("Cảnh báo", "MST chỉ áp dụng cho đồ thị vô hướng!")
            return
        
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        # Chọn thuật toán
        dialog = tk.Toplevel(self.root)
        dialog.title("Cây khung nhỏ nhất")
        dialog.geometry("200x120")
        
        ttk.Label(dialog, text="Chọn thuật toán:").pack(pady=10)
        
        algo_var = tk.StringVar(value="prim")
        ttk.Radiobutton(dialog, text="Prim", variable=algo_var, value="prim").pack()
        ttk.Radiobutton(dialog, text="Kruskal", variable=algo_var, value="kruskal").pack()
        
        def run():
            algo = algo_var.get()
            
            if algo == "prim":
                mst_edges, total_weight = prim(self.graph)
                name = "Prim"
            else:
                mst_edges, total_weight = kruskal(self.graph)
                name = "Kruskal"
            
            if mst_edges:
                result = f"Cây khung nhỏ nhất ({name}):\n"
                result += f"Tổng trọng số: {total_weight:.2f}\n\nCác cạnh:\n"
                for u, v, w in mst_edges:
                    result += f"  ({u}, {v}) - {w:.2f}\n"
                self.log_result(result)
                
                # Tạo danh sách cạnh highlight cho MST
                highlight_edges = [(u, v) for u, v, w in mst_edges]
                
                # Lấy tất cả các đỉnh trong MST
                mst_vertices = set()
                for u, v, w in mst_edges:
                    mst_vertices.add(u)
                    mst_vertices.add(v)
                
                # Cập nhật hiển thị với highlight
                self.update_graph_display(highlight_path=list(mst_vertices), highlight_edges=highlight_edges)
            else:
                self.log_result("Đồ thị không liên thông!")
            
            dialog.destroy()
        
        ttk.Button(dialog, text="Chạy", command=run).pack(pady=10)
    
    def run_max_flow(self):
        """Tìm luồng cực đại (Ford-Fulkerson)"""
        if self.graph.graph_type != GraphType.DIRECTED:
            messagebox.showwarning("Cảnh báo", "Luồng cực đại yêu cầu đồ thị có hướng!")
            return
        
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Luồng cực đại")
        dialog.geometry("250x150")
        
        ttk.Label(dialog, text="Đỉnh nguồn:").grid(row=0, column=0, padx=10, pady=10)
        source_entry = ttk.Entry(dialog)
        source_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Đỉnh đích:").grid(row=1, column=0, padx=10, pady=10)
        sink_entry = ttk.Entry(dialog)
        sink_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def find():
            source_str = source_entry.get().strip()
            sink_str = sink_entry.get().strip()
            
            if not source_str or not sink_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh nguồn và đích!")
                return
            
            # Thử chuyển sang số, nếu không được thì giữ nguyên chuỗi
            try:
                source = int(source_str)
            except ValueError:
                source = source_str
            
            try:
                sink = int(sink_str)
            except ValueError:
                sink = sink_str
            
            # Kiểm tra đỉnh có tồn tại
            vertices = self.graph.get_vertices()
            if source not in vertices:
                messagebox.showerror("Lỗi", f"Đỉnh nguồn '{source}' không tồn tại!\nCác đỉnh hiện có: {sorted(vertices)}")
                return
            
            if sink not in vertices:
                messagebox.showerror("Lỗi", f"Đỉnh đích '{sink}' không tồn tại!\nCác đỉnh hiện có: {sorted(vertices)}")
                return
            
            if source == sink:
                messagebox.showerror("Lỗi", "Đỉnh nguồn và đích phải khác nhau!")
                return
            
            try:
                max_flow_value, flow = ford_fulkerson(self.graph, source, sink)
                
                if max_flow_value == 0:
                    result = f"Luồng cực đại từ {source} đến {sink}: 0\n\n"
                    result += "Không có đường đi từ nguồn đến đích hoặc không có luồng!"
                    self.log_result(result)
                    messagebox.showinfo("Kết quả", "Luồng cực đại = 0\nKhông có đường đi hoặc không có luồng!")
                else:
                    result = f"Luồng cực đại từ {source} đến {sink}: {max_flow_value:.2f}\n\nLuồng trên các cạnh:\n"
                    
                    # Tạo danh sách cạnh có luồng để highlight
                    highlight_edges = []
                    flow_vertices = set([source, sink])
                    
                    # flow là dict với key=(u,v), value=flow_value
                    for (u, v), flow_value in flow.items():
                        if flow_value > 0:
                            result += f"  ({u}, {v}): {flow_value:.2f}\n"
                            highlight_edges.append((u, v))
                            flow_vertices.add(u)
                            flow_vertices.add(v)
                    
                    self.log_result(result)
                    
                    # Cập nhật hiển thị với highlight
                    self.update_graph_display(highlight_path=list(flow_vertices), highlight_edges=highlight_edges)
                
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi tính luồng: {str(e)}")
        
        ttk.Button(dialog, text="Tìm", command=find).grid(row=2, column=0, columnspan=2, pady=10)
    
    def run_euler(self):
        """Tìm chu trình/đường đi Euler"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        euler_type = is_eulerian(self.graph)
        
        # Chuyển đổi sang tiếng Việt để hiển thị
        euler_type_vn = {'cycle': 'chu trình Euler', 'path': 'đường đi Euler', 'none': 'không có'}
        result = f"Kiểm tra Euler: {euler_type_vn.get(euler_type, euler_type)}\n\n"
        
        if euler_type == 'cycle':
            cycle = hierholzer(self.graph)
            if cycle:
                result += f"Chu trình Euler:\n{' → '.join([f'({u},{v})' for u, v in cycle])}"
            else:
                result += "Không tìm thấy chu trình"
        elif euler_type == 'path':
            path = fleury(self.graph)
            if path:
                result += f"Đường đi Euler:\n{' → '.join([f'({u},{v})' for u, v in path])}"
            else:
                result += "Không tìm thấy đường đi"
        
        self.log_result(result)
    
    def show_representations(self):
        """Hiển thị các cách biểu diễn đồ thị"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        # Tạo cửa sổ mới
        dialog = tk.Toplevel(self.root)
        dialog.title("Các cách biểu diễn đồ thị")
        dialog.geometry("700x600")
        
        # Tạo notebook (tabs)
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Ma trận kề
        matrix_frame = ttk.Frame(notebook)
        notebook.add(matrix_frame, text="Ma trận kề")
        
        matrix_text = scrolledtext.ScrolledText(matrix_frame, width=80, height=30, wrap=tk.NONE, font=('Courier', 10))
        matrix_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        adj_matrix = AdjacencyMatrix(self.graph)
        vertices = sorted(self.graph.get_vertices())
        matrix = adj_matrix.get_matrix()
        
        # Header
        header = "     " + "".join([f"{v:>6}" for v in vertices])
        matrix_text.insert(tk.END, header + "\n")
        matrix_text.insert(tk.END, "-" * len(header) + "\n")
        
        # Rows
        for i, v in enumerate(vertices):
            row = f"{v:>4} |" + "".join([f"{matrix[i][j]:>6.1f}" for j in range(len(vertices))])
            matrix_text.insert(tk.END, row + "\n")
        
        matrix_text.config(state=tk.DISABLED)
        
        # Tab 2: Danh sách kề
        list_frame = ttk.Frame(notebook)
        notebook.add(list_frame, text="Danh sách kề")
        
        list_text = scrolledtext.ScrolledText(list_frame, width=80, height=30, wrap=tk.WORD, font=('Courier', 10))
        list_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        adj_list = AdjacencyList(self.graph)
        adj_dict = adj_list.get_list()
        
        for vertex in sorted(adj_dict.keys()):
            neighbors = adj_dict[vertex]
            line = f"Đỉnh {vertex}: "
            if neighbors:
                neighbor_str = ", ".join([f"{n} (w={w:.1f})" for n, w in sorted(neighbors.items())])
                line += neighbor_str
            else:
                line += "(không có kề)"
            list_text.insert(tk.END, line + "\n")
        
        list_text.config(state=tk.DISABLED)
        
        # Tab 3: Danh sách cạnh
        edge_frame = ttk.Frame(notebook)
        notebook.add(edge_frame, text="Danh sách cạnh")
        
        edge_text = scrolledtext.ScrolledText(edge_frame, width=80, height=30, wrap=tk.WORD, font=('Courier', 10))
        edge_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        edge_list = EdgeList(self.graph)
        edges = edge_list.get_edges()
        
        edge_text.insert(tk.END, f"Tổng số cạnh: {len(edges)}\n")
        edge_text.insert(tk.END, "=" * 50 + "\n\n")
        
        for i, (u, v, w) in enumerate(edges, 1):
            direction = "→" if self.graph.graph_type == GraphType.DIRECTED else "--"
            line = f"Cạnh {i:3d}: {u} {direction} {v}  (trọng số: {w:.2f})\n"
            edge_text.insert(tk.END, line)
        
        edge_text.config(state=tk.DISABLED)
        
        # Nút đóng
        ttk.Button(dialog, text="Đóng", command=dialog.destroy).pack(pady=10)
        
        self.log_result("Đã hiển thị các cách biểu diễn đồ thị")
    
    def visualize_prim(self):
        """Trực quan hóa thuật toán Prim"""
        if self.graph.graph_type == GraphType.DIRECTED:
            messagebox.showwarning("Cảnh báo", "Prim chỉ áp dụng cho đồ thị vô hướng!")
            return
        
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        try:
            import matplotlib.pyplot as plt
            visualizer = AlgorithmVisualizer(self.graph)
            visualizer.visualize_prim()
            plt.show()  # Hiển thị cửa sổ
            self.log_result("Đã hiển thị trực quan hóa Prim")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể trực quan hóa: {str(e)}")
    
    def visualize_kruskal(self):
        """Trực quan hóa thuật toán Kruskal"""
        if self.graph.graph_type == GraphType.DIRECTED:
            messagebox.showwarning("Cảnh báo", "Kruskal chỉ áp dụng cho đồ thị vô hướng!")
            return
        
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        try:
            import matplotlib.pyplot as plt
            visualizer = AlgorithmVisualizer(self.graph)
            visualizer.visualize_kruskal()
            plt.show()  # Hiển thị cửa sổ
            self.log_result("Đã hiển thị trực quan hóa Kruskal")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể trực quan hóa: {str(e)}")
    
    def visualize_ford_fulkerson(self):
        """Trực quan hóa thuật toán Ford-Fulkerson"""
        if self.graph.graph_type != GraphType.DIRECTED:
            messagebox.showwarning("Cảnh báo", "Ford-Fulkerson yêu cầu đồ thị có hướng!")
            return
        
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Ford-Fulkerson Visualization")
        dialog.geometry("250x150")
        
        ttk.Label(dialog, text="Đỉnh nguồn:").grid(row=0, column=0, padx=10, pady=10)
        source_entry = ttk.Entry(dialog)
        source_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(dialog, text="Đỉnh đích:").grid(row=1, column=0, padx=10, pady=10)
        sink_entry = ttk.Entry(dialog)
        sink_entry.grid(row=1, column=1, padx=10, pady=10)
        
        def visualize():
            source_str = source_entry.get().strip()
            sink_str = sink_entry.get().strip()
            
            if not source_str or not sink_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh nguồn và đích!")
                return
            
            try:
                source = int(source_str)
            except ValueError:
                source = source_str
            
            try:
                sink = int(sink_str)
            except ValueError:
                sink = sink_str
            
            if source not in self.graph.get_vertices() or sink not in self.graph.get_vertices():
                messagebox.showerror("Lỗi", "Đỉnh không tồn tại!")
                return
            
            try:
                import matplotlib.pyplot as plt
                visualizer = AlgorithmVisualizer(self.graph)
                visualizer.visualize_ford_fulkerson(source, sink)
                plt.show()  # Hiển thị cửa sổ
                self.log_result(f"Đã hiển thị trực quan hóa Ford-Fulkerson ({source} → {sink})")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể trực quan hóa: {str(e)}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Visualize", command=visualize).grid(row=2, column=0, columnspan=2, pady=10)
    
    def visualize_fleury(self):
        """Trực quan hóa thuật toán Fleury"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        euler_type = is_eulerian(self.graph)
        if euler_type == 'none':
            messagebox.showwarning("Cảnh báo", "Đồ thị không có đường đi Euler!")
            return
        
        try:
            import matplotlib.pyplot as plt
            visualizer = AlgorithmVisualizer(self.graph)
            visualizer.visualize_fleury()
            plt.show()  # Hiển thị cửa sổ
            self.log_result("Đã hiển thị trực quan hóa Fleury")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể trực quan hóa: {str(e)}")
    
    def visualize_hierholzer(self):
        """Trực quan hóa thuật toán Hierholzer"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        euler_type = is_eulerian(self.graph)
        if euler_type != 'cycle':
            messagebox.showwarning("Cảnh báo", "Đồ thị không có chu trình Euler! Hierholzer yêu cầu chu trình Euler.")
            return
        
        try:
            import matplotlib.pyplot as plt
            visualizer = AlgorithmVisualizer(self.graph)
            visualizer.visualize_hierholzer()
            plt.show()  # Hiển thị cửa sổ
            self.log_result("Đã hiển thị trực quan hóa Hierholzer")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể trực quan hóa: {str(e)}")
    
    def save_graph_file(self):
        """Lưu đồ thị ra file JSON/TXT"""
        if self.graph.vertex_count() == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="data"
        )
        
        if filename:
            try:
                save_graph(self.graph, filename)
                self.log_result(f"Đã lưu đồ thị vào {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")
    
    def load_graph_file(self):
        """Tải đồ thị từ file JSON/TXT"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
            initialdir="data"
        )
        
        if filename:
            try:
                # Kiểm tra file rỗng
                import os
                if os.path.getsize(filename) == 0:
                    messagebox.showerror("Lỗi", "File rỗng!")
                    return
                
                self.graph = load_graph(filename)
                self.pos = {}  # Reset vị trí đỉnh
                self.update_graph_display()
                self.log_result(f"Đã tải đồ thị từ {filename}")
            except json.JSONDecodeError as e:
                messagebox.showerror("Lỗi", f"File JSON không hợp lệ: {e}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")
    
    def on_mouse_press(self, event):
        """Xử lý khi nhấn chuột - bắt đầu kéo đỉnh"""
        if event.inaxes != self.ax or not self.pos:
            return
        
        # Tìm đỉnh gần nhất với vị trí click
        min_dist = float('inf')
        closest_node = None
        
        for node, (x, y) in self.pos.items():
            dist = (event.xdata - x)**2 + (event.ydata - y)**2
            if dist < min_dist:
                min_dist = dist
                closest_node = node
        
        # Nếu click đủ gần đỉnh (bán kính 0.05)
        if min_dist < 0.05:
            self.dragging_node = closest_node
    
    def on_mouse_release(self, event):
        """Xử lý khi thả chuột - kết thúc kéo"""
        self.dragging_node = None
    
    def on_mouse_move(self, event):
        """Xử lý khi di chuyển chuột - kéo đỉnh"""
        if self.dragging_node is None or event.inaxes != self.ax:
            return
        
        # Cập nhật vị trí đỉnh
        self.pos[self.dragging_node] = (event.xdata, event.ydata)
        
        # Vẽ lại đồ thị
        self.update_graph_display()


def main():
    """
    Hàm main - khởi chạy ứng dụng GUI
    """
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
