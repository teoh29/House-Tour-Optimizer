import itertools
import heapq
import time
import statistics
import sys
import os
import matplotlib

if not sys.stdout.isatty() or (os.name == 'posix' and 'DISPLAY' not in os.environ):
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
import networkx as nx

AVG_SPEED_KMH = 30.0
FUEL_RATE_L_PER_KM = 0.08
CO2_RATE_KG_PER_L = 2.31

# 1. MEMBER MAPPING & GRAPH DATA STRUCTURES
member_mapping = {
    "Nadayu28 Residences": "Teoh En Yi",
    "Bandar Puteri Puchong": "Colin Leong",
    "Puchong Perdana": "Sian Yi Xuan",
    "Taman Puchong Utama": "Damien Yee",
    "Taman Putra Prima": "Choo Yen Ching"
}

raw_edges = {
    "Sunway University": {
        "Nadayu28 Residences": 0.75,
        "Bandar Puteri Puchong": 9.6,
        "Puchong Perdana": 10.7,
        "Taman Puchong Utama": 12.3,
        "Taman Putra Prima": 15.8
    },
    "Nadayu28 Residences": {
        "Bandar Puteri Puchong": 9.3,
        "Puchong Perdana": 11.2,
        "Taman Puchong Utama": 12.8,
        "Taman Putra Prima": 16.2
    },
    "Bandar Puteri Puchong": {
        "Puchong Perdana": 3.4,
        "Taman Puchong Utama": 5.0,
        "Taman Putra Prima": 8.4
    },
    "Puchong Perdana": {
        "Taman Puchong Utama": 2.1,
        "Taman Putra Prima": 7.0
    },
    "Taman Puchong Utama": {
        "Taman Putra Prima": 4.7
    },
    "Taman Putra Prima": {}
}

graph = {}
for source, targets in raw_edges.items():
    if source not in graph:
        graph[source] = {}
    for target, distance in targets.items():
        graph[source][target] = distance
        if target not in graph:
            graph[target] = {}
        graph[target][source] = distance

ALL_NODES = set(graph.keys())


# 2. GRAPH VERIFICATION
def verify_graph_integrity():
    """Programmatically verifies Completeness, Symmetry, and Non-negative weights."""
    for u in ALL_NODES:
        for v in ALL_NODES:
            if u != v:
                if v not in graph[u]:
                    raise ValueError(f"Graph not complete: missing edge {u}-{v}")
                if graph[u][v] != graph[v][u]:
                    raise ValueError(f"Asymmetry detected: {u}-{v}")
                if graph[u][v] < 0:
                    raise ValueError(f"Negative weight detected: {u}-{v}")
    return True

def verify_metric_properties():
    """Checks if the distance matrix strictly satisfies the Triangle Inequality."""
    violations = []
    for u in ALL_NODES:
        for v in ALL_NODES:
            for w in ALL_NODES:
                if u < w and u != v and v != w:
                    if graph[u][w] > graph[u][v] + graph[v][w]:
                        violations.append((u, v, w, graph[u][w], graph[u][v] + graph[v][w]))
    return violations


# 3. HEURISTIC FUNCTION
def get_heuristic(current_node: str, visited_nodes: frozenset) -> float:
    unvisited = ALL_NODES - visited_nodes
    if not unvisited:
        return 0.0
    return min(graph[current_node][t] for t in unvisited)


