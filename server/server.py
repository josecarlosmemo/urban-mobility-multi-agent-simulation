import asyncio
import json
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

# MAP_SIZE int
# MAP_Lanes
# CARS
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

class TrafficDirection(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


class Car(ap.Agent):
     def setup(self, spawn_points):

        opposites = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        }


        pos = random.choice(spawn_points)
        self.model.car_positions.append(pos)
        self.id = self.model.auto_id
        self.model.auto_id += 1

        if pos[0] == 0:  # Spawns south
            self.to_dir = "S"
            self.from_dir = "S"
        elif pos[0] == self.model.p.MAP_SIZE - 1:  # Spawns north
            self.to_dir = "N"
            self.from_dir = "N"
        elif pos[1] == 0:  # Spawns west
            self.to_dir = "W"
            self.from_dir = "W"
        elif pos[1] == self.model.p.MAP_SIZE - 1:  # Spawns east
            self.to_dir = "E"
            self.from_dir = "E"

        while self.to_dir == self.from_dir:
            self.to_dir = random.choice(list(opposites.keys()))

        self.from_dir = opposites[self.from_dir]



class MapModel(ap.Model):
    def setup(self):
        self.grid = ap.Grid(self, tuple([self.p.MAP_SIZE] * 2), track_empty=True)

        laneMin = (self.p.MAP_SIZE - self.p.LANES * 2) / 2
        laneMax = laneMin + self.p.LANES * 2
        laneMid = laneMin + self.p.LANES

        spawn_points = []

        self.tiles = []
        self.auto_id = 0

        for i in range(self.p.MAP_SIZE):
            self.tiles.append([])
            for j in range(self.p.MAP_SIZE):
                if laneMin <= i < laneMax and laneMin <= j < laneMax:
                    self.tiles[i].append(TypesTiles.INTERSECTION)
                elif j == 0 and laneMin <= i < laneMid or j == self.p.MAP_SIZE - 1 and laneMid <= i < laneMax or i == 0 and laneMid <= j < laneMax or i == self.p.MAP_SIZE - 1 and laneMin <= j < laneMid:
                    spawn_points.append((i, j))
                    self.tiles[i].append(TypesTiles.SPAWN)
                elif j == laneMin - 1 and laneMin <= i < laneMid or j == laneMax and laneMid <= i < laneMax or i == laneMin - 1 and laneMid <= j < laneMax or i == laneMax and laneMin <= j < laneMid:
                    self.tiles[i].append(TypesTiles.TRAFFIC_LIGHT)
                elif (j == laneMin - 3 or j == laneMin - 5) and laneMin <= i < laneMid or (j == laneMax + 2 or j == laneMax + 4) and laneMid <= i < laneMax or (i == laneMin - 3 or i == laneMin - 5) and laneMid <= j < laneMax or (i == laneMax + 2 or i == laneMax + 4) and laneMin <= j < laneMid:
                    self.tiles[i].append(TypesTiles.SWITCH_LANE)
                elif 0 <= i < laneMin and laneMin <= j < laneMid or laneMax <= i < self.p.MAP_SIZE and laneMid <= j < laneMax or 0 <= j < laneMin and laneMid <= i < laneMax or laneMax <= j < self.p.MAP_SIZE and laneMin <= i < laneMid:
                    self.tiles[i].append(TypesTiles.REVERSED_STREET)
                elif laneMin <= i < laneMax or laneMin <= j < laneMax:
                    self.tiles[i].append(TypesTiles.STREET)
                else:
                    self.tiles[i].append(TypesTiles.CITY)

        # print tiles
        # print(np.shape(self.tiles))
        # for i in range(self.p.MAP_SIZE-1, -1, -1):
        #     for j in range(self.p.MAP_SIZE):
        #         print(int(self.tiles[i][j]) , end=" ")
        #     print()


        self.car_positions = []
        self.traffic_lights = []

        for i in range(4):
            self.traffic_lights.append(TrafficLightState.RED)
        
        self.traffic_lights[0] = TrafficLightState.GREEN
        self.current_light = 0
        self.light_timer = -1


        car_agents = ap.AgentList(self, self.p.CARS, Car, spawn_points=spawn_points)

        car_agents.type = TypesTiles.CAR
        car_agents.state = CarState.HAS_NOT_TOUCHED_INTERSECTION

        self.grid.add_agents(car_agents, self.car_positions)

        self.turning = False

    def step(self):
        print(self.t)
        
        active_agents = self.grid.agents.to_list()

        cars = active_agents.select(active_agents.type == TypesTiles.CAR)
        
        # Add traffic lights to payload
        payload = '{"t":' + str(self.t) + ', "traffic_lights": ['+ str(self.traffic_lights[0].value) + ', ' + str(self.traffic_lights[1].value) + ', ' + str(self.traffic_lights[2].value) + ', ' + str(self.traffic_lights[3].value) + '], "cars": ['

        self.light_timer += 1
        self.light_timer %= 20

        if self.light_timer % 14 == 0:
            for i in range(4):
                if self.traffic_lights[i] == TrafficLightState.GREEN:
                    self.traffic_lights[i] = TrafficLightState.YELLOW

        if self.light_timer % 20 == 0:
            self.current_light += 1
            self.current_light %= 4
            for i in range(4):
                if i == self.current_light:
                    self.traffic_lights[i] = TrafficLightState.GREEN
                else:
                    self.traffic_lights[i] = TrafficLightState.RED


        for car in cars:
            print(car.from_dir)
            print(car.to_dir)
            print(self.grid.positions[car])
            print(car.state)
            print()

            # Add car id, x and y to payload

            payload += '{"id": ' + str(car.id) + ', "x": ' + str(self.grid.positions[car][1]) + ', "y": ' + str(self.grid.positions[car][0]) + '},'


            if car.state == CarState.HAS_NOT_TOUCHED_INTERSECTION:

                x = dirs[car.from_dir][0] + dirs[car.to_dir][0]
                y = dirs[car.from_dir][1] + dirs[car.to_dir][1]
            
                if abs(x) == 2:
                    x = x // 2
                elif abs(y) == 2:
                    y = y // 2
                
                desired_dir = (x, y)
                desired_pos = (self.grid.positions[car][0] + desired_dir[0], self.grid.positions[car][1] + desired_dir[1])

                # Check if the car is in a swith position
                if self.tiles[self.grid.positions[car][0]][self.grid.positions[car][1]] == TypesTiles.SWITCH_LANE:

                    # Check if there is a car in the desired position
                    if len(self.grid.agents[desired_pos].to_list()) != 0:
                        continue

                    # Check if the desired position is a street
                    if self.tiles[desired_pos[0]][desired_pos[1]] == TypesTiles.STREET:
                        self.grid.move_to(car, desired_pos)
                    else:
                        if len(self.grid.agents[(self.grid.positions[car][0] + dirs[car.from_dir][0], self.grid.positions[car][1] + dirs[car.from_dir][1])].to_list()) != 0:
                            continue

                        self.grid.move_by(car, dirs[car.from_dir])
                    continue

                # The current tile is not a switch position

                # Check if cell in front has a car
                desired_pos = (self.grid.positions[car][0] + dirs[car.from_dir][0], self.grid.positions[car][1] + dirs[car.from_dir][1])

                if len(self.grid.agents[desired_pos].to_list()) == 0:
                    self.grid.move_to(car, desired_pos)

                    # If the car is in a stop-light
                    if self.tiles[self.grid.positions[car][0]][self.grid.positions[car][1]] == TypesTiles.TRAFFIC_LIGHT:
                        car.state = CarState.STOP_LIGHT
                        # Announce a car is turning, so other cars stop
                        # self.turning = True

            elif car.state == CarState.STOP_LIGHT:
                # Check if the traffic light is green
                if self.traffic_lights[traffic_order[car.from_dir]] != TrafficLightState.GREEN:
                    continue

                # Check if cell in front has a car
                desired_pos = (self.grid.positions[car][0] + dirs[car.from_dir][0], self.grid.positions[car][1] + dirs[car.from_dir][1])

                if len(self.grid.agents[desired_pos].to_list()) != 0:
                    continue
                
                # Check if there is a car turning
                if self.turning:
                    continue

                self.grid.move_by(car, dirs[car.from_dir])
                car.state = CarState.HAS_TOUCHED_INTERSECTION

            elif car.state == CarState.HAS_TOUCHED_INTERSECTION:
                x = dirs[car.from_dir][0] + dirs[car.to_dir][0]
                y = dirs[car.from_dir][1] + dirs[car.to_dir][1]
                
                if abs(x) == 2:
                    x = x // 2
                elif abs(y) == 2:
                    y = y // 2
                
                desired_dir = (x, y)
                desired_pos = (self.grid.positions[car][0] + desired_dir[0], self.grid.positions[car][1] + desired_dir[1])

                if not self.tiles[desired_pos[0]][desired_pos[1]] == TypesTiles.INTERSECTION:
                    # Check if there is a car in the desired position
                    car.state = CarState.TO_STREET
                    continue

                if len(self.grid.agents[desired_pos].to_list()) != 0:
                    continue
                self.grid.move_by(car, desired_dir)

            else:
                desired_pos = (self.grid.positions[car][0] + dirs[car.to_dir][0], self.grid.positions[car][1] + dirs[car.to_dir][1])
                # Check if new position is in the grid
                if not (0 <= desired_pos[0] < self.p.MAP_SIZE and 0 <= desired_pos[1] < self.p.MAP_SIZE):
                    # Remove car from grid
                    print("Pos: ", desired_pos)
                    self.grid.remove_agents(car)
                    continue

                if len(self.grid.agents[desired_pos].to_list()) != 0:
                    print("Car in front")
                    continue
                self.grid.move_by(car, dirs[car.to_dir])


        # Send Location

        # Receive Location

        payload = payload[:-1]
        payload += ']}'

        self.t += 1

        return payload



