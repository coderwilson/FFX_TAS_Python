# Libraries and Core Files
import memory.main
from memory.sphere_grid import SphereNodeType, sphere_grid

# Wait for memory to finish loading
while not memory.main.start():
    pass


# Example code to read a particular node
node_123 = sphere_grid.get_node_at(123)

print(f"Node at idx=123 is {node_123}")

last_node = 0
while True:
    cur_node = sphere_grid._get_current_node_idx()
    if cur_node != last_node:
        node = sphere_grid.get_current_node()
        print(
            f"New node: {cur_node}, type {node}, activation: {hex(node.get_activated_by())}"
        )

        # Example check for activation by Yuna
        if node.is_activated_by(1):
            print(f"Node {node} is activated by Yuna")

        # Example comparison of current node
        if node.get_node_type() == SphereNodeType.Flare:
            print("The currently selected node is the Flare spell!")

    last_node = cur_node