# 4. SEARCH ALGORITHMS (A* and UCS)
def perform_graph_search(start: str, use_heuristic: bool = True) -> tuple:
    """Executes Graph Search with state-reopening. Acts as A* if use_heuristic=True, or UCS if False."""
    initial_visited = frozenset([start])
    initial_h = get_heuristic(start, initial_visited) if use_heuristic else 0.0
    
    counter = itertools.count()
    pq = [(initial_h, 0, next(counter), start, [start], initial_visited)]
    best_g = {(start, initial_visited): 0.0}
    expanded_states_count = 0

    while pq:
        f, g, _, current, path, visited = heapq.heappop(pq)

        state_key = (current, visited)
        if g > best_g.get(state_key, float('inf')):
            continue
        
        if len(visited) == len(ALL_NODES):
            return path, g, expanded_states_count
            
        expanded_states_count += 1
        
        for neighbor, travel_cost in graph[current].items():
            new_path = path + [neighbor]
            new_visited = visited | frozenset([neighbor])
            g_new = g + travel_cost
            successor_key = (neighbor, new_visited)
            
            if g_new < best_g.get(successor_key, float('inf')):
                best_g[successor_key] = g_new
                h_new = get_heuristic(neighbor, new_visited) if use_heuristic else 0.0
                f_new = g_new + h_new
                heapq.heappush(pq, (f_new, g_new, next(counter), neighbor, new_path, new_visited))
                
    return None, float('inf'), expanded_states_count

def perform_brute_force(start: str) -> tuple:
    """Exhaustive Evaluation to strictly prove global optimum & worst-case route."""
    # Deterministic sorting prevents variable output across different OS environments
    destinations = sorted(list(ALL_NODES - {start}))
    best_cost, worst_cost = float('inf'), -float('inf')
    best_path, worst_path = None, None
    perm_count = 0
    
    for perm in itertools.permutations(destinations):
        perm_count += 1
        current, cost, path = start, 0, [start]
        for nxt in perm:
            cost += graph[current][nxt]
            path.append(nxt)
            current = nxt
            
        if cost < best_cost:
            best_cost, best_path = cost, path
        if cost > worst_cost:
            worst_cost, worst_path = cost, path
            
    return best_path, best_cost, worst_path, worst_cost, perm_count


