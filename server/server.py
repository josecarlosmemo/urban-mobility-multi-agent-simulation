import asyncio
import websockets
import agentpy as ap
from enum import IntEnum
import random
import numpy as np


class TypesTiles():
    CITY = 0
    STREET = 1
    INTERSECTION = 2
    TRAFFIC_LIGHT = 3
    CAR = 4
    SPAWN = 5
    SWITCH_LANE = 6
    REVERSED_STREET = 7

class TrafficLightState(IntEnum):
    RED = 0
    GREEN = 1
    YELLOW = 2

class CarState(IntEnum):
    HAS_TOUCHED_INTERSECTION = 0
    HAS_NOT_TOUCHED_INTERSECTION = 1
    STOP_LIGHT = 2
    TO_STREET = 3

dirs =  {
            "N": (1, 0),
            "S": (-1, 0),
            "E": (0, 1),
            "W": (0, -1)
        }

traffic_order = {
    "N": 0,
    "E": 1,
    "W": 2,
    "S": 3
}

class Car(ap.Agent):
    """
    Represents a car agent in the simulation.

    Attributes:
        from_dir (str): The direction of the lane where the car spawns.
        to_dir (str): The direction of the lane where the car ends its travel.
        state (CarState): The current state of the car.
    """

    def setup(self, spawn_points):
        """
        Set up the initial state of the car.

        Parameters:
            spawn_points (list): List of possible spawn points for the car.
        """
        # This ensures the car won't take a u-turn.
        directions = {
            "N": ["N", "W", "E"],
            "S": ["S", "W", "E"],
            "E": ["E", "N", "S"],
            "W": ["W", "N", "S"]
        }

        pos = random.choice(spawn_points)
        self.model.car_positions.append(pos)
        self.id = self.model.auto_id
        self.model.auto_id += 1

        if pos[0] == 0:  # Spawns south
            self.from_dir = "N"
        elif pos[0] == self.model.p.MAP_SIZE - 1:  # Spawns north
            self.from_dir = "S"
        elif pos[1] == 0:  # Spawns west
            self.from_dir = "E"
        elif pos[1] == self.model.p.MAP_SIZE - 1:  # Spawns east
            self.from_dir = "W"

        # Assign to the car the direction of the lane where it has to end.
        self.to_dir = random.choice(directions[self.from_dir])

        # Assign the initial state to the car
        self.state = CarState.HAS_NOT_TOUCHED_INTERSECTION

def generate_tiles(MAP_SIZE: int, LANES: int) -> tuple:
    """
    Generate a matrix of tiles representing a map with specified size and lanes.

    Parameters:
        MAP_SIZE (int): The size of the map.
        LANES (int): The number of lanes heading on each direction on the map.

    Returns:
        tuple: A tuple containing:
            - List of lists: Matrix of tiles representing the map.
            - List of tuples: Array of ordered pairs representing spawn points.
    """
    tiles = []
    spawn_points = []

    # Variables to simplify math notation later on
    laneMin = (MAP_SIZE - LANES * 2) / 2
    laneMax = laneMin + LANES * 2
    laneMid = laneMin + LANES
    
    for i in range(MAP_SIZE):
        tiles.append([])
        for j in range(MAP_SIZE):
            if laneMin <= i < laneMax and laneMin <= j < laneMax:
                tiles[i].append(TypesTiles.INTERSECTION)
            elif j == 0 and laneMin <= i < laneMid or j == MAP_SIZE - 1 and laneMid <= i < laneMax or i == 0 and laneMid <= j < laneMax or i == MAP_SIZE - 1 and laneMin <= j < laneMid:
                spawn_points.append((i, j))
                tiles[i].append(TypesTiles.SPAWN)
            elif j == laneMin - 1 and laneMin <= i < laneMid or j == laneMax and laneMid <= i < laneMax or i == laneMin - 1 and laneMid <= j < laneMax or i == laneMax and laneMin <= j < laneMid:
                tiles[i].append(TypesTiles.TRAFFIC_LIGHT)
            elif (j == laneMin - 3 or j == laneMin - 5) and laneMin <= i < laneMid or (j == laneMax + 2 or j == laneMax + 4) and laneMid <= i < laneMax or (i == laneMin - 3 or i == laneMin - 5) and laneMid <= j < laneMax or (i == laneMax + 2 or i == laneMax + 4) and laneMin <= j < laneMid:
                tiles[i].append(TypesTiles.SWITCH_LANE)
            elif 0 <= i < laneMin and laneMin <= j < laneMid or laneMax <= i < MAP_SIZE and laneMid <= j < laneMax or 0 <= j < laneMin and laneMid <= i < laneMax or laneMax <= j < MAP_SIZE and laneMin <= i < laneMid:
                tiles[i].append(TypesTiles.REVERSED_STREET)
            elif laneMin <= i < laneMax or laneMin <= j < laneMax:
                tiles[i].append(TypesTiles.STREET)
            else:
                tiles[i].append(TypesTiles.CITY)

    return tiles, spawn_points


