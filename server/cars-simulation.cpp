// Author: Oscar Valdés
// Last modified: Novemeber 19th, 2022
// Description: This program generates a car intersection model

#include <iostream>

class Car {
    public:
    int x, y;
    char spawn, direction, state;
    Car(int x, int y, char spawn, char direction) {
        this->x = x;
        this->y = y;
        this->spawn = spawn;
        this->direction = direction;
        this->state = 'A';
    }
};

void printGrid(int ** grid, int size, Car car) {
    for (int i = size - 1; i >= 0; i--) {
        for (int j = 0; j < size; j++) {
            if (j == car.x && i == car.y) {
                std::cout << "x" << " ";
            } else {
                std::cout << grid[i][j] << " ";
            }

        }
        std::cout << std::endl;
    }
}

int main() {
    int size, lanes;
    std::cout << "Enter the size of the simulation: ";
    std::cin >> size;

    std::cout << "Enter the number of lanes: ";
    std::cin >> lanes;

    int ** grid = new int*[size];
    for (int i = 0; i < size; i++) {
        grid[i] = new int[size];
        int laneMin = (size - lanes * 2) / 2;
        int laneMid = laneMin + lanes;
        int laneMax = laneMid + lanes;
        for (int j = 0; j < size; j++)
        {
            // Intersection
            if (laneMin <= i && i < laneMax && laneMin <= j && j < laneMax) {
                grid[i][j] = 0;
            } else if (laneMin <= i && i < laneMax || laneMin <= j && j < laneMax) {
                // Street
                grid[i][j] = 1;
            } else {
                // City
                grid[i][j] = 2;
            }

            // Spawn points
            if (j == 0 && laneMin <= i && i < laneMid ||
                j == size - 1 && laneMid <= i && i < laneMax ||
                i == 0 && laneMid <= j && j < laneMax ||
                i == size - 1 && laneMin <= j && j < laneMid) {
                grid[i][j] = 3;
            }

            // Traffic lights
            if (j == laneMin - 1 && laneMin <= i && i < laneMid ||
                j == laneMax && laneMid <= i && i < laneMax ||
                i == laneMin - 1 && laneMid <= j && j < laneMax ||
                i == laneMax && laneMin <= j && j < laneMid) {
                grid[i][j] = 4;
            }
        }
    }
    
    Car car(11, 0, 'N', 'W');

    for (int i = 0; i < 20; i++)
    {
        printGrid(grid, size, car);

        if (car.state == 'A') {
            if (grid[car.y][car.x] != 0) {
                car.y += 1;
            } else {
                car.state = 'B';
            }
        } else {
            if (grid[car.x - 1][car.y + 1] != 2) {
                car.x -= 1;
                car.y += 1;
            } else {
                car.x -= 1;
            }
        }

        
        

        std::cout << "\n\n\n\n\n" << std::endl;
    }
    
    

    return 0;
}