#async def echo(websocket):
#    async for message in websocket:
#        print(message)
#        await websocket.send(message)


#async def main():
#    async with websockets.serve(echo, "localhost", 8765):
#        await asyncio.Future()  # run forever


#asyncio.run(main())


# def animation_plot(model, ax):
#     attr_grid = model.grid.attr_grid('type')
#     color_dict = {TypesTiles.CITY: 'black', TypesTiles.STREET: 'white', TypesTiles.INTERSECTION: 'yellow', TypesTiles.TRAFFIC_LIGHT: 'red', TypesTiles.CAR: 'blue'}


#     ax.set_title(f"Robot Cleaning Simulation", loc="left", fontdict={'family': 'Futura', 'color': 'black', 'size': 15})
#     ax.set_xlabel(f"Step: {model.t}")
#     ap.gridplot(attr_grid, ax=ax, color_dict=color_dict, convert=True)


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

    # await websocket.send("Start")

    while len(model.grid.agents.to_list()) != 0:
        await websocket.send(model.step())
        await websocket.recv()



        # await asyncio.sleep(1)

    # Send first model step and wait for response

    # while True and len(model.grid.agents.to_list()) != 0:
    #     await websocket.send(model.step())
    #     await asyncio.sleep(0.1)
    #     await websocket.recv()
    







    await websocket.send("Done")

   

    pass


async def main():
    async with websockets.serve(run_simulation, "localhost", 8765):
        print("Server started")
        await asyncio.Future()  # run forever



if __name__ == "__main__":
    asyncio.run(main())