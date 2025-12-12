"""
Ứng dụng Streamlit - Quản lý và Phân tích Đồ thị
Đầy đủ các chức năng: vẽ, lưu, duyệt, tìm đường, kiểm tra 2 phía, chuyển đổi biểu diễn, trực quan hóa thuật toán
"""

import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import json
import random
import time
from io import BytesIO, StringIO
from typing import List, Tuple, Optional

# Import thư viện agraph để vẽ đồ thị tương tác (kéo thả đỉnh)
try:
    from streamlit_agraph import agraph, Node, Edge, Config
    AGRAPH_AVAILABLE = True
except ImportError:
    AGRAPH_AVAILABLE = False

# Import các module từ project
from src.core.graph import Graph, GraphType
from src.core.representations import AdjacencyMatrix, AdjacencyList, EdgeList
from src.core.file_io import graph_to_dict, dict_to_graph
from src.algorithms.traversal import bfs, dfs
from src.algorithms.shortest_path import dijkstra, find_shortest_path
from src.algorithms.bipartite import is_bipartite, get_bipartite_sets
from src.algorithms.minimum_spanning_tree import prim, kruskal, prim_with_callback, kruskal_with_callback
from src.algorithms.max_flow import ford_fulkerson
from src.algorithms.eulerian import is_eulerian, fleury, hierholzer


