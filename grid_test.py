import memory.main
from sphere_grid.sphere_grid_library import SphereGrid, NODE_TYPE_MAP
import logging

logger = logging.getLogger(__name__)

# Make sure to update NODE_TYPE_MAP and SPHERE_UNLOCK_TYPE_MAP
# with your actual data before initializing SphereGrid.
# For instance:
# NODE_TYPE_MAP.update({
#     1: "Blank Node",
#     39: "Strength +1",
#     # ... more mappings ...
# })
# SPHERE_UNLOCK_TYPE_MAP.update({
#     0: "Power Sphere",
#     1: "Ability Sphere",
#     # ... more mappings based on node IDs or content ...
# })


memory.main.start()

grid_file_path = "sphere_grid/grid_info.json" # Adjust path as needed
my_sphere_grid = SphereGrid(grid_file_path)
test_node = 708

# print("=== First, sphere grid general test ===")
# print(my_sphere_grid.get_node_position(test_node))
# print(my_sphere_grid.get_node_unlock_sphere_type(test_node))
# print(my_sphere_grid.get_node_unlocked_by(test_node))
# print(my_sphere_grid.get_adjacent_nodes_ids(test_node))
# print("")
print("=== Distance test ===")
try:
    # tar_node, dist = my_sphere_grid.find_nearest_node_of_type(test_node, "Lv. 1 Lock")
    # print(f"Closest lock: {tar_node.id} | {dist}")
    tar_node, dist = my_sphere_grid.find_nearest_node_of_type(test_node, "Empty Node")
    print(f"Closest empty: {tar_node.id} | {dist}")
    
    # tar_node, dist = my_sphere_grid.find_nearest_unlocked_node_for_character(test_node, "Yuna")
    # print(f"Test 2: {tar_node}")
    # print(f"Test 3: {dist}")
    
except:
    pass

print("")
print("=== Now to get an individual node: ===")
# Example: Get info for node 0
node_info = my_sphere_grid.get_node(test_node)
print(node_info)
if node_info:
    print(f"Node Type: {node_info.current_node_type}")
    print(f"Node Position: {node_info.position}")
    print(f"Node Default Type: {node_info.default_node_type}")
    print(f"Node Unlocked By: {node_info.unlocked_by_characters}")

    # # Simulate memory reading update
    # node_info.set_unlocked_status("Auron", True)
    # print(f"Node Unlocked By (after update): {node_info.unlocked_by_characters}")

    print(f"Node Unlock Sphere: {node_info.sphere_type_unlocked_by}")


print("")
print("=== Now to get a character's position: ===")
for i in range(7):
    my_sphere_grid.character_at_node(i)
print("End")

# # Example: Get info for node 1 using helper methods
# print(f"\nNode 1 Position: {my_sphere_grid.get_node_position(1)}")
# print(f"Node 1 Default Type: {my_sphere_grid.get_node_default_type(1)}")
# print(f"Node 1 Unlock Sphere: {my_sphere_grid.get_node_unlock_sphere_type(1)}")
