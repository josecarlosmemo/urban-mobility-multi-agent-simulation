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


class CarState(IntEnum):
    HAS_TOUCHED_INTERSECTION = 0
    HAS_NOT_TOUCHED_INTERSECTION = 1




# MAP_SIZE int
# MAP_Lanes
# CARS
posible_directions =  {
            "N": (1, 0),
            "S": (-1, 0),
            "E": (0, 1),
            "W": (0, -1),
           }


class Car(ap.Agent):
    def setup(self, spawn_points):

        opposites = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E",
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

        street_pos = []
        intersection_pos = []
        city_pos = []
        spawn_points = []
        traffic_lights_pos = []

        for i in range(self.p.MAP_SIZE):
            for j in range(self.p.MAP_SIZE):
                if laneMin <= i < laneMax and laneMin <= j < laneMax:
                    intersection_pos.append((i, j))
                elif j == 0 and laneMin <= i < laneMid or j == self.p.MAP_SIZE - 1 and laneMid <= i < laneMax or i == 0 and laneMid <= j < laneMax or i == self.p.MAP_SIZE - 1 and laneMin <= j < laneMid:
                    spawn_points.append((i, j))
                elif j == laneMin - 1 and laneMin <= i < laneMid or j == laneMax and laneMid <= i < laneMax or i == laneMin - 1 and laneMid <= j < laneMax or i == laneMax and laneMin <= j < laneMid:
                    traffic_lights_pos.append((i, j))
                elif laneMin <= i < laneMax or laneMin <= j < laneMax:
                    street_pos.append((i, j))
                else:
                    city_pos.append((i, j))

        city_agents = ap.AgentList(self, len(city_pos))
        street_agents = ap.AgentList(self, len(street_pos))
        intersection_agents = ap.AgentList(self, len(intersection_pos))
        traffic_lights_agents = ap.AgentList(self, len(traffic_lights_pos))

        #spawn_points = spawn_points * (self.p.CARS // len(spawn_points) + 1)
        #random.shuffle(spawn_points)


        self.car_positions = []


        car_agents = ap.AgentList(self, self.p.CARS, Car, spawn_points=spawn_points)




        city_agents.type = TypesTiles.CITY
        street_agents.type = TypesTiles.STREET
        intersection_agents.type = TypesTiles.INTERSECTION
        traffic_lights_agents.type = TypesTiles.TRAFFIC_LIGHT
        car_agents.type = TypesTiles.CAR
        car_agents.state = CarState.HAS_NOT_TOUCHED_INTERSECTION


        self.grid.add_agents(city_agents, city_pos)
        self.grid.add_agents(street_agents, street_pos)
        self.grid.add_agents(intersection_agents, intersection_pos)
        self.grid.add_agents(traffic_lights_agents, traffic_lights_pos)
        self.grid.add_agents(car_agents, self.car_positions)

    def step(self):

        active_agents = self.grid.agents.to_list()

        cars = active_agents.select(active_agents.type == TypesTiles.CAR)


        for car in cars:
            print(car.from_dir)
            print(car.to_dir)
            print(self.grid.positions[car])


            if car.state == CarState.HAS_NOT_TOUCHED_INTERSECTION:

                #print(self.grid.positions[car])

                self.grid.move_by(car, posible_directions[car.from_dir])

                if len(self.grid.agents[self.grid.positions[car]].to_list().select(self.grid.agents[self.grid.positions[car]].type == TypesTiles.INTERSECTION)) == 1:
                    car.state = CarState.HAS_TOUCHED_INTERSECTION
            else:
                dir = tuple(np.sum([posible_directions[car.from_dir], posible_directions[car.to_dir]], axis=0))
                new_pos = tuple(np.sum([self.grid.positions[car], dir], axis=0))

                # Check if new position is in the grid
                if not (0 <= new_pos[0] < self.p.MAP_SIZE and 0 <= new_pos[1] < self.p.MAP_SIZE):
                    continue



                if len(self.grid.agents[new_pos].to_list().select(self.grid.agents[new_pos].type == TypesTiles.INTERSECTION)) == 1:
                    self.grid.move_by(car, dir)
                else:
                    self.grid.move_by(car, posible_directions[car.to_dir])
















            pass
















        # Print the grid
        #for i in range(self.p.MAP_SIZE-1, -1, -1):
        #    for j in range(self.p.MAP_SIZE):
        #        print(self.grid.agents[(i,j)].type, end="")
        #    print()


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