# ==================== CẤU HÌNH TRANG ====================
st.set_page_config(
    page_title="Graph Analyzer - Ứng dụng Phân tích Đồ thị",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CSS GIAO DIỆN SÁNG ====================
st.markdown("""
<style>
    /* Background sáng */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    
    /* Header - xanh dương đậm trên nền sáng */
    .main-header {
        background: linear-gradient(90deg, #1e88e5 0%, #42a5f5 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(30, 136, 229, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.2rem;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Card style - nền trắng */
    .info-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .info-card p {
        color: #333;
        margin: 0.4rem 0;
        font-size: 0.95rem;
    }
    
    /* Result box - nền xanh nhạt */
    .result-box {
        background: #e8f5e9;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #43a047;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .result-box h4 {
        color: #2e7d32;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .result-box p {
        color: #333;
        margin: 0.3rem 0;
    }
    
    .result-box pre {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        color: #1b5e20;
        border: 1px solid #c8e6c9;
        overflow-x: auto;
    }
    
    /* Step box - các bước thuật toán */
    .step-box {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin: 0.4rem 0;
        color: #333;
        transition: all 0.2s ease;
    }
    
    .step-box:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .step-box.added {
        border-left: 4px solid #43a047;
        background: #f1f8e9;
    }
    
    .step-box.rejected {
        border-left: 4px solid #e53935;
        background: #ffebee;
    }
    
    .step-box.considering {
        border-left: 4px solid #fb8c00;
        background: #fff3e0;
    }
    
    /* Sidebar - nền xám nhạt */
    section[data-testid="stSidebar"] {
        background: #fafafa;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #1565c0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1e88e5 0%, #42a5f5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 136, 229, 0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #666;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1e88e5;
        color: white;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: white;
        border: 1px solid #ddd;
        border-radius: 6px;
        color: #333;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        background: white;
        border-radius: 6px;
    }
    
    /* File uploader */
    .stFileUploader {
        background: white;
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: white;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 8px;
        color: #333;
    }
    
    /* DataFrame */
    .stDataFrame {
        background: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ==================== HELPER FUNCTIONS ====================

def init_session_state():
    """Khởi tạo session state"""
    if 'graph' not in st.session_state:
        st.session_state.graph = Graph(GraphType.UNDIRECTED)
    if 'pos' not in st.session_state:
        st.session_state.pos = {}
    if 'algorithm_steps' not in st.session_state:
        st.session_state.algorithm_steps = []
    if 'interactive_mode' not in st.session_state:
        st.session_state.interactive_mode = True  # Mặc định bật chế độ tương tác


def create_interactive_agraph(graph: Graph, 
                               highlight_nodes: List = None,
                               highlight_edges: List = None,
                               node_colors: dict = None,
                               height: int = 500):
    """Tạo đồ thị tương tác với streamlit-agraph (hỗ trợ kéo thả đỉnh)"""
    
    if not AGRAPH_AVAILABLE:
        st.warning("Thư viện streamlit-agraph chưa được cài đặt. Chạy: `pip install streamlit-agraph`")
        return None
    
    if graph.vertex_count() == 0:
        st.info("Đồ thị rỗng - Hãy thêm đỉnh và cạnh!")
        return None
    
    nodes = []
    edges_list = []
    
    # Màu sắc cho các nodes
    for vertex in graph.get_vertices():
        # Xác định màu node
        if node_colors and vertex in node_colors:
            color = node_colors[vertex]
        elif highlight_nodes and vertex in highlight_nodes:
            if vertex == highlight_nodes[0]:
                color = '#2e7d32'  # Đỉnh nguồn - xanh lá đậm
            elif vertex == highlight_nodes[-1]:
                color = '#c62828'  # Đỉnh đích - đỏ đậm
            else:
                color = '#ef6c00'  # Đỉnh trung gian - cam
        else:
            color = '#1e88e5'  # Màu mặc định - xanh dương
        
        nodes.append(Node(
            id=str(vertex),
            label=str(vertex),
            size=30,
            color=color,
            font={'color': 'white', 'size': 16, 'face': 'Arial', 'strokeWidth': 0},
            borderWidth=3,
            borderWidthSelected=5,
            shape='circle'
        ))
    
    # Tạo edges
    for u, v, w in graph.get_edges():
        is_highlighted = False
        if highlight_edges:
            if (u, v) in highlight_edges or (v, u) in highlight_edges:
                is_highlighted = True
        
        edge_color = '#1565c0' if is_highlighted else '#b0bec5'
        edge_width = 4 if is_highlighted else 2
        
        edges_list.append(Edge(
            source=str(u),
            target=str(v),
            label=f"{w:.1f}",
            color=edge_color,
            width=edge_width,
            font={'size': 12, 'color': '#333', 'align': 'middle'},
            arrows={'to': {'enabled': graph.is_directed(), 'scaleFactor': 0.8}}
        ))
    
    # Cấu hình đồ thị tương tác
    config = Config(
        width='100%',
        height=height,
        directed=graph.is_directed(),
        physics={
            'enabled': True,
            'solver': 'forceAtlas2Based',
            'forceAtlas2Based': {
                'gravitationalConstant': -50,
                'centralGravity': 0.01,
                'springLength': 150,
                'springConstant': 0.08,
                'damping': 0.4
            },
            'stabilization': {
                'enabled': True,
                'iterations': 100
            }
        },
        interaction={
            'navigationButtons': True,
            'keyboard': True,
            'dragNodes': True,  # Cho phép kéo thả đỉnh
            'dragView': True,   # Cho phép kéo view
            'zoomView': True,   # Cho phép zoom
            'hover': True,
            'multiselect': True,
            'selectable': True,
            'tooltipDelay': 100
        },
        manipulation={
            'enabled': False  # Tắt chế độ chỉnh sửa (thêm/xóa) trực tiếp
        }
    )
    
    return agraph(nodes=nodes, edges=edges_list, config=config)


def graph_to_txt_string(graph: Graph) -> str:
    """Chuyển đồ thị thành chuỗi TXT"""
    lines = []
    lines.append(graph.graph_type.value.upper())
    vertices = graph.get_vertices()
    lines.append(str(len(vertices)))
    lines.append(" ".join(map(str, sorted(vertices, key=str))))
    edges = graph.get_edges()
    lines.append(str(len(edges)))
    for u, v, w in edges:
        lines.append(f"{u} {v} {w}")
    return "\n".join(lines)


def txt_string_to_graph(txt_content: str) -> Graph:
    """Chuyển chuỗi TXT thành đồ thị"""
    lines = [line.strip() for line in txt_content.strip().split('\n') if line.strip() and not line.strip().startswith('#')]
    
    if not lines:
        raise ValueError("File rỗng hoặc không hợp lệ")
    
    graph_type_str = lines[0].lower()
    graph_type = GraphType.DIRECTED if graph_type_str == 'directed' else GraphType.UNDIRECTED
    graph = Graph(graph_type)
    
    idx = 1
    # Bỏ qua số đỉnh nếu có
    if idx < len(lines):
        try:
            int(lines[idx])
            idx += 1
        except ValueError:
            pass
    
    # Đọc đỉnh (nếu tất cả trên một dòng)
    if idx < len(lines):
        parts = lines[idx].split()
        if len(parts) > 2 or (len(parts) <= 2 and not any(c.isdigit() and '.' not in lines[idx] for c in lines[idx])):
            # Nhiều phần tử = danh sách đỉnh
            for v_str in parts:
                try:
                    v = int(v_str)
                except ValueError:
                    v = v_str
                graph.add_vertex(v)
            idx += 1
    
    # Bỏ qua số cạnh nếu có
    if idx < len(lines):
        try:
            int(lines[idx])
            idx += 1
        except ValueError:
            pass
    
    # Đọc các cạnh
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


def create_graph_figure(graph: Graph, 
                       highlight_nodes: List = None, 
                       highlight_edges: List = None,
                       node_colors: dict = None,
                       title: str = "") -> go.Figure:
    """Tạo figure Plotly từ đồ thị"""
    
    if graph.vertex_count() == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Đồ thị rỗng - Hãy thêm đỉnh và cạnh!",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color="#1e88e5")
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500
        )
        return fig
    
    # Chuyển sang NetworkX để tính layout
    if graph.is_directed():
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    for vertex in graph.get_vertices():
        G.add_node(vertex)
    
    for u, v, w in graph.get_edges():
        G.add_edge(u, v, weight=w)
    
    # Tính layout
    if len(G.nodes()) <= 15:
        pos = nx.circular_layout(G, scale=2)
    else:
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    
    st.session_state.pos = pos
    
    # Tạo traces cho edges
    edge_traces = []
    
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        weight = data.get('weight', 1)
        
        is_highlighted = False
        if highlight_edges:
            if (u, v) in highlight_edges or (v, u) in highlight_edges:
                is_highlighted = True
        
        # Màu đường đi nổi bật hơn - xanh dương đậm
        if is_highlighted:
            color = '#1565c0'  # Xanh dương đậm cho đường đi
            width = 5
        else:
            color = '#b0bec5'  # Xám nhạt cho cạnh thường
            width = 2
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=width, color=color),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_trace)
        
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        
        # Màu label trọng số
        label_color = '#0d47a1' if is_highlighted else '#607d8b'
        
        edge_label = go.Scatter(
            x=[mid_x],
            y=[mid_y],
            mode='text',
            text=[f'{weight:.1f}'],
            textposition='middle center',
            textfont=dict(size=11, color=label_color, family='Arial Bold' if is_highlighted else 'Arial'),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_label)
    
    # Tạo trace cho nodes
    node_x = []
    node_y = []
    node_text = []
    node_color_list = []
    node_size_list = []
    node_border_list = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(str(node))
        
        if node_colors and node in node_colors:
            node_color_list.append(node_colors[node])
            node_size_list.append(50)
            node_border_list.append(3)
        elif highlight_nodes and node in highlight_nodes:
            if node == highlight_nodes[0]:
                # Đỉnh nguồn - Xanh lá đậm, to hơn
                node_color_list.append('#2e7d32')  # Xanh lá đậm
                node_size_list.append(55)
                node_border_list.append(4)
            elif node == highlight_nodes[-1]:
                # Đỉnh đích - Đỏ đậm, to hơn  
                node_color_list.append('#c62828')  # Đỏ đậm
                node_size_list.append(55)
                node_border_list.append(4)
            else:
                # Đỉnh trung gian trên đường đi - Cam
                node_color_list.append('#ef6c00')  # Cam đậm
                node_size_list.append(48)
                node_border_list.append(3)
        else:
            # Đỉnh thường - Xám
            node_color_list.append('#78909c')  # Xám xanh
            node_size_list.append(45)
            node_border_list.append(2)
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Arial Black'),
        hoverinfo='text',
        hovertext=[f'Đỉnh: {n}<br>Bậc: {G.degree(n)}' for n in G.nodes()],
        marker=dict(
            size=node_size_list,
            color=node_color_list,
            line=dict(width=node_border_list, color='white'),
            symbol='circle'
        ),
        showlegend=False
    )
    
    fig = go.Figure(data=edge_traces + [node_trace])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color='#1565c0'),
            x=0.5
        ),
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    if graph.is_directed():
        annotations = []
        for u, v, _ in graph.get_edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            
            dx = x1 - x0
            dy = y1 - y0
            length = (dx**2 + dy**2)**0.5
            if length > 0:
                offset = 0.15
                x1_adj = x1 - (dx/length) * offset
                y1_adj = y1 - (dy/length) * offset
                
                annotations.append(dict(
                    ax=x0, ay=y0,
                    x=x1_adj, y=y1_adj,
                    xref='x', yref='y',
                    axref='x', ayref='y',
                    arrowhead=2,
                    arrowsize=1.5,
                    arrowwidth=2,
                    arrowcolor='#1e88e5'
                ))
        
        fig.update_layout(annotations=annotations)
    
    return fig


def parse_vertex(vertex_str: str):
    """Chuyển đổi chuỗi đỉnh thành số hoặc giữ nguyên"""
    vertex_str = vertex_str.strip()
    try:
        return int(vertex_str)
    except ValueError:
        return vertex_str


def get_graph_info_dict(graph: Graph) -> dict:
    """Lấy thông tin đồ thị dạng dict"""
    vertices = graph.get_vertices()
    edges = graph.get_edges()
    
    if not vertices:
        return {
            'type': graph.graph_type.value,
            'vertices': 0,
            'edges': 0,
            'avg_degree': 0,
            'is_connected': False
        }
    
    degrees = [graph.get_degree(v) for v in vertices]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0
    
    is_connected = True
    if vertices:
        visited = set(bfs(graph, vertices[0]))
        is_connected = len(visited) == len(vertices)
    
    return {
        'type': 'Có hướng' if graph.is_directed() else 'Vô hướng',
        'vertices': len(vertices),
        'edges': len(edges),
        'avg_degree': avg_degree,
        'min_degree': min(degrees) if degrees else 0,
        'max_degree': max(degrees) if degrees else 0,
        'total_weight': sum(w for _, _, w in edges),
        'is_connected': is_connected
    }


# ==================== MAIN APP ====================

def main():
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Graph Analyzer</h1>
        <p>Ứng dụng Quản lý và Phân tích Đồ thị</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== SIDEBAR ==========
    with st.sidebar:
        st.markdown("## Điều khiển")
        
        st.markdown("### Tạo đồ thị")
        
        graph_type = st.radio(
            "Loại đồ thị:",
            ["Vô hướng", "Có hướng"],
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Tạo mới", use_container_width=True):
                gtype = GraphType.DIRECTED if graph_type == "Có hướng" else GraphType.UNDIRECTED
                st.session_state.graph = Graph(gtype)
                st.session_state.pos = {}
                st.success("Đã tạo đồ thị mới!")
        
        with col2:
            # Nút mở dialog tạo ngẫu nhiên
            if st.button("Ngẫu nhiên", use_container_width=True):
                st.session_state.show_random_dialog = True
        
        # Dialog tạo đồ thị ngẫu nhiên
        if st.session_state.get('show_random_dialog', False):
            st.markdown("---")
            st.markdown("**Tùy chọn tạo ngẫu nhiên:**")
            
            # Kiểu đỉnh
            vertex_type = st.radio(
                "Kiểu đỉnh:",
                ["Số (0, 1, 2, ...)", "Chữ thường (a, b, c, ...)", "Chữ hoa (A, B, C, ...)"],
                key="vertex_type_radio"
            )
            
            # Số đỉnh
            num_vertices = st.slider("Số đỉnh:", min_value=3, max_value=26, value=6, key="num_vertices_slider")
            
            # Xác suất cạnh
            edge_prob = st.slider("Xác suất cạnh (%):", min_value=10, max_value=80, value=40, key="edge_prob_slider")
            
            # Trọng số
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                min_weight = st.number_input("Trọng số min:", value=1.0, step=0.5, key="min_weight_input")
            with col_w2:
                max_weight = st.number_input("Trọng số max:", value=10.0, step=0.5, key="max_weight_input")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Tạo", use_container_width=True, key="create_random_btn"):
                    gtype = GraphType.DIRECTED if graph_type == "Có hướng" else GraphType.UNDIRECTED
                    st.session_state.graph = Graph(gtype)
                    
                    # Tạo danh sách đỉnh theo kiểu
                    if "Số" in vertex_type:
                        vertices = list(range(num_vertices))
                    elif "thường" in vertex_type:
                        vertices = [chr(ord('a') + i) for i in range(num_vertices)]
                    else:  # Chữ hoa
                        vertices = [chr(ord('A') + i) for i in range(num_vertices)]
                    
                    # Thêm đỉnh
                    for v in vertices:
                        st.session_state.graph.add_vertex(v)
                    
                    # Thêm cạnh ngẫu nhiên
                    for i in range(len(vertices)):
                        for j in range(i+1, len(vertices)):
                            if random.random() < (edge_prob / 100):
                                weight = round(random.uniform(min_weight, max_weight), 1)
                                st.session_state.graph.add_edge(vertices[i], vertices[j], weight)
                    
                    st.session_state.pos = {}
                    st.session_state.show_random_dialog = False
                    st.success(f"Tạo đồ thị với {num_vertices} đỉnh!")
                    st.rerun()
            
            with col_btn2:
                if st.button("Hủy", use_container_width=True, key="cancel_random_btn"):
                    st.session_state.show_random_dialog = False
                    st.rerun()
        
        st.divider()
        
        st.markdown("### Thêm đỉnh/cạnh")
        
        vertex_input = st.text_input("Tên đỉnh:", placeholder="VD: A hoặc 1")
        if st.button("Thêm đỉnh", use_container_width=True):
            if vertex_input:
                v = parse_vertex(vertex_input)
                st.session_state.graph.add_vertex(v)
                st.session_state.pos = {}
                st.success(f"Đã thêm đỉnh {v}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            u_input = st.text_input("Từ:", placeholder="u")
        with col2:
            v_input = st.text_input("Đến:", placeholder="v")
        with col3:
            w_input = st.number_input("Trọng số:", value=1.0, step=0.1)
        
        if st.button("Thêm cạnh", use_container_width=True):
            if u_input and v_input:
                u = parse_vertex(u_input)
                v = parse_vertex(v_input)
                st.session_state.graph.add_edge(u, v, w_input)
                st.session_state.pos = {}
                st.success(f"Đã thêm cạnh ({u}, {v})")
        
        st.divider()
        
        st.markdown("### Lưu/Tải đồ thị")
        
        if st.session_state.graph.vertex_count() > 0:
            file_format = st.radio("Định dạng:", ["JSON", "TXT"], horizontal=True)
            
            if file_format == "JSON":
                graph_data = graph_to_dict(st.session_state.graph)
                json_str = json.dumps(graph_data, indent=2, ensure_ascii=False)
                st.download_button(
                    label="Tải xuống (JSON)",
                    data=json_str,
                    file_name="graph.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                txt_str = graph_to_txt_string(st.session_state.graph)
                st.download_button(
                    label="Tải xuống (TXT)",
                    data=txt_str,
                    file_name="graph.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        uploaded_file = st.file_uploader("Tải lên đồ thị", type=["json", "txt"])
        if uploaded_file:
            try:
                file_content = uploaded_file.read().decode('utf-8')
                file_name = uploaded_file.name.lower()
                
                if file_name.endswith('.json'):
                    data = json.loads(file_content)
                    st.session_state.graph = dict_to_graph(data)
                else:
                    st.session_state.graph = txt_string_to_graph(file_content)
                
                st.session_state.pos = {}
                st.success("Đã tải đồ thị!")
            except Exception as e:
                st.error(f"Lỗi: {e}")
        
        st.divider()
        
        st.markdown("### Thông tin đồ thị")
        info = get_graph_info_dict(st.session_state.graph)
        
        st.markdown(f"""
        <div class="info-card">
            <p><b>Loại:</b> {info['type']}</p>
            <p><b>Số đỉnh:</b> {info['vertices']}</p>
            <p><b>Số cạnh:</b> {info['edges']}</p>
            <p><b>Bậc TB:</b> {info['avg_degree']:.2f}</p>
            <p><b>Liên thông:</b> {'Có' if info['is_connected'] else 'Không'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== MAIN CONTENT ==========
    
    tabs = st.tabs([
        "Trực quan hóa", 
        "Thuật toán cơ bản",
        "Thuật toán nâng cao",
        "Biểu diễn đồ thị"
    ])
    
    # ========== TAB 1: TRỰC QUAN HÓA ==========
    with tabs[0]:
        # Toggle chọn chế độ hiển thị
        mode_col1, mode_col2 = st.columns([3, 1])
        
        with mode_col1:
            if AGRAPH_AVAILABLE:
                st.session_state.interactive_mode = st.toggle(
                    "Chế độ tương tác (kéo thả đỉnh bằng chuột)", 
                    value=st.session_state.interactive_mode,
                    help="Bật để kéo thả các đỉnh, zoom và di chuyển đồ thị bằng chuột"
                )
        
        with mode_col2:
            if st.session_state.interactive_mode and AGRAPH_AVAILABLE:
                st.markdown("""
                <div style="background: #e3f2fd; padding: 10px; border-radius: 8px; font-size: 0.85rem;">
                    <b>Hướng dẫn:</b><br>
                    • Kéo đỉnh để di chuyển<br>
                    • Cuộn chuột để zoom<br>
                    • Kéo nền để di chuyển view<br>
                    • Nút điều hướng ở góc
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.session_state.interactive_mode and AGRAPH_AVAILABLE:
                # Chế độ tương tác với agraph
                st.markdown("### Đồ thị tương tác")
                create_interactive_agraph(
                    st.session_state.graph,
                    height=550
                )
            else:
                # Chế độ tĩnh với Plotly
                st.markdown("### Đồ thị tĩnh")
                fig = create_graph_figure(
                    st.session_state.graph,
                    title="Đồ thị hiện tại"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Danh sách cạnh")
            edges = st.session_state.graph.get_edges()
            if edges:
                # Container có thể cuộn
                edge_container = st.container(height=400)
                with edge_container:
                    for i, (u, v, w) in enumerate(edges, 1):
                        arrow = "→" if st.session_state.graph.is_directed() else "—"
                        st.write(f"**{i}.** {u} {arrow} {v} (w={w:.1f})")
            else:
                st.info("Chưa có cạnh nào")
            
            # Hiển thị thông tin bổ sung
            st.divider()
            st.markdown("### Thao tác nhanh")
            
            delete_col1, delete_col2 = st.columns(2)
            with delete_col1:
                vertices = st.session_state.graph.get_vertices()
                if vertices:
                    del_v = st.selectbox("Chọn đỉnh:", vertices, key="del_vertex_select")
            
            with delete_col2:
                st.write("")  # Spacer
                st.write("")
                if st.button("Xóa đỉnh", key="del_vertex_btn", use_container_width=True):
                    if vertices:
                        st.session_state.graph.remove_vertex(del_v)
                        st.session_state.pos = {}
                        st.rerun()
            
            # Xóa cạnh
            if edges:
                edge_options = [f"{u} {'→' if st.session_state.graph.is_directed() else '—'} {v}" for u, v, w in edges]
                selected_edge = st.selectbox("Chọn cạnh:", edge_options, key="del_edge_select")
                
                if st.button("Xóa cạnh", key="del_edge_btn", use_container_width=True):
                    idx = edge_options.index(selected_edge)
                    u, v, w = edges[idx]
                    st.session_state.graph.remove_edge(u, v)
                    st.session_state.pos = {}
                    st.rerun()
    

    # ========== TAB 2: THUẬT TOÁN CƠ BẢN ==========
    with tabs[1]:
        algo_col1, algo_col2 = st.columns([1, 2])
        
        with algo_col1:
            st.markdown("### Chọn thuật toán")
            
            algorithm = st.selectbox(
                "Thuật toán:",
                [
                    "Duyệt BFS",
                    "Duyệt DFS", 
                    "Đường đi ngắn nhất",
                    "Kiểm tra đồ thị 2 phía"
                ]
            )
            
            vertices = st.session_state.graph.get_vertices()
            
            if algorithm in ["Duyệt BFS", "Duyệt DFS"]:
                if vertices:
                    start_vertex = st.selectbox("Đỉnh bắt đầu:", vertices)
                    
                    if st.button("Chạy", use_container_width=True, key="run_traversal"):
                        if algorithm == "Duyệt BFS":
                            result = bfs(st.session_state.graph, start_vertex)
                            st.session_state.last_result = {
                                'type': 'BFS',
                                'path': result,
                                'start': start_vertex
                            }
                        else:
                            result = dfs(st.session_state.graph, start_vertex)
                            st.session_state.last_result = {
                                'type': 'DFS',
                                'path': result,
                                'start': start_vertex
                            }
                else:
                    st.warning("Đồ thị rỗng!")
            
            elif algorithm == "Đường đi ngắn nhất":
                if vertices:
                    col_s, col_e = st.columns(2)
                    with col_s:
                        start_v = st.selectbox("Từ:", vertices, key="sp_start")
                    with col_e:
                        end_v = st.selectbox("Đến:", vertices, key="sp_end")
                    
                    if st.button("Tìm đường", use_container_width=True, key="run_sp"):
                        path, distance = find_shortest_path(st.session_state.graph, start_v, end_v)
                        st.session_state.last_result = {
                            'type': 'Shortest Path',
                            'path': path,
                            'distance': distance,
                            'start': start_v,
                            'end': end_v
                        }
                else:
                    st.warning("Đồ thị rỗng!")
            
            elif algorithm == "Kiểm tra đồ thị 2 phía":
                if st.button("Kiểm tra", use_container_width=True, key="run_bip"):
                    is_bip = is_bipartite(st.session_state.graph)
                    if is_bip:
                        _, set1, set2 = get_bipartite_sets(st.session_state.graph)
                        st.session_state.last_result = {
                            'type': 'Bipartite',
                            'is_bipartite': True,
                            'set1': set1,
                            'set2': set2
                        }
                    else:
                        st.session_state.last_result = {
                            'type': 'Bipartite',
                            'is_bipartite': False
                        }
        
        with algo_col2:
            st.markdown("### Kết quả")
            
            if 'last_result' in st.session_state:
                result = st.session_state.last_result
                
                if result['type'] in ['BFS', 'DFS']:
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Kết quả {result['type']}</h4>
                        <p><b>Đỉnh bắt đầu:</b> {result['start']}</p>
                        <p><b>Thứ tự duyệt:</b></p>
                        <pre>{' → '.join(map(str, result['path']))}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Chú thích màu
                    st.markdown("""
                    <div style="display:flex; gap:20px; margin:10px 0; flex-wrap:wrap;">
                        <span><span style="display:inline-block;width:16px;height:16px;background:#2e7d32;border-radius:50%;margin-right:5px;"></span> Đỉnh nguồn</span>
                        <span><span style="display:inline-block;width:16px;height:16px;background:#c62828;border-radius:50%;margin-right:5px;"></span> Đỉnh cuối</span>
                        <span><span style="display:inline-block;width:16px;height:16px;background:#ef6c00;border-radius:50%;margin-right:5px;"></span> Đỉnh trên đường đi</span>
                        <span><span style="display:inline-block;width:16px;height:16px;background:#78909c;border-radius:50%;margin-right:5px;"></span> Đỉnh khác</span>
                        <span><span style="display:inline-block;width:20px;height:4px;background:#1565c0;margin-right:5px;"></span> Cạnh đường đi</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    edges_hl = [(result['path'][i], result['path'][i+1]) 
                               for i in range(len(result['path'])-1)]
                    fig = create_graph_figure(
                        st.session_state.graph,
                        highlight_nodes=result['path'],
                        highlight_edges=edges_hl,
                        title=f"Kết quả {result['type']}"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                elif result['type'] == 'Shortest Path':
                    if result['path']:
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>Đường đi ngắn nhất</h4>
                            <p><b>Từ:</b> {result['start']} → <b>Đến:</b> {result['end']}</p>
                            <p><b>Độ dài:</b> {result['distance']:.2f}</p>
                            <p><b>Đường đi:</b></p>
                            <pre>{' → '.join(map(str, result['path']))}</pre>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Chú thích màu
                        st.markdown("""
                        <div style="display:flex; gap:20px; margin:10px 0; flex-wrap:wrap;">
                            <span><span style="display:inline-block;width:16px;height:16px;background:#2e7d32;border-radius:50%;margin-right:5px;"></span> Đỉnh nguồn</span>
                            <span><span style="display:inline-block;width:16px;height:16px;background:#c62828;border-radius:50%;margin-right:5px;"></span> Đỉnh đích</span>
                            <span><span style="display:inline-block;width:16px;height:16px;background:#ef6c00;border-radius:50%;margin-right:5px;"></span> Đỉnh trên đường đi</span>
                            <span><span style="display:inline-block;width:20px;height:4px;background:#1565c0;margin-right:5px;"></span> Đường đi ngắn nhất</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        edges_hl = [(result['path'][i], result['path'][i+1]) 
                                   for i in range(len(result['path'])-1)]
                        fig = create_graph_figure(
                            st.session_state.graph,
                            highlight_nodes=result['path'],
                            highlight_edges=edges_hl,
                            title="Đường đi ngắn nhất"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Không tìm thấy đường đi!")
                
                elif result['type'] == 'Bipartite':
                    if result['is_bipartite']:
                        st.markdown(f"""
                        <div class="result-box">
                            <h4>Đồ thị 2 phía</h4>
                            <p>Đây LÀ đồ thị 2 phía (bipartite)</p>
                            <p><b>Tập 1:</b> {result['set1']}</p>
                            <p><b>Tập 2:</b> {result['set2']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        node_colors = {}
                        for v in result['set1']:
                            node_colors[v] = '#1e88e5'
                        for v in result['set2']:
                            node_colors[v] = '#fb8c00'
                        
                        fig = create_graph_figure(
                            st.session_state.graph,
                            node_colors=node_colors,
                            title="Đồ thị 2 phía"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.markdown("""
                        <div class="result-box" style="background:#ffebee; border-left-color:#e53935;">
                            <h4 style="color:#c62828;">Không phải đồ thị 2 phía</h4>
                            <p>Đồ thị này KHÔNG phải là đồ thị 2 phía</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("Chọn thuật toán và nhấn Chạy để xem kết quả")
    
    # ========== TAB 3: THUẬT TOÁN NÂNG CAO ==========
    with tabs[2]:
        adv_col1, adv_col2 = st.columns([1, 2])
        
        with adv_col1:
            st.markdown("### Thuật toán nâng cao")
            
            adv_algorithm = st.selectbox(
                "Chọn thuật toán:",
                [
                    "Prim (Cây khung nhỏ nhất)",
                    "Kruskal (Cây khung nhỏ nhất)",
                    "Ford-Fulkerson (Luồng cực đại)",
                    "Fleury (Đường đi Euler)",
                    "Hierholzer (Chu trình Euler)"
                ]
            )
            
            vertices = st.session_state.graph.get_vertices()
            
            if adv_algorithm in ["Prim (Cây khung nhỏ nhất)", "Kruskal (Cây khung nhỏ nhất)"]:
                if st.session_state.graph.is_directed():
                    st.warning("MST chỉ áp dụng cho đồ thị vô hướng!")
                else:
                    if st.button("Chạy MST", use_container_width=True, key="run_mst"):
                        steps = []
                        
                        def callback(u, v, weight, state):
                            steps.append({
                                'u': u, 'v': v, 
                                'weight': weight, 
                                'state': state
                            })
                        
                        if "Prim" in adv_algorithm:
                            mst_edges, total = prim_with_callback(
                                st.session_state.graph, None, callback
                            )
                            algo_name = "Prim"
                        else:
                            mst_edges, total = kruskal_with_callback(
                                st.session_state.graph, callback
                            )
                            algo_name = "Kruskal"
                        
                        st.session_state.adv_result = {
                            'type': 'MST',
                            'algorithm': algo_name,
                            'edges': mst_edges,
                            'total': total,
                            'steps': steps
                        }
            
            elif adv_algorithm == "Ford-Fulkerson (Luồng cực đại)":
                if not st.session_state.graph.is_directed():
                    st.warning("Luồng cực đại yêu cầu đồ thị có hướng!")
                elif vertices:
                    col_s, col_t = st.columns(2)
                    with col_s:
                        source = st.selectbox("Nguồn:", vertices, key="ff_source")
                    with col_t:
                        sink = st.selectbox("Đích:", vertices, key="ff_sink")
                    
                    if st.button("Tìm luồng cực đại", use_container_width=True, key="run_ff"):
                        max_flow, flow = ford_fulkerson(
                            st.session_state.graph, source, sink
                        )
                        st.session_state.adv_result = {
                            'type': 'MaxFlow',
                            'source': source,
                            'sink': sink,
                            'max_flow': max_flow,
                            'flow': flow
                        }
            
            elif adv_algorithm in ["Fleury (Đường đi Euler)", "Hierholzer (Chu trình Euler)"]:
                euler_type = is_eulerian(st.session_state.graph)
                
                if euler_type == 'none':
                    st.warning("Đồ thị không có đường đi/chu trình Euler!")
                else:
                    if st.button("Tìm đường Euler", use_container_width=True, key="run_euler"):
                        if "Fleury" in adv_algorithm:
                            path = fleury(st.session_state.graph)
                            algo_name = "Fleury"
                        else:
                            path = hierholzer(st.session_state.graph)
                            algo_name = "Hierholzer"
                        
                        st.session_state.adv_result = {
                            'type': 'Euler',
                            'algorithm': algo_name,
                            'path': path,
                            'euler_type': euler_type
                        }
        
        with adv_col2:
            st.markdown("### Kết quả trực quan hóa")
            
            if 'adv_result' in st.session_state:
                result = st.session_state.adv_result
                
                if result['type'] == 'MST':
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Cây khung nhỏ nhất ({result['algorithm']})</h4>
                        <p><b>Tổng trọng số:</b> {result['total']:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### Các bước thực hiện:")
                    for i, step in enumerate(result['steps'], 1):
                        state_text = "[THÊM]" if step['state'] == 'added' else "[LOẠI]" if step['state'] == 'rejected' else "[XÉT]"
                        state_class = step['state']
                        st.markdown(f"""
                        <div class="step-box {state_class}">
                            <b>Bước {i}:</b> Cạnh ({step['u']}, {step['v']}) - w={step['weight']:.1f} {state_text}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    highlight_edges = [(u, v) for u, v, _ in result['edges']]
                    mst_vertices = set()
                    for u, v, _ in result['edges']:
                        mst_vertices.add(u)
                        mst_vertices.add(v)
                    
                    fig = create_graph_figure(
                        st.session_state.graph,
                        highlight_nodes=list(mst_vertices),
                        highlight_edges=highlight_edges,
                        title=f"Cây khung nhỏ nhất ({result['algorithm']})"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                elif result['type'] == 'MaxFlow':
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>Luồng cực đại (Ford-Fulkerson)</h4>
                        <p><b>Nguồn:</b> {result['source']} → <b>Đích:</b> {result['sink']}</p>
                        <p><b>Luồng cực đại:</b> {result['max_flow']:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### Luồng trên các cạnh:")
                    highlight_edges = []
                    for (u, v), flow_val in result['flow'].items():
                        if flow_val > 0:
                            st.markdown(f"""
                            <div class="step-box added">
                                ({u} → {v}): <b>{flow_val:.2f}</b>
                            </div>
                            """, unsafe_allow_html=True)
                            highlight_edges.append((u, v))
                    
                    fig = create_graph_figure(
                        st.session_state.graph,
                        highlight_nodes=[result['source'], result['sink']],
                        highlight_edges=highlight_edges,
                        title="Luồng cực đại"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                elif result['type'] == 'Euler':
                    euler_type_vn = "Chu trình" if result['euler_type'] == 'cycle' else "Đường đi"
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>{euler_type_vn} Euler ({result['algorithm']})</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if result['path']:
                        st.markdown("#### Đường đi:")
                        path_str = " → ".join([f"({u},{v})" for u, v in result['path']])
                        st.code(path_str)
                        
                        highlight_edges = [(u, v) for u, v in result['path']]
                        fig = create_graph_figure(
                            st.session_state.graph,
                            highlight_edges=highlight_edges,
                            title=f"{euler_type_vn} Euler"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Không tìm thấy đường đi Euler!")
            else:
                st.info("Chọn thuật toán và nhấn Chạy để xem kết quả")
    
    # ========== TAB 4: BIỂU DIỄN ĐỒ THỊ ==========
    with tabs[3]:
        st.markdown("### Chuyển đổi biểu diễn đồ thị")
        
        if st.session_state.graph.vertex_count() == 0:
            st.warning("Đồ thị rỗng! Hãy tạo đồ thị trước.")
        else:
            rep_tabs = st.tabs(["Ma trận kề", "Danh sách kề", "Danh sách cạnh"])
            
            with rep_tabs[0]:
                st.markdown("#### Ma trận kề (Adjacency Matrix)")
                
                adj_matrix = AdjacencyMatrix(st.session_state.graph)
                vertices = adj_matrix.vertices
                matrix = adj_matrix.get_matrix()
                
                import pandas as pd
                df = pd.DataFrame(
                    matrix,
                    index=[str(v) for v in vertices],
                    columns=[str(v) for v in vertices]
                )
                
                st.dataframe(
                    df.style.format("{:.1f}").background_gradient(cmap='Blues'),
                    use_container_width=True
                )
                
                with st.expander("Xem dạng văn bản"):
                    header = "     " + "".join([f"{v:>6}" for v in vertices])
                    st.code(header)
                    for i, v in enumerate(vertices):
                        row = f"{v:>4} |" + "".join([f"{matrix[i][j]:>6.1f}" for j in range(len(vertices))])
                        st.code(row)
            
            with rep_tabs[1]:
                st.markdown("#### Danh sách kề (Adjacency List)")
                
                adj_list = AdjacencyList(st.session_state.graph)
                adj_dict = adj_list.get_list()
                
                for vertex in sorted(adj_dict.keys(), key=str):
                    neighbors = adj_dict[vertex]
                    if neighbors:
                        neighbor_str = ", ".join([f"{n} (w={w:.1f})" for n, w in sorted(neighbors.items(), key=lambda x: str(x[0]))])
                    else:
                        neighbor_str = "(không có kề)"
                    
                    st.markdown(f"""
                    <div class="step-box">
                        <b>Đỉnh {vertex}:</b> {neighbor_str}
                    </div>
                    """, unsafe_allow_html=True)
            
            with rep_tabs[2]:
                st.markdown("#### Danh sách cạnh (Edge List)")
                
                edge_list = EdgeList(st.session_state.graph)
                edges = edge_list.get_edges()
                
                st.write(f"**Tổng số cạnh:** {len(edges)}")
                
                direction = "→" if st.session_state.graph.is_directed() else "—"
                
                for i, (u, v, w) in enumerate(edges, 1):
                    st.markdown(f"""
                    <div class="step-box">
                        <b>Cạnh {i}:</b> {u} {direction} {v} (trọng số: {w:.2f})
                    </div>
                    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #1565c0; padding: 1rem;">
        <p><b>Graph Analyzer</b> | Phát triển bằng Streamlit</p>
        <p style="font-size: 0.8rem; color: #666;">
            Hỗ trợ: BFS, DFS, Dijkstra, Bipartite Check, Prim, Kruskal, Ford-Fulkerson, Fleury, Hierholzer
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
