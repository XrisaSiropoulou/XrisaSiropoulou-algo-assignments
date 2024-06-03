import math
import argparse


def run_viterbi(X, k, lambdas, d):
    n = len(X)
    C = [[float('inf')] * (k) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(k)]

    # Initial condition
    C[0][0] = 0

    for t in range(1, n + 1):
        for s in range(k):
            l_min = 0
            c_min = C[t - 1][0] + ti(0, s, n)
            for l in range(1, k):
                c = C[t - 1][l] + ti(l, s, n)
                if c < c_min:
                    c_min = c
                    l_min = l
            C[t][s] = c_min - math.log(lambdas[s] * math.exp(-(lambdas[s] * X[t - 1])))
            P[s][0:t] = P[l_min][0:t]
            P[s][t] = s
    if d:
        print(f"Time step {t}:")
        print("C matrix:")
        for row in C:
            print(row)

    l_min = 0
    c_min = C[n][0]
    for s in range(1, k):
        if C[n][s] < c_min:
            c_min = C[n][s]
            l_min = s

    return P[l_min][:n + 1]


def ti(i, j, n):
    if j > i:
        return (1 * (j - i) * math.log(n))  # gamma
    else:
        return 0


def identify_intervals(S, X):
    intervals = []
    start = 0
    current_state = S[0]

    for t in range(1, len(S)):
        if S[t] != current_state:
            intervals.append((current_state, X[start], X[t]))
            current_state = S[t]
            start = t

    intervals.append((current_state, X[start], X[-1]))
    return intervals


# Transition cost function
def transition_cost(i, j, gamma, ln_n):
    if j > i:
        return gamma * (j - i) * ln_n
    else:
        return 0


def run_bellman(X, k, lambdas):
    n = len(X)
    C = [[float('inf')] * (k) for _ in range(n + 1)]
    P = [[0] * (n + 1) for _ in range(k)]

    # Initial condition
    C[0][0] = 0

    for t in range(1, n + 1):
        for s in range(k):
            l_min = 0
            c_min = C[t - 1][0] + ti(0, s, n)
            for l in range(1, k):
                c = C[t - 1][l] + ti(l, s, n)
                if c < c_min:
                    c_min = c
                    l_min = l
            C[t][s] = c_min - math.log(lambdas[s] * math.exp(-(lambdas[s] * (X[t - 1] - X[t - 2]))))  # change
            P[s][0:t] = P[l_min][0:t]
            P[s][t] = s
    '''
    if d:
        print(f"Time step {t}:")
        print("C matrix:")
        for row in C:
            print(row)
    '''
    l_min = 0
    c_min = C[n][0]
    for s in range(1, k):
        if C[n][s] < c_min:
            c_min = C[n][s]
            l_min = s

    return P[l_min][:n + 1]


def main():
    parser = argparse.ArgumentParser(description="Run bursts analysis")
    parser.add_argument("offsets_file", type=str)
    parser.add_argument("-s", type=float, default=2.0)
    parser.add_argument("-g", "--gamma", type=float, default=1.0)
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("mode", choices=["viterbi", "trellis"])

    args = parser.parse_args()
    with open(args.offsets_file, 'r') as file:
        first_line = file.readline().strip()
    X = [int(num) for num in first_line.split()]

    k = math.ceil(1 + math.log(X[-1], args.s) + math.log((1 / 1), args.s))  # Number of states
    lambdas = [(args.s ** i) / (X[-1] / len(X)) for i in range(k)]  # Exponential distribution parameters

    if args.mode == "viterbi":
        S = run_viterbi(X, k, lambdas, args.debug)
        intervals = identify_intervals(S, X)
        for state, start, end in intervals:
            print(f"{state}[{start},{end})")

    elif args.mode == "trellis":
        S = run_bellman(X, k, lambdas)
        intervals = identify_intervals(S, X)
        for state, start, end in intervals:
            print(f"{state}[{start},{end})")


if __name__ == "__main__":
    main()  