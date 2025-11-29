# Ứng Dụng Quản Lý và Phân Tích Đồ Thị

Ứng dụng Python với **giao diện đồ họa** (GUI) để quản lý, phân tích và trực quan hóa đồ thị với các chức năng cơ bản và nâng cao.
Toàn bộ code được chú thích bằng **tiếng Việt có dấu** rõ ràng, dễ hiểu.

## Tính Năng Chính

### Giao Diện Đồ Họa (GUI)
1. **Giao diện thân thiện**: Sử dụng tkinter với matplotlib tích hợp
2. **Tương tác trực quan**: Kéo thả đỉnh bằng chuột, zoom, pan
3. **Màu sắc phân biệt**: Đường đi được tô màu (xanh → vàng → đỏ)
4. **Layout thông minh**: Tự động điều chỉnh bố cục theo số đỉnh
5. **Hiển thị thời gian thực**: Cập nhật đồ thị ngay lập tức

### Chức Năng Cơ Bản
1. **Quản lý đồ thị**: Thêm/xóa đỉnh và cạnh, hỗ trợ đồ thị có hướng và vô hướng
2. **Đỉnh linh hoạt**: Hỗ trợ tên đỉnh là số (0,1,2...) hoặc chữ cái (A,B,C... hoặc a,b,c...)
3. **Biểu diễn đồ thị**: Ma trận kề, Danh sách kề, Danh sách cạnh
4. **Lưu/Tải đồ thị**: Hỗ trợ định dạng JSON và TXT
5. **Tạo đồ thị ngẫu nhiên**: Sinh đồ thị tự động với tùy chọn tên đỉnh (số/chữ hoa/chữ thường)

### Thuật Toán Đồ Thị

#### Duyệt đồ thị
- **BFS** (Breadth-First Search) - Duyệt theo chiều rộng
- **DFS** (Depth-First Search) - Duyệt theo chiều sâu

#### Đường đi ngắn nhất
- **Dijkstra** - Tìm đường đi ngắn nhất (trọng số không âm)
- **Bellman-Ford** - Hỗ trợ trọng số âm
- **Floyd-Warshall** - Tất cả cặp đỉnh

#### Cây khung nhỏ nhất (MST)
- **Prim** - Thuật toán Prim
- **Kruskal** - Thuật toán Kruskal với Union-Find

#### Luồng cực đại
- **Ford-Fulkerson** - Tìm luồng cực đại
- **Edmonds-Karp** - Biến thể của Ford-Fulkerson

#### Đường đi Euler
- **Fleury** - Thuật toán Fleury
- **Hierholzer** - Thuật toán Hierholzer (hiệu quả hơn)

#### Đồ thị 2 phía
- Kiểm tra đồ thị có phải 2 phía không
- Tô màu và phân tách thành 2 tập

### Trực Quan Hóa Nâng Cao
- **Layout thích ứng**: Circular (≤10 đỉnh), Spring (11-50 đỉnh), Kamada-Kawai (>50 đỉnh)
- **Tô màu thông minh**: Đỉnh đầu (xanh lá), đỉnh cuối (đỏ), đỉnh trung gian (vàng)
- **Highlight đường đi**: Cạnh trong kết quả thuật toán được tô màu đỏ nổi bật
- **Kéo thả đỉnh**: Di chuyển đỉnh bằng chuột để tùy chỉnh bố cục
- **Zoom & Pan**: Công cụ matplotlib tích hợp để phóng to/thu nhỏ

## Cấu Trúc Dự Án

```
App_ctrr/
├── gui_app.py                   # Ứng dụng GUI chính (khởi chạy từ đây)
├── src/
│   ├── core/                    # Module cốt lõi
│   │   ├── graph.py            # Lớp đồ thị cơ bản
│   │   ├── representations.py  # Các cách biểu diễn
│   │   └── file_io.py          # Đọc/ghi file
│   ├── algorithms/              # Các thuật toán
│   │   ├── traversal.py        # BFS, DFS
│   │   ├── shortest_path.py    # Dijkstra, Bellman-Ford, Floyd-Warshall
│   │   ├── bipartite.py        # Kiểm tra đồ thị 2 phía
│   │   ├── minimum_spanning_tree.py  # Prim, Kruskal
│   │   ├── max_flow.py         # Ford-Fulkerson, Edmonds-Karp
│   │   └── eulerian.py         # Fleury, Hierholzer
│   ├── visualization/           # Trực quan hóa
│   │   ├── graph_drawer.py     # Vẽ đồ thị
│   │   └── algorithm_visualizer.py  # Trực quan hóa thuật toán
│   └── utils/                   # Tiện ích
│       ├── config.py           # Cấu hình
│       └── helpers.py          # Hàm hỗ trợ
├── data/                        # Dữ liệu đồ thị (JSON/TXT)
├── requirements.txt             # Thư viện cần thiết
├── README.md                    # File này
├── ARCHITECTURE.md             # Kiến trúc dự án
└── NAMING_CONVENTIONS.md       # Quy tắc đặt tên
```

