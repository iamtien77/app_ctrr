# Quy Tắc Đặt Tên

## Nguyên Tắc Chung

- Sử dụng tiếng Anh cho tất cả tên biến, hàm, lớp
- Tên phải mô tả rõ ràng mục đích sử dụng
- Tuân thủ PEP 8 style guide của Python
- Tránh viết tắt không rõ ràng
- Tên phải nhất quán trong toàn bộ dự án

## Đặt Tên File và Thư Mục

### Thư Mục

- Tên thư mục viết thường, không dấu gạch dưới: src, tests, data
- Tên thư mục mô tả rõ nội dung bên trong

### File Python

- Tên file viết thường, dùng dấu gạch dưới để phân cách từ: graph.py, file_io.py, shortest_path.py
- Tên file phải khớp với module chính bên trong
- File test bắt đầu bằng test_: test_graph.py, test_algorithms.py

## Đặt Tên Biến

### Biến Thường

- Viết thường, dùng dấu gạch dưới: vertex, edge_list, graph_type
- Tên phải là danh từ hoặc cụm danh từ: num_vertices, start_vertex, target_vertex

### Biến Tạm Thời

- Có thể dùng tên ngắn nếu phạm vi nhỏ: i, j cho vòng lặp, u, v cho đỉnh trong thuật toán

### Hằng Số

- Viết hoa toàn bộ, dùng dấu gạch dưới: DEFAULT_LAYOUT, VERTEX_SIZE, MAX_VERTICES
- Đặt trong class Config hoặc module constants

## Đặt Tên Hàm và Phương Thức

### Hàm Thường

- Viết thường, dùng dấu gạch dưới: add_vertex, remove_edge, get_neighbors
- Tên phải là động từ hoặc cụm động từ: find_shortest_path, check_bipartite, convert_to_matrix

### Phương Thức Getter/Setter

- Getter: bắt đầu bằng get_: get_vertices, get_edges, get_matrix
- Setter: bắt đầu bằng set_: set_weight, set_color
- Kiểm tra: bắt đầu bằng is_ hoặc has_: is_bipartite, has_edge, is_directed

### Phương Thức Callback

- Kết thúc bằng _with_callback: bfs_with_callback, dijkstra_with_callback
- Hoặc bắt đầu bằng visualize_: visualize_prim, visualize_bfs

### Phương Thức Xử Lý Sự Kiện

- Bắt đầu bằng on_: on_new_graph, on_add_vertex, on_run_bfs
- Mô tả rõ sự kiện được xử lý

## Đặt Tên Lớp

- Viết hoa chữ cái đầu mỗi từ, không dùng dấu gạch dưới: Graph, GraphDrawer, AlgorithmVisualizer
- Tên lớp là danh từ hoặc cụm danh từ: AdjacencyMatrix, ShortestPath, BipartiteChecker

### Lớp Enum

- Tên enum viết hoa chữ cái đầu: GraphType
- Giá trị enum viết hoa toàn bộ: DIRECTED, UNDIRECTED

## Đặt Tên Module

- Tên module viết thường, dùng dấu gạch dưới nếu cần: graph, file_io, shortest_path
- Tên module phải khớp với tên file

## Đặt Tên Tham Số

- Viết thường, dùng dấu gạch dưới: graph, start_vertex, target_vertex, edge_weight
- Tên tham số phải mô tả rõ ý nghĩa
- Tránh tên chung chung như data, obj, item

## Đặt Tên Thuộc Tính Lớp

- Viết thường, dùng dấu gạch dưới: graph_type, vertices, edges
- Thuộc tính private bắt đầu bằng dấu gạch dưới: _internal_state, _cache
- Thuộc tính protected bắt đầu bằng một dấu gạch dưới: _helper_method

## Quy Ước Đặc Biệt

### Thuật Toán

- Tên thuật toán giữ nguyên tên gốc: dijkstra, prim, kruskal, fleury, hierholzer
- Không viết hoa trừ khi là từ viết tắt: BFS, DFS

### Đồ Thị

- Biến đồ thị: graph hoặc g
- Đỉnh: vertex, vertices, u, v, start, end, source, sink
- Cạnh: edge, edges, (u, v)
- Trọng số: weight, edge_weight

### Danh Sách và Tập Hợp

- Danh sách: vertices_list, edges_list, path_list
- Tập hợp: vertices_set, visited_set
- Từ điển: adjacency_dict, color_dict

## Ví Dụ Tốt và Xấu

### Tốt

- add_vertex(vertex: int)
- find_shortest_path(start: int, end: int)
- is_bipartite(graph: Graph)
- visualize_prim(start: Optional[int])

### Xấu

- addV(v) - không rõ ràng
- findPath(s, e) - viết tắt không rõ
- check(graph) - không mô tả rõ
- prim_viz(n) - không nhất quán

## Lưu Ý Khi Làm Việc Nhóm

- Thống nhất quy tắc đặt tên trước khi bắt đầu code
- Code review phải kiểm tra việc tuân thủ quy tắc đặt tên
- Sử dụng linter để tự động kiểm tra
- Khi thêm code mới, phải tuân thủ quy tắc hiện có
- Nếu cần thay đổi quy tắc, phải thảo luận và cập nhật tài liệu này

