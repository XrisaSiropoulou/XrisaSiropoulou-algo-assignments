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

def bfs(graph, seeds, p):
    return

def monte_carlo(graph, seeds, p, iterations=1000):
    return

def select_seed_out_degree(graph, selected_seeds):
    return

def select_seed_greedy(graph, selected_seeds, p):
    return 

def maximize_influence(graph, p, k, method):
    return 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Influence Maximization')
    parser.add_argument('input_file', type=str, help='Input file containing the graph')
    parser.add_argument('k', type=int, help='Number of seeds to select')
    parser.add_argument('method', type=str, choices=['out-degree', 'greedy'], help='Seed selection method')
    parser.add_argument('p', type=float, help='Influence probability')
    parser.add_argument('mc', type=float, help='Monte Carlo')
    parser.add_argument('-r', type=int, help='Seed')
    args = parser.parse_args()

    graph = read_graph(args.input_file)
    seeds, influence = maximize_influence(graph, args.p, args.k, args.m)
    print(f"Seeds: {seeds}")
    print(f"Influences: {influence}")
