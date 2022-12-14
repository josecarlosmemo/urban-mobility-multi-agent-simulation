<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
![Languages][languages-shield]

<br />

<div align="center">
  <a href="https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation">
    <img src="https://upload.wikimedia.org/wikipedia/commons/4/47/Logo_del_ITESM.svg" alt="Logo" width="80" height="80">
  </a>
<h3 align="center">Urban Mobility in México</h3>
  <p align="center">
        In this challenge, we propose a solution to the problem of urban
        mobility in Mexico through a multi-agent system that simulates
        traffic and reduces vehicular congestion.
    <br />
                <a href="https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation"><strong>Explore the docs »</strong></a>
            <br />
    <br />
        <a href="https://youtu.be/WCIW4GSYRKo">View Demo</a>
    ·
                <a href="https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation/issues">Report Bug</a>
    ·
    <a href="https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation/issues">Request Feature</a>
          </p>
</div>
<details>
  <summary>Table of Contents</summary>
  <ol>
   <li>
   <a href="#how-the-simulation-works">How the Simulation Works</a>
   <ul>
   <li><a href="#agent-protocol">Agent Protocol</a></li>
   </ul>
   </li>
   <li><a href="#running-the-server-and-the-simulation">Running the Server and the Simulation</a></li>

  </ol>
</details>

## Project Demo

[![demo](./images/demo.gif)](https://youtu.be/WCIW4GSYRKo)



For a complete demo of the project, please visit the following link or click on the image above:

[https://youtu.be/WCIW4GSYRKo](https://youtu.be/WCIW4GSYRKo)

The problem of urban mobility in Mexico is a pressing issue that needs
to be addressed. The indiscriminate use of cars has led to negative
economic, environmental, and social effects, such as smog, accidents,
diseases, and traffic congestion.

Our solution implements one or more of the following strategies:

- Control and assignment of available parking spaces in a city area to
    avoid cars driving around looking for parking.
- Sharing of vehicles to increase occupancy and reduce the number of
    cars on the streets.
- Use of the least congested routes to reduce consumption and
    pollution.
- Coordination of traffic lights to reduce congestion at
    intersections.

We believe that our solution can contribute to the improvement of
mobility in Mexican cities and enhance the economic activities and
quality of life of millions of people.

## How the Simulation Works

The simulation is based on a multi-agent system that represents the
traffic in a city. Each agent is a car that has its own behavior and
decision-making capabilities. The agents interact with each other and
with the environment, following the rules and strategies implemented in
the simulation.

The simulation is performed using the Unity game engine, which allows
for the visual representation of the traffic and the performance of the
agents. The communication between the simulation and the server is
established using WebSockets, which allows for real-time data transfer
and synchronization.

### Agent Protocol

The movement of the agents (cars) in the simulation is determined by
their behavior and the rules of the road. Each agent has a set of rules
that govern its actions, such as maintaining a safe distance from other
cars, obeying traffic lights.

The agents in the simulation are finite deterministic automata that have
4 states and follow the rules outlined below. Additionally, the agents
only move to unoccupied squares, otherwise they wait.

#### Initial state

If the agent is on a lane-change square and needs to change lanes, it
does so. Otherwise, it moves forward. If the square it arrives at is a
traffic light, the agent enters the traffic light state.

#### Traffic light state

If the traffic light is green, the agent advances and changes to the
intersection state.

#### Intersection state

The agent sums the vectors of the direction of the street it is coming
from and the street it is going to, and normalizes the result. If the
adjacent square in that direction is an intersection, the agent moves to
it. Otherwise, the agent moves in the direction of the destination
street and enters the final state.

#### Final state

If the square in front is within the range of the map, the agent moves
to it. Otherwise, we remove the agent from the simulation.

<p align="right">(<a href="#top">back to top</a>)</p>

## Running the Server and the Simulation

To run the server and the simulation, you will need to have Python 3
installed on your computer. You will also need to have make installed in
order to run the provided Makefile. Follow these steps:

1. Clone the repository to your local machine:

``` sh
git clone https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation.git
```

2. Navigate to the server directory where the Makefile is located:
    - Run the following command to create a virtual environment for
        the project:

``` sh
make venv
```

This will create a venv directory and install the required dependencies
into it.

3. Activate the virtual environment by running the following command:

``` sh
source venv/bin/activate
```

4. Install the development dependencies by running the following
    command:

``` sh
make dep
```

5. Start the server by running the following command:

``` sh
make run
```

This will start the server and it will be ready to accept connections
from the client.

6. Open the Unity project in the `client` directory.

    - In the Unity editor, click on the “Play” button to start the
        simulation.

The server and the simulation should now be running and communicating
with each other using WebSockets.

### Built With

<div>
<img width="40px" height="40px" src="https://skillicons.dev/icons?i=py"/>
<img width="40px" height="40px" src="https://skillicons.dev/icons?i=unity"/>
<img width="40px" height="40px" src="https://skillicons.dev/icons?i=cpp"/>
</div>

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/josecarlosmemo/urban-mobility-multi-agent-simulation.svg?style=for-the-badge
[contributors-url]: https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/josecarlosmemo/urban-mobility-multi-agent-simulation.svg?style=for-the-badge
[forks-url]: https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation/network/members
[stars-shield]: https://img.shields.io/github/stars/josecarlosmemo/urban-mobility-multi-agent-simulation.svg?style=for-the-badge
[stars-url]: https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation/stargazers
[issues-shield]: https://img.shields.io/github/issues/josecarlosmemo/urban-mobility-multi-agent-simulation.svg?style=for-the-badge
[issues-url]: https://github.com/josecarlosmemo/urban-mobility-multi-agent-simulation/issues
[languages-shield]: https://img.shields.io/github/languages/count/josecarlosmemo/urban-mobility-multi-agent-simulation.svg?style=for-the-badge
