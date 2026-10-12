from network.node import Node


class Renderer:
    __slots__ = ['render_queue']
    def __init__(self):
        self.render_queue = []

    def add_to_queue(self, node: Node):
        self.render_queue.append(node)

    def render(self):
        for node in self.render_queue:
            node.render()

