from physics.feedline import Feedline
from physics.valve import Valve
from renderer.renderer import Renderer
from solver.solver_main import Solver

if __name__ == '__main__':
    renderer = Renderer()

    feedline = Feedline(name="Main Feedline", flow_coefficient=0.8)
    valve = Valve(name="Main Valve", is_open=True)

    feedline.connect(valve)

    solver = Solver(feedline)

    result = solver.solve([1.0, 0.0, 1.0, 0.0])

    print(feedline.interfaces)
    print(feedline.connections[0].interfaces)
    print("solver result:", result.x)

    renderer.add_to_queue(feedline)
    renderer.add_to_queue(valve)