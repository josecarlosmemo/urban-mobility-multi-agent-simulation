import asyncio
import websockets
import agentpy as ap
from enum import IntEnum
import random


class TypesTiles(IntEnum):
    CITY = 0
    STREET = 1
    INTERSECTION = 2
    TRAFFIC_LIGHT = 3
    CAR = 4


# MAP_SIZE int
# MAP_Lanes
# CARS
posible_directions =  {
            "N": (0, 1),
            "S": (0, -1),
            "E": (1, 0),
            "W": (-1, 0),
            "NE": (1, 1),
            "NW": (-1, 1),
            "SE": (1, -1),
            "SW": (-1, -1),}



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

        spawn_points = spawn_points * (self.p.CARS // len(spawn_points) + 1)
        random.shuffle(spawn_points)


        car_agents = ap.AgentList(self, self.p.CARS)

        opposites = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E",
        }

        # Assign initial positions to cars
        for spawn_pos, car in zip(spawn_points, car_agents):
            car.pos = spawn_pos

            to_dir = ""
            from_dir = ""

            if car.pos[0] == 0: # Spawns south
                to_dir = "S"
                from_dir = "S"
            elif car.pos[0] == self.p.MAP_SIZE - 1: # Spawns north
                to_dir = "N"
                from_dir = "N"
            elif car.pos[1] == 0: # Spawns west
                to_dir = "W"
                from_dir = "W"
            elif car.pos[1] == self.p.MAP_SIZE - 1: # Spawns east
                to_dir = "E"
                from_dir = "E"

            while to_dir == from_dir:
                to_dir = random.choice(list(opposites.keys()))



            car.to_dir = to_dir
            car.from_dir = opposites[from_dir]





        city_agents.type = TypesTiles.CITY
        street_agents.type = TypesTiles.STREET
        intersection_agents.type = TypesTiles.INTERSECTION
        traffic_lights_agents.type = TypesTiles.TRAFFIC_LIGHT
        car_agents.type = TypesTiles.CAR


        self.grid.add_agents(city_agents, city_pos)
        self.grid.add_agents(street_agents, street_pos)
        self.grid.add_agents(intersection_agents, intersection_pos)
        self.grid.add_agents(traffic_lights_agents, traffic_lights_pos)
        self.grid.add_agents(car_agents, spawn_points[0: len(car_agents)])

    def step(self):

        # Getting List of Currently Active Agents
        active_agents = self.grid.agents.to_list()

        cars = active_agents.select(active_agents.type == TypesTiles.CAR)

        for car in cars:
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



if __name__ == "__main__":
    model = MapModel({
        "MAP_SIZE": 18,
        "LANES": 3,
        "CARS": 200,
    })
    model.run(1)
