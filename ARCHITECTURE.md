# Cấu Trúc Dự Án

## Tổng Quan

Dự án ứng dụng quản lý và phân tích đồ thị được tổ chức theo cấu trúc module rõ ràng, tách biệt các chức năng cơ bản và nâng cao.

## Cấu Trúc Thư Mục

### Thư Mục Gốc

- main.py: Điểm khởi chạy chính của ứng dụng, gọi GraphApplication từ module visualization
- requirements.txt: Danh sách các thư viện Python cần thiết cho dự án
- README.md: Tài liệu hướng dẫn sử dụng và cài đặt
- .gitignore: Các file và thư mục không cần commit lên git

### Thư Mục src/

Thư mục chứa toàn bộ source code của ứng dụng.

#### src/core/

Module cốt lõi chứa các lớp và cấu trúc dữ liệu cơ bản của đồ thị.

- graph.py: Lớp Graph cơ bản, định nghĩa cấu trúc đồ thị với các phương thức thêm/xóa đỉnh, thêm/xóa cạnh, truy vấn thông tin. Hỗ trợ đồ thị có hướng và vô hướng thông qua enum GraphType.

- representations.py: Các lớp chuyển đổi giữa các phương pháp biểu diễn đồ thị:
  - AdjacencyMatrix: Biểu diễn bằng ma trận kề
  - AdjacencyList: Biểu diễn bằng danh sách kề
  - EdgeList: Biểu diễn bằng danh sách cạnh
  Mỗi lớp có phương thức chuyển đổi sang các dạng khác.

- file_io.py: Xử lý lưu và tải đồ thị từ file. Hỗ trợ định dạng JSON và TXT. Các phương thức save_graph, load_graph, export_to_json, import_from_json, export_to_txt, import_from_txt.

#### src/algorithms/

Module chứa các thuật toán xử lý đồ thị.

- traversal.py: Thuật toán duyệt đồ thị:
  - bfs: Duyệt theo chiều rộng
  - dfs: Duyệt theo chiều sâu
  - bfs_with_callback, dfs_with_callback: Phiên bản có callback để trực quan hóa từng bước

- shortest_path.py: Thuật toán tìm đường đi ngắn nhất:
  - dijkstra: Thuật toán Dijkstra
  - bellman_ford: Thuật toán Bellman-Ford
  - floyd_warshall: Thuật toán Floyd-Warshall cho tất cả cặp đỉnh
  - dijkstra_with_callback: Phiên bản có callback để trực quan hóa

- bipartite.py: Kiểm tra đồ thị 2 phía:
  - is_bipartite: Kiểm tra đồ thị có phải 2 phía không
  - is_bipartite_with_coloring: Kiểm tra và trả về cách tô màu
  - is_bipartite_with_callback: Phiên bản có callback để trực quan hóa

- minimum_spanning_tree.py: Thuật toán tìm cây khung nhỏ nhất:
  - prim: Thuật toán Prim
  - kruskal: Thuật toán Kruskal
  - prim_with_callback, kruskal_with_callback: Phiên bản có callback để trực quan hóa

- max_flow.py: Thuật toán luồng cực đại:
  - ford_fulkerson: Thuật toán Ford-Fulkerson
  - edmonds_karp: Thuật toán Edmonds-Karp
  - ford_fulkerson_with_callback: Phiên bản có callback để trực quan hóa

- eulerian.py: Thuật toán tìm đường đi Euler:
  - fleury: Thuật toán Fleury
  - hierholzer: Thuật toán Hierholzer
  - is_eulerian: Kiểm tra đồ thị có đường đi Euler không
  - fleury_with_callback, hierholzer_with_callback: Phiên bản có callback để trực quan hóa

#### src/visualization/

Module xử lý giao diện và trực quan hóa.

- graph_drawer.py: Vẽ đồ thị:
  - draw_graph: Vẽ đồ thị cơ bản với các tùy chọn layout, hiển thị nhãn, trọng số
  - draw_with_highlight: Vẽ đồ thị với đỉnh và cạnh được tô sáng
  - draw_path: Vẽ đồ thị với đường đi được tô sáng
  - save_graph_image: Lưu hình ảnh đồ thị ra file

- algorithm_visualizer.py: Trực quan hóa các thuật toán từng bước:
  - visualize_prim: Trực quan hóa thuật toán Prim
  - visualize_kruskal: Trực quan hóa thuật toán Kruskal
  - visualize_ford_fulkerson: Trực quan hóa thuật toán Ford-Fulkerson
  - visualize_fleury: Trực quan hóa thuật toán Fleury
  - visualize_hierholzer: Trực quan hóa thuật toán Hierholzer
  - visualize_bfs: Trực quan hóa BFS
  - visualize_dfs: Trực quan hóa DFS
  - visualize_shortest_path: Trực quan hóa tìm đường đi ngắn nhất
  - visualize_bipartite_check: Trực quan hóa kiểm tra đồ thị 2 phía

- gui.py: Giao diện người dùng chính:
  - GraphApplication: Lớp chính quản lý toàn bộ giao diện
  - setup_ui: Thiết lập giao diện
  - create_menu_bar: Tạo thanh menu
  - create_toolbar: Tạo thanh công cụ
  - create_graph_canvas: Tạo canvas vẽ đồ thị
  - create_control_panel: Tạo bảng điều khiển các thuật toán
  - on_new_graph, on_open_graph, on_save_graph: Xử lý file
  - on_add_vertex, on_add_edge: Thêm đỉnh và cạnh
  - on_run_bfs, on_run_dfs: Chạy thuật toán duyệt
  - on_find_shortest_path: Tìm đường đi ngắn nhất
  - on_check_bipartite: Kiểm tra đồ thị 2 phía
  - on_convert_representation: Chuyển đổi biểu diễn
  - on_visualize_prim, on_visualize_kruskal, on_visualize_ford_fulkerson, on_visualize_fleury, on_visualize_hierholzer: Trực quan hóa các thuật toán

#### src/utils/

Module chứa các tiện ích và cấu hình.

- config.py: Cấu hình ứng dụng:
  - Các hằng số về màu sắc, kích thước, layout
  - Cấu hình animation interval
  - Cấu hình cửa sổ và canvas
  - get_all_settings: Lấy tất cả cấu hình

- helpers.py: Các hàm tiện ích:
  - validate_graph: Kiểm tra tính hợp lệ của đồ thị
  - get_graph_info: Lấy thông tin thống kê đồ thị
  - generate_random_graph: Tạo đồ thị ngẫu nhiên
  - copy_graph: Sao chép đồ thị

### Thư Mục tests/

Chứa các file test cho từng module.

- test_graph.py: Test các phương thức của lớp Graph
- test_algorithms.py: Test các thuật toán
- test_representations.py: Test chuyển đổi giữa các biểu diễn

### Thư Mục data/

Thư mục lưu trữ các file đồ thị được người dùng lưu lại.

## Luồng Hoạt Động

1. Người dùng khởi chạy ứng dụng từ main.py
2. GraphApplication được khởi tạo, tạo giao diện
3. Người dùng có thể tạo đồ thị mới, mở đồ thị từ file, hoặc thêm đỉnh/cạnh
4. Chọn thuật toán để chạy hoặc trực quan hóa
5. Kết quả được hiển thị trên canvas
6. Có thể lưu đồ thị và kết quả

## Phụ Thuộc Giữa Các Module

- visualization phụ thuộc vào core và algorithms
- algorithms phụ thuộc vào core
- utils được sử dụng bởi tất cả các module khác
- tests phụ thuộc vào tất cả các module để kiểm thử

