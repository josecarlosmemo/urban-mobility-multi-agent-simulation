using System;


// Traffic light enum
public enum TrafficLight
{
    Red = 0,
    Green=1,
    Yellow=2
}



[Serializable]
public class ListCars
{
    public int t;
    public Car[] cars;
    public TrafficLight[] traffic_lights;
}