# 5. EXECUTION & TERMINAL DASHBOARD
if __name__ == "__main__":
    
    # 1. Verify Graph
    verify_graph_integrity()
    ti_violations = verify_metric_properties()
    
    # 2. Benchmark A* Search
    a_star_times = []
    for _ in range(1000):
        start_time = time.perf_counter()
        optimal_route, total_distance, a_star_expanded = perform_graph_search("Sunway University", use_heuristic=True)
        a_star_times.append((time.perf_counter() - start_time) * 1000)
    exec_time_ms = statistics.median(a_star_times)
    
    if optimal_route is None:
        raise RuntimeError("ERROR: No valid route could be found. Graph may be disconnected.")
    
    # 3. Benchmark UCS Baseline
    ucs_times = []
    for _ in range(1000):
        start_time = time.perf_counter()
        _, _, ucs_expanded = perform_graph_search("Sunway University", use_heuristic=False)
        ucs_times.append((time.perf_counter() - start_time) * 1000)
    ucs_time_ms = statistics.median(ucs_times)

    # 4. Benchmark Brute-Force
    bf_times = []
    for _ in range(1000):
        start_time = time.perf_counter()
        _, bf_best_cost, worst_route, worst_cost, total_perms = perform_brute_force("Sunway University")
        bf_times.append((time.perf_counter() - start_time) * 1000)
    bf_time_ms = statistics.median(bf_times)

    if abs(total_distance - bf_best_cost) >= 1e-9:
        raise RuntimeError("CRITICAL ERROR: A* did not find the optimal route!")

    # 5. Calculate Environmental Metrics
    est_time_mins = (total_distance / AVG_SPEED_KMH) * 60
    fuel_consumed = total_distance * FUEL_RATE_L_PER_KM
    co2_emissions = fuel_consumed * CO2_RATE_KG_PER_L

    W = 140

    print("\n" + "═"*W)
    print("             CSC3206 AI ASSIGNMENT 2 — HOUSE TOUR OPTIMIZER             ".center(W))
    print("═"*W)
    print("  [ SYSTEM VERIFICATION & BASELINES ]")
    print("  • Graph Integrity : PASSED (Symmetry & Completeness Verified)")
    
    if ti_violations:
        print(f"  • Metric Warning  : {len(ti_violations)} Triangle Inequality violations detected (Minor urban routing detours exist):")
        for u, v, w, direct_dist, detour_dist in ti_violations:
            print(f"                      ➔ {u} to {w} ({direct_dist:.2f} km) > via {v} ({detour_dist:.2f} km)")
        
    print(f"  • UCS Baseline    : {ucs_expanded} states expanded | Exec Time: {ucs_time_ms:.3f} ms")
    print(f"  • Brute-Force     : {total_perms} permutations   | Exec Time: {bf_time_ms:.3f} ms")
    print(f"  • Worst-Case Route: {worst_cost:.2f} km")
    print("─"*W)
    print("  [ A* OPTIMIZATION RESULTS ]")
    print("  • Search Strategy : A* Graph Search (Nearest-Node Heuristic)")
    print(f"  • Total Cost      : {total_distance:.2f} km")
    print(f"  • Est. Drive Time : {est_time_mins:.2f} min")
    print(f"  • Fuel Estimated  : {fuel_consumed:.2f} L")
    print(f"  • CO2 Emissions   : {co2_emissions:.2f} kg")
    print(f"  • States Expanded : {a_star_expanded} states (Expanded {ucs_expanded - a_star_expanded} fewer states than UCS)")
    print(f"  • Execution Time  : {exec_time_ms:.3f} ms (Median over 1,000 runs)")
    print("─"*W)
    print(f"  {'Step':<6} | {'Location':<27} | {'Group Member':<20} | {'Leg':<10} | {'Total':<10}")
    print("─"*W)

    cumulative = 0.0
    for i, loc in enumerate(optimal_route):
        member = member_mapping.get(loc, "Tour Origin Point")
        if i == 0:
            leg_str = "0.00 km"
            cum_str = "0.00 km"
        else:
            prev = optimal_route[i-1]
            step_cost = graph[prev][loc]
            cumulative += step_cost
            leg_str = f"+{step_cost:.2f} km"
            cum_str = f"{cumulative:.2f} km"
            
        print(f"  [{i}]    | {loc:<27} | {member:<20} | {leg_str:<10} | {cum_str:<10}")

    print("─"*W)
    print("  OPTIMAL TRAVERSAL SEQUENCE:")
    path_short = " ➔ ".join(optimal_route)
    print(f"  {path_short}")
    print("═"*W + "\n")

    # 6. GRAPHICAL MAP VISUALIZATION
    G = nx.Graph()
    for src, destinations in graph.items():
        for dest, dist in destinations.items():
            G.add_edge(src, dest, weight=dist)

    plt.figure(figsize=(13, 9))

    pos = {
        "Sunway University": (101.6055, 3.0720),
        "Nadayu28 Residences": (101.5990, 3.0645),
        "Bandar Puteri Puchong": (101.6155, 3.0185),
        "Puchong Perdana": (101.5975, 3.0035),
        "Taman Puchong Utama": (101.6080, 2.9930),
        "Taman Putra Prima": (101.5940, 2.9735)
    }

    node_labels = {}
    for node in G.nodes():
        if node in member_mapping:
            node_labels[node] = f"{node}\n[{member_mapping[node]}]"
        else:
            node_labels[node] = node

    nx.draw_networkx_nodes(G, pos, node_color='#a2d2ff', node_size=900, edgecolors='black')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='#bde0fe', width=1.5, style='dashed')

    route_edges = [(optimal_route[i], optimal_route[i+1]) for i in range(len(optimal_route)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='#ff006e', width=4, label="Optimized Tour Route")

    # VISUAL FIX: label_pos=0.3 pushes the text slightly off-center to prevent overlap with the line!
    edge_labels = nx.get_edge_attributes(G, 'weight')
    formatted_labels = {k: f"{v}km" for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_labels, font_size=8, font_color='#2b2d42', label_pos=0.3)

    plt.title(f"Topological Representation of House Tour Network\n(A* Optimized Path Total Cost: {total_distance:.2f}km)", fontsize=13, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("route_map.png", dpi=300, bbox_inches="tight")
    if matplotlib.get_backend().lower() != 'agg':
        plt.show()