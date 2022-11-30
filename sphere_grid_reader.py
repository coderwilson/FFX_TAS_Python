# Libraries and Core Files
import memory.main
from memory.sphere_grid import SphereNodeType, sphere_grid
from players import Auron, Kimahri, Lulu, Rikku, Tidus, Wakka, Yuna

"""
NOTE! This file is intended as an example of how to use the sphere grid API,
it's a test file with its own main, and should not be imported into the TAS.

Use the sphere_grid object imported from memory.sphere_grid when implementing
the functionality in the TAS.
"""


if __name__ == "__main__":
    # Wait for memory to finish loading
    while not memory.main.start():
        pass

    # Example code to read a particular node at an arbitrary position
    node_123 = sphere_grid.get_node_at(123)
    print(f"Node at idx=123 is {node_123}")

    last_node = 0
    while True:
        # ID of the node currently selected by the GUI
        cur_node = sphere_grid.get_current_node_idx()
        if cur_node != last_node:
            # The actual node selected by the GUI
            node = sphere_grid.get_current_node()
            # Print the node indices of all the players
            print(
                f"Positions: [Tidus={sphere_grid.get_player_node_idx(Tidus.id)}] [Yuna={sphere_grid.get_player_node_idx(Yuna.id)}] [Auron={sphere_grid.get_player_node_idx(Auron.id)}] [Kimahri={sphere_grid.get_player_node_idx(Kimahri.id)}] [Wakka={sphere_grid.get_player_node_idx(Wakka.id)}] [Lulu={sphere_grid.get_player_node_idx(Lulu.id)}] [Rikku={sphere_grid.get_player_node_idx(Rikku.id)}]"
            )
            # Print the currently selected node and a bitfield of what characters have activated it
            print(
                f"New node: {cur_node}, type {node}, activation: {hex(node.get_activated_by())}"
            )

            # Example check for activation by Yuna
            if node.is_activated_by(Yuna.id):
                print(f"Node {node} is activated by Yuna")

            # Example comparison of current node to the enum list
            if node.get_node_type() == SphereNodeType.Flare:
                print("The currently selected node is the Flare spell!")
        # Just to prevent spam, only print the info once
        last_node = cur_node