## Cài Đặt

### Yêu Cầu
- Python 3.8 trở lên
- pip (Python package installer)

### Các Bước Cài Đặt

1. **Clone hoặc tải dự án về**
```bash
cd App_ctrr
```

2. **Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

Các thư viện bao gồm:
- `networkx >= 3.0` - Thư viện đồ thị
- `matplotlib >= 3.7.0` - Vẽ biểu đồ
- `numpy >= 1.24.0` - Tính toán số học

## Sử Dụng

### Chạy Ứng Dụng GUI
```bash
python gui_app.py
```

### Hướng Dẫn Sử Dụng GUI

#### 1. Tạo Đồ Thị
- **Tạo đồ thị mới**: Chọn loại (vô hướng/có hướng) → Click "Tạo đồ thị mới"
- **Tạo ngẫu nhiên**: Click "Tạo đồ thị ngẫu nhiên" → Nhập số đỉnh, xác suất cạnh, chọn kiểu tên đỉnh (số/chữ hoa/chữ thường)

#### 2. Thêm Đỉnh/Cạnh
- **Thêm đỉnh**: Nhập tên đỉnh (số hoặc chữ) → Click "Thêm đỉnh"
- **Thêm cạnh**: Nhập đỉnh u, v và trọng số w → Click "Thêm cạnh"

#### 3. Chạy Thuật Toán
- **Duyệt BFS/DFS**: Click nút → Chọn đỉnh bắt đầu → Xem kết quả màu sắc trên đồ thị
- **Đường đi ngắn nhất**: Click nút → Nhập đỉnh nguồn và đích → Đường đi được tô màu
- **Cây khung nhỏ nhất**: Click nút → Chọn Prim/Kruskal → Các cạnh MST được highlight
- **Luồng cực đại**: Click nút → Nhập nguồn và đích → Các cạnh có luồng được hiển thị
- **Kiểm tra 2 phía**: Click nút → Xem kết quả và 2 tập đỉnh (nếu có)
- **Đường đi Euler**: Click nút → Xem kết quả chu trình/đường đi Euler

#### 4. Tương Tác Với Đồ Thị
- **Kéo đỉnh**: Click và giữ chuột trên đỉnh → Di chuyển → Thả chuột
- **Zoom**: Dùng công cụ zoom trong toolbar
- **Pan**: Dùng công cụ pan để di chuyển khung nhìn

#### 5. Lưu/Tải Đồ Thị
- **Lưu**: Click "Lưu đồ thị" → Chọn vị trí và tên file → Lưu dạng JSON/TXT
- **Tải**: Click "Tải đồ thị" → Chọn file → Đồ thị được tải và hiển thị

### Ví Dụ Sử Dụng Module (Code)

```python
from src.core.graph import Graph, GraphType
from src.algorithms.shortest_path import find_shortest_path

# Tạo đồ thị vô hướng
graph = Graph(GraphType.UNDIRECTED)

# Thêm các cạnh
graph.add_edge(0, 1, 4)
graph.add_edge(1, 2, 3)
graph.add_edge(0, 2, 7)

# Tìm đường đi ngắn nhất
path, distance = find_shortest_path(graph, 0, 2)
print(f"Đường đi: {path}")  # [0, 1, 2]
print(f"Độ dài: {distance}")  # 7.0
```

## Tài Liệu

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Kiến trúc và thiết kế hệ thống
- **[NAMING_CONVENTIONS.md](NAMING_CONVENTIONS.md)** - Quy tắc đặt tên trong dự án

## Ví Dụ Nâng Cao (Code)

### 1. Tạo và Phân Tích Đồ Thị Ngẫu Nhiên
```python
from src.utils.helpers import generate_random_graph, get_graph_info
from src.core.graph import GraphType

# Tạo đồ thị ngẫu nhiên
graph = generate_random_graph(
    num_vertices=10, 
    edge_probability=0.3,
    graph_type=GraphType.UNDIRECTED
)

# Phân tích đồ thị
info = get_graph_info(graph)
print(f"Số đỉnh: {info['vertex_count']}")
print(f"Số cạnh: {info['edge_count']}")
print(f"Liên thông: {info['is_connected']}")
print(f"Bậc trung bình: {info['avg_degree']:.2f}")
```

