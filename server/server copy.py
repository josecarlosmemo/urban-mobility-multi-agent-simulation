import asyncio
import websockets
import agentpy as ap
from enum import IntEnum
import random
import numpy as np


class TypesTiles(IntEnum):
    CITY = 0
    STREET = 1
    INTERSECTION = 2
    TRAFFIC_LIGHT = 3
    CAR = 4
    SPAWN = 5


class CarState(IntEnum):
    HAS_TOUCHED_INTERSECTION = 0
    HAS_NOT_TOUCHED_INTERSECTION = 1
    STOP_LIGHT = 2

# MAP_SIZE int
# MAP_Lanes
# CARS
dirs =  {
            "N": (1, 0),
            "S": (-1, 0),
            "E": (0, 1),
            "W": (0, -1)
        }


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


        car_agents = ap.AgentList(self, self.p.CARS, Car, spawn_points=spawn_points)

        car_agents.type = TypesTiles.CAR
        car_agents.state = CarState.HAS_NOT_TOUCHED_INTERSECTION

        self.grid.add_agents(car_agents, self.car_positions)

        self.turning = False

    def step(self):

        active_agents = self.grid.agents.to_list()

        cars = active_agents.select(active_agents.type == TypesTiles.CAR)

        for car in cars:
            print(car.from_dir)
            print(car.to_dir)
            print(self.grid.positions[car])
            print(car.state)
            print()

            # MY PROPOSAL ----------------------------------------------------    
            if car.state == CarState.HAS_NOT_TOUCHED_INTERSECTION:
                # Check if cell in front has a car
                desired_pos = (self.grid.positions[car][0] + dirs[car.from_dir][0], self.grid.positions[car][1] + dirs[car.from_dir][1])
                if not (0 <= desired_pos[0] < self.p.MAP_SIZE and 0 <= desired_pos[1] < self.p.MAP_SIZE):
                    continue

                if len(self.grid.agents[desired_pos].to_list()) == 0:
                    self.grid.move_to(car, desired_pos)

                    # If the car is in a stop-light
                    if self.tiles[self.grid.positions[car][0]][self.grid.positions[car][1]] == TypesTiles.TRAFFIC_LIGHT:
                        car.state = CarState.STOP_LIGHT
                        # Announce a car is turning, so other cars stop
                        # self.turning = True

            elif car.state == CarState.STOP_LIGHT:
                # Check if cell in front has a car
                desired_pos = (self.grid.positions[car][0] + dirs[car.from_dir][0], self.grid.positions[car][1] + dirs[car.from_dir][1])
                if not (0 <= desired_pos[0] < self.p.MAP_SIZE and 0 <= desired_pos[1] < self.p.MAP_SIZE):
                    continue

                if len(self.grid.agents[desired_pos].to_list()) != 0:
                    continue
                
                # Check if there is a car turning
                if self.turning:
                    continue

                self.grid.move_by(car, dirs[car.from_dir])
                car.state = CarState.HAS_TOUCHED_INTERSECTION

            else:
                x = dirs[car.from_dir][0] + dirs[car.to_dir][0]
                y = dirs[car.from_dir][1] + dirs[car.to_dir][1]
                
                if abs(x) == 2:
                    x = x // 2
                elif abs(y) == 2:
                    y = y // 2
                
                desired_dir = (x, y)
                desired_pos = (self.grid.positions[car][0] + desired_dir[0], self.grid.positions[car][1] + desired_dir[1])

                print("desired pos: ", desired_pos)

                # Check if new position is in the grid
                if not (0 <= desired_pos[0] < self.p.MAP_SIZE and 0 <= desired_pos[1] < self.p.MAP_SIZE):
                    continue

                if self.tiles[desired_pos[0]][desired_pos[1]] == TypesTiles.INTERSECTION:
                    self.grid.move_by(car, desired_dir)
                else:
                    self.grid.move_by(car, dirs[car.to_dir])

        # Send Location

        # Receive Location

        pass


#async def echo(websocket):
#    async for message in websocket:
#        print(message)
#        await websocket.send(message)


#async def main():
#    async with websockets.serve(echo, "localhost", 8765):
#        await asyncio.Future()  # run forever


#asyncio.run(main())


def animation_plot(model, ax):
    attr_grid = model.grid.attr_grid('type')
    color_dict = {TypesTiles.CITY: 'black', TypesTiles.STREET: 'white', TypesTiles.INTERSECTION: 'yellow', TypesTiles.TRAFFIC_LIGHT: 'red', TypesTiles.CAR: 'blue'}


    ax.set_title(f"Robot Cleaning Simulation", loc="left", fontdict={'family': 'Futura', 'color': 'black', 'size': 15})
    ax.set_xlabel(f"Step: {model.t}")
    ap.gridplot(attr_grid, ax=ax, color_dict=color_dict, convert=True)



if __name__ == "__main__":
    model = MapModel({
        "MAP_SIZE": 18,
        "LANES": 3,
        "CARS": 1,
    })
    model.run(20)


