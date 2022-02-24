from reprandom import rr
from graph import Graph
from typing import List


def _random_set(v: List[int], size: int):
    v_cop = v.copy()
    set = []
    while(len(set) < size):
        if v_cop == []:
            return set
        num = rr.randint(0, len(v_cop) - 1)
        set.append(v_cop[num])
        del v_cop[num]
    return set


def gen(
    max_a: int,
    min_ne: int, max_ne: int,
    min_soe: int, max_soe: int,
    min_sog: int, max_sog: int,
    att_prob: float
):
    a = rr.randint(1, max_a)
    x = rr.randint(min_ne, max_ne)
    s = rr.randint(min_soe, max_soe)
    r = rr.randint(min_sog, max_sog)
    g = Graph(list(range(1, a+1)))
    # grounded = list(range(1, R + 1))
    for i in range(1, r + 1):
        for k in range(i):
            if (rr.random() < att_prob):
                g.edges.append((g.vertices[i - 1], g.vertices[k]))
    for _ in range(1, x+1):
        m = _random_set(g.vertices, s)
        for i in range(r + 1, a + 1):
            if not g.vertices[i - 1] in m:
                ak = m[rr.randint(0, len(m) - 1)]
                g.edges.append((ak, g.vertices[i - 1]))
    return g
