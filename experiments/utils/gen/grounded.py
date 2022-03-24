from utils.reprandom import rr
from utils.graph import Graph


def gen(max_a: int, att_prob: float):
    a = rr.randint(1, max_a)
    unconnected = list(range(1, a + 1))
    g = Graph([str(n) for n in range(1, a + 1)])
    for i in range(a):
        for j in range(i - 1):
            if rr.random() < att_prob:
                g.edges.append((g.vertices[i], g.vertices[j]))
                try:
                    unconnected.remove(i + 1)
                except ValueError:
                    continue
    for b in unconnected:
        k = rr.randint(0, a - 1)
        if rr.randint(0, 1) == 0:
            g.edges.append((str(b), g.vertices[k]))
        else:
            g.edges.append((g.vertices[k], str(b)))
    return g