### 2. Đồ Thị Với Đỉnh Là Chữ Cái
```python
from src.core.graph import Graph, GraphType
from src.algorithms.shortest_path import find_shortest_path

# Tạo đồ thị với đỉnh là chữ cái
graph = Graph(GraphType.UNDIRECTED)

# Thêm các cạnh với tên đỉnh là chữ
graph.add_edge('A', 'B', 5)
graph.add_edge('B', 'C', 3)
graph.add_edge('A', 'C', 8)

# Tìm đường đi ngắn nhất
path, distance = find_shortest_path(graph, 'A', 'C')
print(f"Đường đi: {' → '.join(path)}")  # A → B → C
print(f"Độ dài: {distance}")  # 8.0
```

### 3. Lưu và Tải Đồ Thị
```python
from src.core.file_io import save_graph, load_graph

# Lưu đồ thị ra file JSON
save_graph(graph, 'data/my_graph.json')

# Tải đồ thị từ file
loaded_graph = load_graph('data/my_graph.json')
print(f"Đã tải {loaded_graph.vertex_count()} đỉnh, {loaded_graph.edge_count()} cạnh")
```

### 4. Kiểm Tra Các Thuộc Tính Đồ Thị
```python
from src.algorithms.bipartite import is_bipartite
from src.algorithms.eulerian import is_eulerian

# Kiểm tra đồ thị 2 phía
if is_bipartite(graph):
    print("Đồ thị là đồ thị 2 phía")

# Kiểm tra đường đi Euler
euler_type = is_eulerian(graph)
print(f"Loại Euler: {euler_type}")
```

## Chú Thích Tiếng Việt

Toàn bộ code trong dự án được chú thích bằng **tiếng Việt có dấu** đầy đủ:

```python
def dijkstra(graph: Graph, start: int):
    """
    Thuật toán Dijkstra tìm đường đi ngắn nhất từ một đỉnh
    
    Thuật toán:
    1. Khởi tạo khoảng cách tất cả đỉnh = vô cực, trừ đỉnh start = 0
    2. Sử dụng hàng đợi ưu tiên để chọn đỉnh có khoảng cách nhỏ nhất
    3. Cập nhật khoảng cách các đỉnh kề
    
    Args:
        graph: Đồ thị cần tìm
        start: Đỉnh bắt đầu
    Returns:
        Tuple (khoảng_cách, đỉnh_cha)
    """
```

## Đóng Góp

Dự án này được tạo ra với mục đích học tập và nghiên cứu. Mọi đóng góp đều được hoan nghênh!

## License

Dự án này được phát hành dưới giấy phép MIT.

## Tác Giả

- **Repository**: app_ctrr
- **Owner**: iamtien77

## Điểm Nổi Bật

- **Giao diện trực quan**: GUI thân thiện, dễ sử dụng
- **Tương tác chuột**: Kéo thả đỉnh, zoom, pan
- **Màu sắc phân biệt**: Đường đi/cây khung được highlight rõ ràng
- **Hỗ trợ đa dạng**: Đỉnh có thể là số hoặc chữ cái
- **Layout thông minh**: Tự động tối ưu bố cục theo kích thước đồ thị
- **Thuật toán đầy đủ**: 10+ thuật toán đồ thị kinh điển
- **Code tiếng Việt**: Dễ đọc, dễ hiểu, dễ học
- **Lưu/Tải linh hoạt**: Hỗ trợ JSON và TXT

## Học Tập

Dự án này phù hợp cho:
- Sinh viên học môn Cấu trúc dữ liệu và Giải thuật
- Người mới bắt đầu học về đồ thị
- Nghiên cứu các thuật toán đồ thị cổ điển
- Thực hành Python và lập trình hướng đối tượng
- Học cách xây dựng GUI với tkinter và matplotlib

## Screenshot

![GUI Application](docs/screenshot.png) *(Giao diện chính của ứng dụng)*

## Công Nghệ Sử Dụng

- **Python 3.8+**: Ngôn ngữ lập trình chính
- **tkinter**: GUI framework (built-in Python)
- **matplotlib**: Vẽ đồ thị và biểu đồ
- **networkx**: Thư viện hỗ trợ layout và thuật toán đồ thị
- **numpy**: Tính toán ma trận và số học

## Liên Hệ

Nếu có câu hỏi hoặc gặp vấn đề, vui lòng tạo issue trên GitHub repository.

---

**Chúc bạn học tập và nghiên cứu hiệu quả!**

