import sys
import argparse
import random
from collections import deque

def bfs(graph, seeds, p):
    return ''

def monte_carlo(graph, seeds, p, iterations=1000):
    return ''

def select_seed_out_degree(graph, selected_seeds):
    return ''

def select_seed_greedy(graph, selected_seeds, p):
    return ''

def maximize_influence(graph, p, k, method):
    seeds = set()
    for _ in range(k):
        if method == 'out-degree':
            seed = select_seed_out_degree(graph, seeds)
        elif method == 'greedy':
            seed = select_seed_greedy(graph, seeds, p)
        seeds.add(seed)
    return seeds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Influence Maximization')
    parser.add_argument('input_file', type=str, help='Input file containing the graph')
    parser.add_argument('p', type=float, help='Influence probability')
    parser.add_argument('k', type=int, help='Number of seeds to select')
    parser.add_argument('method', type=str, choices=['out-degree', 'greedy'], help='Seed selection method')
    args = parser.parse_args()

    
    graph = {}#from file

    seeds = maximize_influence(graph, args.p, args.k, args.method)
    print(seeds)