"""
Cấu hình ứng dụng - Chứa các hằng số và thiết lập
"""

# ===== CẤU HÌNH MÀU SẮC =====
# Màu cho đồ thị
VERTEX_COLOR = '#1f77b4'           # Màu đỉnh mặc định (xanh dương)
VERTEX_HIGHLIGHT_COLOR = '#ff7f0e' # Màu đỉnh được tô sáng (cam)
EDGE_COLOR = '#7f7f7f'             # Màu cạnh mặc định (xám)
EDGE_HIGHLIGHT_COLOR = '#d62728'   # Màu cạnh được tô sáng (đỏ)
PATH_COLOR = '#2ca02c'             # Màu đường đi (xanh lá)
VISITED_COLOR = '#9467bd'          # Màu đỉnh đã thăm (tím)
CURRENT_COLOR = '#e377c2'          # Màu đỉnh hiện tại (hồng)

# Màu cho đồ thị 2 phía
BIPARTITE_COLOR_1 = '#1f77b4'      # Màu tập đỉnh thứ nhất (xanh dương)
BIPARTITE_COLOR_2 = '#ff7f0e'      # Màu tập đỉnh thứ hai (cam)

# Màu nền
BACKGROUND_COLOR = '#ffffff'       # Màu nền trắng
CANVAS_BG_COLOR = '#f5f5f5'        # Màu nền canvas (xám nhạt)

# ===== CẤU HÌNH KÍCH THƯỚC =====
# Kích thước đỉnh và cạnh
VERTEX_SIZE = 500                  # Kích thước đỉnh
VERTEX_FONT_SIZE = 12              # Kích thước font chữ trên đỉnh
EDGE_WIDTH = 2.0                   # Độ dày cạnh
EDGE_HIGHLIGHT_WIDTH = 3.0         # Độ dày cạnh được tô sáng
EDGE_FONT_SIZE = 10                # Kích thước font chữ trọng số

# ===== CẤU HÌNH BỐ CỤC (LAYOUT) =====
# Các kiểu bố cục đồ thị
LAYOUT_SPRING = 'spring'           # Bố cục lò xo (mặc định)
LAYOUT_CIRCULAR = 'circular'       # Bố cục vòng tròn
LAYOUT_RANDOM = 'random'           # Bố cục ngẫu nhiên
LAYOUT_SHELL = 'shell'             # Bố cục vỏ sò
LAYOUT_SPECTRAL = 'spectral'       # Bố cục phổ

DEFAULT_LAYOUT = LAYOUT_SPRING     # Bố cục mặc định

# Tham số bố cục
SPRING_K = 0.5                     # Hệ số lò xo cho spring layout
SPRING_ITERATIONS = 50             # Số lần lặp cho spring layout

# ===== CẤU HÌNH ANIMATION =====
# Tốc độ animation (milliseconds)
ANIMATION_INTERVAL_SLOW = 2000     # Chậm - 2 giây
ANIMATION_INTERVAL_NORMAL = 1000   # Bình thường - 1 giây
ANIMATION_INTERVAL_FAST = 500      # Nhanh - 0.5 giây
ANIMATION_INTERVAL_VERY_FAST = 200 # Rất nhanh - 0.2 giây

DEFAULT_ANIMATION_INTERVAL = ANIMATION_INTERVAL_NORMAL

# ===== CẤU HÌNH CỬA SỔ =====
# Kích thước cửa sổ chính
WINDOW_WIDTH = 1200                # Chiều rộng cửa sổ
WINDOW_HEIGHT = 800                # Chiều cao cửa sổ
WINDOW_TITLE = "Ứng Dụng Quản Lý và Phân Tích Đồ Thị"

# ===== CẤU HÌNH CANVAS =====
# Kích thước canvas vẽ đồ thị
CANVAS_WIDTH = 800                 # Chiều rộng canvas
CANVAS_HEIGHT = 600                # Chiều cao canvas

# ===== CẤU HÌNH ĐỒ THỊ MẶC ĐỊNH =====
# Giới hạn số lượng
MAX_VERTICES = 100                 # Số đỉnh tối đa
MAX_EDGES = 1000                   # Số cạnh tối đa

# Trọng số mặc định
DEFAULT_WEIGHT = 1.0               # Trọng số mặc định cho cạnh
MIN_WEIGHT = 0.1                   # Trọng số tối thiểu
MAX_WEIGHT = 100.0                 # Trọng số tối đa

