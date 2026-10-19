from physics.engine import Engine
from physics.feedline import Feedline
from physics.valve import Valve
from renderer.renderer import Renderer
from solver.solver_main import Solver

if __name__ == '__main__':
    renderer = Renderer()

    feedline = Feedline(name="Main Feedline", flow_coefficient=0.8)
    valve = Valve(name="Main Valve", is_open=True)
    engine = Engine(name="Engine")

    feedline.connect(valve)
    valve.connect(engine)

    solver = Solver(feedline)

    result = solver.solve([100.0, 0.0])

    feedline.calculate_residuals(result.x)
    print("feedline:", feedline.interfaces)
    print("valve:", valve.interfaces)
    print("engine:", engine.interfaces)
    print("solver result:", result.x)
    print("solver residuals:", result.fun)

    renderer.add_to_queue(feedline)
    renderer.add_to_queue(valve)