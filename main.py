from physics.feedline import Feedline
from physics.valve import Valve
from renderer.renderer import Renderer

if __name__ == '__main__':
    renderer = Renderer()

    feedline = Feedline(name="Main Feedline", flow_coefficient=0.8)
    valve = Valve(name="Main Valve", is_open=True)



    renderer.add_to_queue(feedline)
    renderer.add_to_queue(valve)