# ===== CẤU HÌNH FILE =====
# Đường dẫn thư mục
DATA_DIR = 'data'                  # Thư mục chứa dữ liệu
GRAPH_DIR = 'data/graphs'          # Thư mục chứa file đồ thị
IMAGE_DIR = 'data/images'          # Thư mục chứa hình ảnh

# Định dạng file
GRAPH_FILE_EXTENSION = '.json'     # Phần mở rộng file đồ thị
IMAGE_FILE_EXTENSION = '.png'      # Phần mở rộng file hình ảnh

# ===== CẤU HÌNH THUẬT TOÁN =====
# Giá trị vô cực cho các thuật toán
INFINITY = float('inf')

# Khoảng cách khởi tạo
DEFAULT_DISTANCE = INFINITY

# ===== CẤU HÌNH ĐỒ THỊ NGẪU NHIÊN =====
# Tham số tạo đồ thị ngẫu nhiên
RANDOM_GRAPH_MIN_VERTICES = 5      # Số đỉnh tối thiểu
RANDOM_GRAPH_MAX_VERTICES = 20     # Số đỉnh tối đa
RANDOM_GRAPH_EDGE_PROBABILITY = 0.3 # Xác suất tạo cạnh
RANDOM_GRAPH_MIN_WEIGHT = 1        # Trọng số tối thiểu
RANDOM_GRAPH_MAX_WEIGHT = 10       # Trọng số tối đa


def get_all_settings() -> dict:
    """
    Lấy tất cả các cấu hình của ứng dụng
    Returns:
        Dictionary chứa tất cả các cấu hình
    """
    return {
        'colors': {
            'vertex': VERTEX_COLOR,
            'vertex_highlight': VERTEX_HIGHLIGHT_COLOR,
            'edge': EDGE_COLOR,
            'edge_highlight': EDGE_HIGHLIGHT_COLOR,
            'path': PATH_COLOR,
            'visited': VISITED_COLOR,
            'current': CURRENT_COLOR,
            'bipartite_1': BIPARTITE_COLOR_1,
            'bipartite_2': BIPARTITE_COLOR_2,
            'background': BACKGROUND_COLOR,
            'canvas_bg': CANVAS_BG_COLOR,
        },
        'sizes': {
            'vertex_size': VERTEX_SIZE,
            'vertex_font_size': VERTEX_FONT_SIZE,
            'edge_width': EDGE_WIDTH,
            'edge_highlight_width': EDGE_HIGHLIGHT_WIDTH,
            'edge_font_size': EDGE_FONT_SIZE,
        },
        'layout': {
            'default': DEFAULT_LAYOUT,
            'spring_k': SPRING_K,
            'spring_iterations': SPRING_ITERATIONS,
        },
        'animation': {
            'interval_slow': ANIMATION_INTERVAL_SLOW,
            'interval_normal': ANIMATION_INTERVAL_NORMAL,
            'interval_fast': ANIMATION_INTERVAL_FAST,
            'interval_very_fast': ANIMATION_INTERVAL_VERY_FAST,
            'default_interval': DEFAULT_ANIMATION_INTERVAL,
        },
        'window': {
            'width': WINDOW_WIDTH,
            'height': WINDOW_HEIGHT,
            'title': WINDOW_TITLE,
        },
        'canvas': {
            'width': CANVAS_WIDTH,
            'height': CANVAS_HEIGHT,
        },
        'graph_limits': {
            'max_vertices': MAX_VERTICES,
            'max_edges': MAX_EDGES,
            'default_weight': DEFAULT_WEIGHT,
            'min_weight': MIN_WEIGHT,
            'max_weight': MAX_WEIGHT,
        },
        'files': {
            'data_dir': DATA_DIR,
            'graph_dir': GRAPH_DIR,
            'image_dir': IMAGE_DIR,
            'graph_extension': GRAPH_FILE_EXTENSION,
            'image_extension': IMAGE_FILE_EXTENSION,
        }
    }


def get_color_scheme():
    """
    Lấy bảng màu của ứng dụng
    Returns:
        Dictionary chứa các màu
    """
    return {
        'vertex': VERTEX_COLOR,
        'vertex_highlight': VERTEX_HIGHLIGHT_COLOR,
        'edge': EDGE_COLOR,
        'edge_highlight': EDGE_HIGHLIGHT_COLOR,
        'path': PATH_COLOR,
        'visited': VISITED_COLOR,
        'current': CURRENT_COLOR,
        'bipartite_1': BIPARTITE_COLOR_1,
        'bipartite_2': BIPARTITE_COLOR_2,
    }