class MapModel(ap.Model):
    def setup(self):
        # Create a grid for the simulation
        self.grid = ap.Grid(self, tuple([self.p.MAP_SIZE] * 2), track_empty=True)

        # Initialize an auto-incrementing ID for cars
        self.auto_id = 0

        # Generate map tiles and spawn points
        self.tiles, spawn_points = generate_tiles(self.p.MAP_SIZE, self.p.LANES)

        """
        DEBUG CODE
        print tiles
        print(np.shape(self.tiles))
        for i in range(self.p.MAP_SIZE-1, -1, -1):
            for j in range(self.p.MAP_SIZE):
                print(int(self.tiles[i][j]) , end=" ")
            print()
        """

        # List to keep track of car positions
        self.car_positions = []

        # Initialize car agents directly without using an intermediate variable
        self.grid.add_agents(
            ap.AgentList(self, self.p.CARS, Car, spawn_points=spawn_points),
            self.car_positions
        )

        # Initialize variables for the traffic
        self.traffic_lights = [TrafficLightState.RED] * 4
        self.traffic_lights[0] = TrafficLightState.GREEN
        self.current_light = 0
        self.light_timer = 0

        # NOT IMPLEMENTED - finished turning logic is missing
        # self.turning = False

    def step(self):
        print(self.t)

        # Add traffic lights to payload
        payload = f'{{"t":{self.t}, "traffic_lights": [{", ".join(str(light.value) for light in self.traffic_lights)}], "cars": ['

        # Update the traffic lights colors
        self.update_traffic_lights()

        for car in self.grid.agents.to_list():
            # DEBUG
            self.print_car_info(car)

            # Add car id, x and y to payload
            payload += '{"id": ' + str(car.id) + ', "x": ' + str(self.grid.positions[car][1]) + ', "y": ' + str(self.grid.positions[car][0]) + '},'

            if car.state == CarState.HAS_NOT_TOUCHED_INTERSECTION:
                self.move_to_intersection(car)

            elif car.state == CarState.STOP_LIGHT:
                self.wait_at_stop_light(car)

            elif car.state == CarState.HAS_TOUCHED_INTERSECTION:
                self.cross_intersection(car)

            elif car.state == CarState.TO_STREET:
                self.finish_travel(car)

        payload = payload.rstrip(',') + ']}'

        # Increase iteration.
        self.t += 1

        return payload

    ### ABSTRACTION LOWER LAYERS
    def update_traffic_lights(self):
        """
        Update the traffic lights colors based on the light timer.
        """
        if self.light_timer % 14 == 0:
            # Turn the green light into yellow
            self.traffic_lights[self.current_light] = TrafficLightState.YELLOW

        if self.light_timer % 20 == 0:
            # Turn the yellow into red and make the next light green
            self.traffic_lights[self.current_light] = TrafficLightState.RED
            self.current_light = (self.current_light + 1) % 4  # Increment it and keep it in range [0-3]
            self.traffic_lights[self.current_light] = TrafficLightState.GREEN

        self.light_timer = (self.light_timer + 1) % 20  # Increment it and keep it in range [0-19]

    def print_car_info(self, car):
        print(car.from_dir)
        print(car.to_dir)
        print(self.grid.positions[car])
        print(car.state)
        print()

    def get_car_desired_direction(self, car):
        x = dirs[car.from_dir][0] + dirs[car.to_dir][0]
        y = dirs[car.from_dir][1] + dirs[car.to_dir][1]
        
        if x != 0:
            x //= abs(x)
        if y != 0:
            y //= abs(y)
        
        return (x, y)

    def move_to_intersection(self, car):

        [car_y, car_x] = self.grid.positions[car]

        desired_dir = self.get_car_desired_direction(car)
        desired_pos = (car_y + desired_dir[0], car_x + desired_dir[1])
        from_dir = dirs[car.from_dir]

        # Check if the car is in a swith position
        if self.tiles[car_y][car_x] == TypesTiles.SWITCH_LANE:

            # Check if there is a car in the desired position
            if len(self.grid.agents[desired_pos].to_list()) > 0:
                return

            # Check if the desired position is a street
            if self.tiles[desired_pos[0]][desired_pos[1]] == TypesTiles.STREET:
                self.grid.move_to(car, desired_pos)
            else:
                # If it wants to invade an oncoming lane or a city block continue straight
                if len(self.grid.agents[(car_y + from_dir[0], car_x + from_dir[1])].to_list()) > 0:
                    return

                self.grid.move_by(car, from_dir)
            return

        # Check if cell in front has a car
        desired_pos = (car_y + from_dir[0], car_x + from_dir[1])

        if len(self.grid.agents[desired_pos].to_list()) == 0:
            self.grid.move_to(car, desired_pos)

            # If the car is in a stop-light
            if self.tiles[car_y][car_x] == TypesTiles.TRAFFIC_LIGHT:
                car.state = CarState.STOP_LIGHT
                # Announce a car is turning, so other cars stop
                # self.turning = True

    def wait_at_stop_light(self, car):
        # Check if the traffic light is green
        if self.traffic_lights[traffic_order[car.from_dir]] != TrafficLightState.GREEN:
            return

        from_dir = dirs[car.from_dir]
        position = self.grid.positions[car]
        # Check if cell in front has a car
        desired_pos = (position[0] + from_dir[0], position[1] + from_dir[1])

        if len(self.grid.agents[desired_pos].to_list()) > 0:
            return
        
        # Check if there is a car turning
        # if self.turning:
        #     return

        self.grid.move_by(car, from_dir)
        car.state = CarState.HAS_TOUCHED_INTERSECTION

    def cross_intersection(self, car):
        position = self.grid.positions[car]
        desired_dir = self.get_car_desired_direction(car)
        desired_pos = (position[0] + desired_dir[0], position[1] + desired_dir[1])

        if self.tiles[desired_pos[0]][desired_pos[1]] != TypesTiles.INTERSECTION:
            car.state = CarState.TO_STREET
            return

        if len(self.grid.agents[desired_pos].to_list()) != 0:
            return
        self.grid.move_by(car, desired_dir)

    def finish_travel(self, car):
        position = self.grid.positions[car]

        desired_pos = (position[0] + dirs[car.to_dir][0], position[1] + dirs[car.to_dir][1])
        # Check if new position is in the grid
        if not (0 <= desired_pos[0] < self.p.MAP_SIZE and 0 <= desired_pos[1] < self.p.MAP_SIZE):
            # Remove car from grid
            self.grid.remove_agents(car)
            return

        if len(self.grid.agents[desired_pos].to_list()) != 0:
            return
        self.grid.move_by(car, dirs[car.to_dir])



async def run_simulation(websocket, path):
    print ("New connection")

    map_size = await websocket.recv()
    map_size = int(map_size)
    print("map_size: ", map_size)

    lanes = await websocket.recv()
    lanes = int(lanes)
    print("lanes: ", lanes)

    cars = await websocket.recv()
    cars = int(cars)
    print("cars: ", cars)

    model = MapModel({
        "MAP_SIZE": map_size,
        "LANES": lanes,
        "CARS": cars,
        "WEBSOCKET": websocket,
    })

    model.setup()

    while len(model.grid.agents.to_list()) != 0:
        await websocket.send(model.step())
        await websocket.recv()

    await websocket.send("Done")

    pass

async def main():
    async with websockets.serve(run_simulation, "localhost", 8765):
        print("Server started")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
