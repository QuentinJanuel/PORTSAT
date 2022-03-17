from utils.reprandom import rr
from utils.graph import Graph


def gen(
    max_a: int,
    max_num_scc: int,
    att_prob_inner: float,
    att_prob_outer: float,
    connect_prob:float,
):
    a = rr.randint(1, max_a)
    n = rr.randint(1, max_num_scc)
    g = Graph(list(range(1, a+1)))
    c = [[]]*n
    for i in range (a):
        k = rr.randint(0, n-1)
        c[k].append(g.vertices[i])
    for i in range(n):
        for arg1 in c[i]:
            for arg2 in c[i]:
                if (rr.random() < att_prob_inner):
                    g.edges.append((arg1,arg2))
    for i in range(n-1):
        for j in range(i+1,n):
            if (rr.random() < connect_prob):
                for arg1 in c[i]:
                    for arg2 in c[j]:
                        if (rr.random() < att_prob_outer):
                            g.edges.append((arg1,arg2))
    return g