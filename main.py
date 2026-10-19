from physics.engine import Engine
from physics.feedline import Feedline
from physics.tank import Tank
from physics.valve import Valve
from renderer.renderer import Renderer
from solver.solver_main import Solver

if __name__ == '__main__':
    renderer = Renderer()

    tank = Tank(name="Main Tank", volume=1000.0, mass=100.0, Cd=0.6, radius=0.1)
    feedline = Feedline(name="Main Feedline", flow_coefficient=0.8)
    valve = Valve(name="Main Valve", is_open=True)
    engine = Engine(name="Engine")

    tank.connect(feedline)
    feedline.connect(valve)
    valve.connect(engine)

    solver = Solver(tank)

    result = solver.solve([0.0, 0.0])

    feedline.calculate_residuals(result.x)
    print("feedline:", feedline.interfaces)
    print("valve:", valve.interfaces)
    print("engine:", engine.interfaces, engine.v_e)
    print("thrust:", engine.interfaces["downstream_mass_flow_rate"] * engine.v_e)
    print("solver result:", result.x)
    print("solver residuals:", result.fun)

    renderer.add_to_queue(feedline)
    renderer.add_to_queue(valve)