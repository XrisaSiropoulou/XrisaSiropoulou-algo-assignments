import sys
import argparse
from collections import defaultdict, deque
import random

def read_graph(input_file):
    graph = defaultdict(list)
    with open(input_file, 'r') as file:
        for line in file:
            u = int(line.strip().split()[0])
            v = int(line.strip().split()[1])
            graph[u].append(v)
    return graph

def icm_step(graph, seeds, p):
    active_nodes = set(seeds)
    new_nodes = set(seeds)
    while new_nodes:
        next_new_nodes = []
        for node in new_nodes:
            for neighbor in graph[node]:
                if neighbor not in active_nodes:
                    if random.random() < p:
                        next_new_nodes.append(neighbor)
                        active_nodes.add(neighbor)
        new_nodes = next_new_nodes
    
    return active_nodes

def monte_carlo(graph, seeds, p, iterations):
    influence = {seed: 0 for seed in seeds}
    for i in range(iterations):
        iter_seed=[]
        for seed in seeds:
            iter_seed.append(seed)
            influenced_nodes = icm_step(graph, iter_seed, p)
            influence[seed] += len(influenced_nodes)

    for seed, count in influence.items():
        influence[seed] = count / iterations
    
    return influence

def select_seeds_out_degree(graph, k):
    seeds=[]
    sorted_items = sorted(graph.items(), key=lambda item: (-len(item[1]), item[0]))
    for item in sorted_items[:k]:
        seeds.append(item[0])
    return seeds

def select_seeds_greedy(graph, k, p, iterations):
    used_nodes=[]
    nodes = set(graph.keys())
    for i in range(k):
        max_inf = -1
        for seed in nodes:
            if seed not in used_nodes:
                temp_inf = monte_carlo(graph, used_nodes + [seed], p, iterations)
                if temp_inf[seed] > max_inf:
                    max_inf = temp_inf[seed]
                    temp_seed=seed
                    influence = temp_inf
        used_nodes.append(temp_seed)
    return used_nodes, influence

def maximize_influence(graph, p, k, method, iterations):
    if method == 'max_degree':
        seeds = select_seeds_out_degree(graph, k)
        influence = monte_carlo(graph, seeds, p, iterations)
    elif method == 'greedy':
        seeds, influence = select_seeds_greedy(graph, k, p, iterations)
    return seeds, influence 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Influence Maximization')
    parser.add_argument('input_file', type=str, help='Input file containing the graph')
    parser.add_argument('k', type=int, help='Number of seeds to select')
    parser.add_argument('method', type=str, choices=['max_degree', 'greedy'], help='Seed selection method')
    parser.add_argument('p', type=float, help='Influence probability')
    parser.add_argument('mc', type=int, help='Monte Carlo')
    parser.add_argument('-r', type=int, help='Seed')
    args = parser.parse_args()
    
    random.seed(args.r)
    graph = read_graph(args.input_file)
    seeds, influence = maximize_influence(graph, args.p, args.k, args.method, args.mc)
    inf=[]
    for item in influence:
       inf.append(influence[item])
    print(f"Seeds: {seeds}")
    print(f"Influences: {inf}")


