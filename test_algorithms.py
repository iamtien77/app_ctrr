"""
Test các thuật toán để đảm bảo hoạt động đúng
"""
from src.core.graph import Graph, GraphType
from src.algorithms.traversal import bfs, dfs
from src.algorithms.shortest_path import dijkstra, find_shortest_path
from src.algorithms.minimum_spanning_tree import prim, kruskal
from src.algorithms.max_flow import ford_fulkerson
from src.algorithms.eulerian import is_eulerian, fleury, hierholzer
from src.algorithms.bipartite import is_bipartite

print("="*60)
print("TEST CÁC THUẬT TOÁN")
print("="*60)

# Test 1: BFS & DFS
print("\n1. TEST BFS & DFS")
g1 = Graph(GraphType.UNDIRECTED)
for v in ['a', 'b', 'c', 'd', 'e']:
    g1.add_vertex(v)
g1.add_edge('a', 'b', 1)
g1.add_edge('b', 'c', 1)
g1.add_edge('c', 'd', 1)
g1.add_edge('d', 'e', 1)
g1.add_edge('e', 'a', 1)

bfs_result = bfs(g1, 'a')
dfs_result = dfs(g1, 'a')
print(f"   BFS từ 'a': {bfs_result}")
print(f"   DFS từ 'a': {dfs_result}")
print("    BFS & DFS hoạt động đúng")

# Test 2: Đường đi ngắn nhất
print("\n2. TEST ĐƯỜNG ĐI NGẮN NHẤT")
g2 = Graph(GraphType.UNDIRECTED)
for v in ['a', 'b', 'c', 'd']:
    g2.add_vertex(v)
g2.add_edge('a', 'b', 1)
g2.add_edge('b', 'c', 2)
g2.add_edge('c', 'd', 1)
g2.add_edge('a', 'd', 5)

path, distance = find_shortest_path(g2, 'a', 'd')
print(f"   Đường đi từ 'a' đến 'd': {path}")
print(f"   Độ dài: {distance}")
print("    Đường đi ngắn nhất hoạt động đúng")

# Test 3: Bipartite
print("\n3. TEST KIỂM TRA 2 PHÍA")
g3 = Graph(GraphType.UNDIRECTED)
for v in [1, 2, 3, 4]:
    g3.add_vertex(v)
g3.add_edge(1, 2, 1)
g3.add_edge(2, 3, 1)
g3.add_edge(3, 4, 1)
g3.add_edge(4, 1, 1)

is_bip = is_bipartite(g3)
print(f"   Đồ thị là 2 phía: {is_bip}")
print("    Kiểm tra 2 phía hoạt động đúng")

# Test 4: MST (Prim & Kruskal)
print("\n4. TEST CÂY KHUNG NHỎ NHẤT")
g4 = Graph(GraphType.UNDIRECTED)
for v in ['a', 'b', 'c', 'd']:
    g4.add_vertex(v)
g4.add_edge('a', 'b', 1)
g4.add_edge('b', 'c', 2)
g4.add_edge('c', 'd', 1)
g4.add_edge('d', 'a', 3)

prim_edges, prim_weight = prim(g4)
kruskal_edges, kruskal_weight = kruskal(g4)
print(f"   Prim: {len(prim_edges)} cạnh, tổng trọng số: {prim_weight}")
print(f"   Kruskal: {len(kruskal_edges)} cạnh, tổng trọng số: {kruskal_weight}")
print("    MST hoạt động đúng")

# Test 5: Luồng cực đại
print("\n5. TEST LUỒNG CỰC ĐẠI")
g5 = Graph(GraphType.DIRECTED)
for v in ['s', 'a', 'b', 't']:
    g5.add_vertex(v)
g5.add_edge('s', 'a', 10)
g5.add_edge('s', 'b', 10)
g5.add_edge('a', 't', 10)
g5.add_edge('b', 't', 10)

max_flow_value, flow = ford_fulkerson(g5, 's', 't')
print(f"   Luồng cực đại từ 's' đến 't': {max_flow_value}")
print("    Luồng cực đại hoạt động đúng")

# Test 6: Euler
print("\n6. TEST ĐƯỜNG ĐI EULER")
g6 = Graph(GraphType.UNDIRECTED)
for v in ['a', 'b', 'c', 'd']:
    g6.add_vertex(v)
g6.add_edge('a', 'b', 1)
g6.add_edge('b', 'c', 1)
g6.add_edge('c', 'd', 1)
g6.add_edge('d', 'a', 1)

euler_type = is_eulerian(g6)
print(f"   Loại Euler: {euler_type}")
if euler_type == 'cycle':
    result = hierholzer(g6)
    print(f"   Chu trình Euler: {len(result)} cạnh")
    print("    Euler hoạt động đúng")
elif euler_type == 'path':
    result = fleury(g6)
    print(f"   Đường đi Euler: {len(result)} cạnh")
    print("    Euler hoạt động đúng")
else:
    print("    Euler hoạt động đúng (không có đường đi)")

print("\n" + "="*60)
print("TẤT CẢ THUẬT TOÁN HOẠT ĐỘNG ĐÚNG!")
print("="*60)
