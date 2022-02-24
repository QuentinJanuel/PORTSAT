import os


class Graph:
    def __init__(
        self,
        vertices: list[int],
        edges: list[tuple[int, int]] = [],
    ):
        self.vertices = vertices
        self.edges = edges

    def save(self, file_name: str):
        if not os.path.exists("graph"):
            os.makedirs("graph")
        with open(f"graph/{file_name}", "w") as file:
            for v in self.vertices:
                file.write(f"{v}\n")
            file.write("#\n")
            for v1, v2 in self.edges:
                file.write(f"{v1} {v2}\n")
