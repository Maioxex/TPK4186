import random
import csv
import os
from threading import Lock

class Container:
    def __init__(self, code, size, weight):
        self.code = code
        self.size = size
        self.weight = weight
        
    def get_code(self):
        return self.code
    
    def get_size(self):
        return self.size
    
    def get_weight(self):
        return self.weight
    
    def set_size(self, new_size):
        self.size = new_size
        
    def set_weight(self, new_weight):
        self.weight = new_weight
        
class ContainerSet:
    def __init__(self):
        self.containers = []
        
    def add_container(self, container):
        self.containers.append(container)
        
    def remove_container(self, code):
        for container in self.containers:
            if container.get_code() == code:
                self.containers.remove(container)
                return True
        return False
    
    def find_container(self, code):
        for container in self.containers:
            if container.get_code() == code:
                return container
        return None

def generate_random_container():
    length_options = [20, 40]
    length = random.choice(length_options)
    
    if length == 20:
        max_load = 20
    else:
        max_load = 22
    load = random.randint(0, max_load)
    
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
    
    return Container(code, length, load)

def generate_random_container_set(num_containers):
    container_set = ContainerSet()
    for i in range(num_containers):
        container = generate_random_container()
        container_set.add_container(container)
    return container_set


def write_container_set_to_file(container_set, file_name = "ContainerList.csv"):
    # Create the file if it doesn't exist
    if not os.path.exists(file_name):
        open(file_name, 'w').close()

    with open(file_name, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for container in container_set.containers:
            writer.writerow([container.get_code(), container.get_size(), container.get_weight()])
            
def load_container_set_from_file(file_name = "ContainerList.csv"):
    container_set = ContainerSet()
    with open(file_name, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            code = row[0]
            size = int(row[1])
            weight = int(row[2])
            container = Container(code, size, weight)
            container_set.add_container(container)
    return container_set

# listo = generate_random_container_set(10)
# write_container_set_to_file(listo)
# listo = load_container_set_from_file()
# for each in listo.containers:
#     print(each.get_code())
    
class ContainerShip:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.bays = [[[None for _ in range(height)] for _ in range(width)] for _ in range(length)]
        
    
    def find_container(self, container_code):
        for i in range(self.length):
            for j in range(self.width):
                for k in range(self.height):
                    if self.bays[i][j][k] is not None and self.bays[i][j][k].get_code() == container_code:
                        return (i, j, k)
        return None
    
    def find_available_bay(self, container_size):
        if container_size == 20:
            for i in range(self.length):
                for j in range(self.width):
                    for k in range(self.height):
                        if self.bays[i][j][k] is None:
                            return (i, j, k)
        elif container_size == 40:
            for i in range(self.length):
                for j in range(self.width):
                    for k in range(self.height):
                        if k + 1 < self.height and all(self.bays[i][j][l] is None for l in range(k, k + 2)):
                            return (i, j, k)
        return None
    
    def load_container(self, container, bay):
        if self.bays[bay[0]][bay[1]][bay[2]] is not None:
            return False
        if container.get_size() == 20:
            self.bays[bay[0]][bay[1]][bay[2]] = container
            return True
        elif container.get_size() == 40:
            if bay[2] + 1 >= self.height or self.bays[bay[0]][bay[1]][bay[2] + 1] is not None:
                return False
            self.bays[bay[0]][bay[1]][bay[2]] = container
            self.bays[bay[0]][bay[1]][bay[2] + 1] = container
            return True
    
    def remove_container(self, container_code):
        bay = self.find_container(container_code)
        if bay is None:
            return False
        self.bays[bay[0]][bay[1]][bay[2]] = None
        if bay[2] + 1 < self.height and self.bays[bay[0]][bay[1]][bay[2] + 1] is not None:
            self.bays[bay[0]][bay[1]][bay[2] + 1] = None
        return True
def print_ship_load_to_file(ship, filename):
    """
    Prints the load of a ship into a TSV file.

    Args:
        ship (ContainerShip): the ship whose load should be printed.
        filename (str): the name of the output file.
    """
    with open(filename, 'w') as file:
        file.write('container_code\tlength\tweight_empty\tweight_loaded\tposition_bay\tposition_row\tposition_tier\n')
        for container in ship.containers:
            file.write(f"{container.code}\t{container.length}\t{container.weight_empty}\t{container.weight_loaded}\t{container.position.bay}\t{container.position.row}\t{container.position.tier}\n")


def load_ship_load_from_file(ship, filename = "ContainerShipList.csv"):
    """
    Loads the load of a ship from a TSV file.

    Args:
        ship (ContainerShip): the ship to load the containers into.
        filename (str): the name of the input file.
    """
    with open(filename, 'r') as file:
        # Skip the header line
        next(file)
        for line in file:
            values = line.strip().split('\t')
            code = values[0]
            length = int(values[1])
            weight_empty = int(values[2])
            weight_loaded = int(values[3])
            position_bay = int(values[4])
            position_row = int(values[5])
            position_tier = int(values[6])
            position = ContainerPosition(position_bay, position_row, position_tier)
            container = Container(code, length, weight_empty, weight_loaded, position)
            ship.load_container(container)
class ContainerPosition:
    def __init__(self, bay, row, tier):
        self.bay = bay
        self.row = row
        self.tier = tier
def unload_ship(ship):
    """
    Unload a ship container by container and creates the corresponding ordered list of containers.
    Returns a list of the unloaded containers in the order they were unloaded.
    """
    unloaded_containers = []
    while ship.containers:
        last_container = ship.containers.pop()
        unloaded_containers.insert(0, last_container)
        unload_container(ship, last_container)
    return unloaded_containers
def load_ship(ship, containers):
    """
    Load a ship container by container from a set of containers.
    Returns a list of the loaded containers in the order they were loaded.
    """
    loaded_containers = []
    for container in containers:
        if can_load_container(ship, container):
            load_container(ship, container)
            loaded_containers.append(container)
        else:
            while loaded_containers and not can_load_container(ship, container):
                last_container = loaded_containers.pop()
                unload_container(ship, last_container)
            if can_load_container(ship, container):
                load_container(ship, container)
                loaded_containers.append(container)
    return loaded_containers

def can_load_container(ship, container):
    if container['size'] == '20':
        for i in range(ship['L']):
            for j in range(ship['W']):
                for k in range(ship['H']):
                    if k == 0 and not any(ship['grid'][i][j][k]):
                        return True
                    elif not ship['grid'][i][j][k] and ship['grid'][i][j][k-1]:
                        top_container = ship['grid'][i][j][k-1]
                        if top_container['weight_loaded'] >= container['weight_loaded']:
                            return True
    elif container['size'] == '40':
        for i in range(ship['L']):
            for j in range(ship['W']):
                for k in range(ship['H']):
                    if k == 0 and not any(ship['grid'][i][j][k]) and j < ship['W'] - 1:
                        if not any(ship['grid'][i][j+1][k]):
                            return True
                    elif j == ship['W'] - 1 and k == 0 and not any(ship['grid'][i][j][k]):
                        return True
                    elif not ship['grid'][i][j][k] and ship['grid'][i][j][k-1]:
                        top_container = ship['grid'][i][j][k-1]
                        if top_container['weight_loaded'] >= container['weight_loaded']:
                            if j == ship['W'] - 1:
                                if not any(ship['grid'][i+1][0][k]):
                                    return True
                            else:
                                if not any(ship['grid'][i][j+1][k]):
                                    return True
    return False

def load_container(ship, container):
    """
    Load a container into the ship if it satisfies the stability constraints.

    Parameters:
    ship (Ship): The ship to load the container onto.
    container (Container): The container to load onto the ship.

    Returns:
    bool: True if the container was loaded, False otherwise.
    """
    if can_load_container(ship, container):
        # Try to load the container into an empty slot
        for bay in range(len(ship.layout)):
            for row in range(len(ship.layout[bay])):
                for col in range(len(ship.layout[bay][row])):
                    if ship.layout[bay][row][col] is None:
                        if container.length == 1:
                            # For a 20-ft container
                            weight = container.weight_loaded
                        else:
                            # For a 40-ft container
                            weight = container.weight_loaded + container.weight_empty
                        ship.layout[bay][row][col] = (container, weight)
                        ship.total_weight += weight
                        # Update the weights for starboard and portside
                        if col < ship.width // 2:
                            ship.starboard_weight += weight
                        else:
                            ship.portside_weight += weight
                        # Update the weights for the first, middle, and last sections
                        if bay < ship.length // 3:
                            ship.first_section_weight += weight
                        elif bay < 2 * ship.length // 3:
                            ship.middle_section_weight += weight
                        else:
                            ship.last_section_weight += weight
                        return True
        # Try to load the container by removing a previously loaded container
        for bay in reversed(range(len(ship.layout))):
            for row in reversed(range(len(ship.layout[bay]))):
                for col in reversed(range(len(ship.layout[bay][row]))):
                    if ship.layout[bay][row][col] is not None:
                        prev_container, prev_weight = ship.layout[bay][row][col]
                        if can_load_container(ship, prev_container, container):
                            # Unload the previously loaded container
                            ship.layout[bay][row][col] = None
                            ship.total_weight -= prev_weight
                            # Update the weights for starboard and portside
                            if col < ship.width // 2:
                                ship.starboard_weight -= prev_weight
                            else:
                                ship.portside_weight -= prev_weight
                            # Update the weights for the first, middle, and last sections
                            if bay < ship.length // 3:
                                ship.first_section_weight -= prev_weight
                            elif bay < 2 * ship.length // 3:
                                ship.middle_section_weight -= prev_weight
                            else:
                                ship.last_section_weight -= prev_weight
                            # Load the new container
                            if container.length == 1:
                                # For a 20-ft container
                                weight = container.weight_loaded
                            else:
                                # For a 40-ft container
                                weight = container.weight_loaded + container.weight_empty
                            ship.layout[bay][row][col] = (container, weight)
                            ship.total_weight += weight
                            # Update the weights for starboard and portside
                            if col < ship.width // 2:
                                ship.starboard_weight += weight
                            else:
                                ship.portside_weight += weight
                            # Update the weights for the first, middle, and last sections
                            if bay < ship.length // 3:
                                ship.first_section_weight += weight
                            elif bay < 2 * ship.length // 3:
                                ship.middle_section_weight += weight
                            else:
                                ship.last_section_weight += weight
                            return True
    return False

def unload_container(ship, container_id):
    """
    Unloads the container with the given ID from the ship and returns it.

    Args:
        ship (Ship): The ship to unload the container from.
        container_id (int): The ID of the container to unload.

    Returns:
        Container: The unloaded container, or None if the container was not found on the ship.
    """
    for bay in reversed(ship.bays):
        for i, container in enumerate(bay):
            if container and container.id == container_id:
                container = bay.pop(i)
                return container
    return None

def calculate_total_weight(ship):
    """
    Calculates the total weight of containers loaded in the ship.

    Args:
        ship: An instance of the Ship class.

    Returns:
        The total weight of containers loaded in the ship.
    """
    total_weight = 0
    for container in ship.containers:
        total_weight += container.loaded_weight
    return total_weight


def calculate_starboard_portside_weight(ship):
    """
    Calculates the total weight of containers loaded on starboard and on portside of the ship.

    Args:
        ship: An instance of the Ship class.

    Returns:
        A tuple with the total weight of containers loaded on starboard and on portside of the ship.
    """
    starboard_weight = 0
    portside_weight = 0
    for container in ship.containers:
        if container.location.startswith("S"):
            starboard_weight += container.loaded_weight
        else:
            portside_weight += container.loaded_weight
    return starboard_weight, portside_weight


def calculate_section_weight(ship):
    """
    Calculates the total weight of containers loaded in the first, middle and last section of the ship.

    Args:
        ship: An instance of the Ship class.

    Returns:
        A tuple with the total weight of containers loaded in the first, middle and last section of the ship.
    """
    section_lengths = [int(ship.width/3), int(ship.width/3), ship.width - 2*int(ship.width/3)]
    section_weights = [0] * 3
    current_section = 0
    for container in ship.containers:
        while current_section < len(section_lengths) - 1 and container.position[1] >= section_lengths[current_section]:
            current_section += 1
        section_weights[current_section] += container.loaded_weight
    return tuple(section_weights)


def is_load_balanced(ship, x=5, y=10):
    """
    Checks if the load of the ship is balanced.

    Args:
        ship: An instance of the Ship class.
        x: The maximum percentage difference allowed between the weight on starboard and on portside of the ship.
        y: The maximum percentage difference allowed between the weight on a section of the ship and another section.

    Returns:
        True if the load of the ship is balanced, False otherwise.
    """
    total_weight = calculate_total_weight(ship)
    starboard_weight, portside_weight = calculate_starboard_portside_weight(ship)
    section_weights = calculate_section_weight(ship)

    # Check starboard and portside balance
    max_diff = max(starboard_weight, portside_weight) * x / 100
    if abs(starboard_weight - portside_weight) > max_diff:
        return False

    # Check section balance
    for i in range(len(section_weights)):
        max_diff = section_weights[i] * y / 100
        for j in range(i + 1, len(section_weights)):
            if abs(section_weights[i] - section_weights[j]) > max_diff:
                return False

    return True
# Initialize the available and occupied bays data structure
available_bays = set((section, row, col) for section in range(1, 5)
                     for row in range(1, N+1) for col in range(1, M+1))
occupied_bays = set()


def load_container(ship, container, port=True):
    if not can_load_container(ship, container):
        return False

    if port:
        sections = ship.port_sections
        cranes = ship.port_cranes
    else:
        sections = ship.starboard_sections
        cranes = ship.starboard_cranes

    # Acquire the lock before accessing the shared resource
    for i in range(len(sections)):
        with cranes[i], sections[i].lock:
            if can_load_container_in_section(sections[i], container):
                load_container_in_section(sections[i], container)
                return True
    return False

def unload_container(container):
    # Try to find an occupied bay in the same section that is not adjacent to another occupied bay
    for section in range(1, 5):
        section_bays = [(row, col) for (s, row, col) in occupied_bays if s == section]
        for (row, col) in section_bays:
