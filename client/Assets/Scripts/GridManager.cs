using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;

public class GridManager : MonoBehaviour {
    [SerializeField] private int _mapSize = 18;
    [SerializeField] private int _nLanes = 3;
    [SerializeField] private float speed = 5f;

    [SerializeField] private Material _grassMaterial;
    [SerializeField] private Material _roadMaterial;
    

    [SerializeField] private Tile _tilePrefab;

    [SerializeField] private Transform _cam;

    [SerializeField] private GameObject _trafficLightPrefab;

    private Dictionary<Vector2, Tile> _tiles;

    private int _movedCarsCount = 0;
    // Private coordinate array
    private Vector2[] _trafficLightPositions;

    private List<Vector2> _endPositions;

    public List<GameObject> _trafficLights;

    void Start() {
        GenerateGrid();
    }

    void GenerateGrid() {
        _tiles = new Dictionary<Vector2, Tile>();
        _endPositions = new List<Vector2>();

        int laneMin = (_mapSize - _nLanes * 2) / 2;
        int laneMax = laneMin + _nLanes * 2;
        int laneMid = laneMin + _nLanes;

        for (int x = 0; x < _mapSize; x++) {
            for (int y = 0; y < _mapSize; y++) {
                var spawnedTile = Instantiate(_tilePrefab, new Vector3(x * 10, 0, y * 10), Quaternion.identity);
                spawnedTile.name = $"Tile {x} {y}";



                if (laneMin <= x && x < laneMax && laneMin <= y && y < laneMax) { // INTERSECTION
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (y == 0 && laneMid <= x && x < laneMax || x == 0 && laneMin <= y && y < laneMid || y == _mapSize - 1 && laneMin <= x && x < laneMid || x == _mapSize - 1 && laneMid <= y && y < laneMax) { // SPAWN
                    spawnedTile.name = "Spawn";
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (x == laneMin - 1 && laneMin <= y && y < laneMid || x == laneMax && laneMid <= y && y < laneMax || y == laneMin - 1 && laneMid <= x && x < laneMax || y == laneMax && laneMin <= x&& x < laneMid){ // self.tiles[i].append(TxpesTiles.TRAFFIC_LIGHT)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if ((x == laneMin - 3 || x == laneMin - 5) && laneMin <= y && y < laneMid || (x == laneMax + 2 || x == laneMax + 4) && laneMid <= y&& y < laneMax || (y == laneMin - 3 || y == laneMin - 5) && laneMid <= x && x < laneMax || (y == laneMax + 2 || y == laneMax + 4) && laneMin <= x && x < laneMid) { // SWITCH_LANE
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (y == 0 && laneMin <= x && x < laneMid || y == _mapSize - 1 && laneMid <= x && x < laneMax || x == 0 && laneMid <= y && y < laneMax || x == _mapSize - 1 && laneMin <= y && y< laneMid) { // END_STREET
                    spawnedTile.GetComponent<Renderer>().material.color = Color.red;
                    spawnedTile.name = "EndTile";
                    // add collider
                    BoxCollider bc = spawnedTile.gameObject.AddComponent<BoxCollider>();
                    bc.isTrigger = true;
                    bc.size = new Vector3(10, 10, 10);
                    // Add rigidbody with no gravity
                    Rigidbody rb = spawnedTile.gameObject.AddComponent<Rigidbody>();
                    rb.useGravity = false;


                } else if (0 <= x && x < laneMin && laneMin <= y && y < laneMid || laneMax <= x && x < _mapSize && laneMid <= y && y < laneMax || 0 <= y && y < laneMin && laneMid <= x && x < laneMax || laneMax <= y && y < _mapSize && laneMin <= x && x < laneMid) { // REVERSED_STREET
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (laneMin <= x && x < laneMax || laneMin <= y && y < laneMax) { // STREET
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else {
                    spawnedTile.GetComponent<MeshRenderer>().material = _grassMaterial;
                }

                _tiles[new Vector2(x, y)] = spawnedTile;
            }
        }

        // TODO: Add IF to check if tile is end point
        _trafficLightPositions = new Vector2[4];
        _trafficLightPositions[0] = new Vector2(laneMax, laneMin - 1); // Bottom
        _trafficLightPositions[1] = new Vector2(laneMax, laneMax); // Right
        _trafficLightPositions[2] = new Vector2(laneMin - 1, laneMin - 1); // Left
        _trafficLightPositions[3] = new Vector2(laneMin - 1, laneMax); // Top 

        var t4 =Instantiate(_trafficLightPrefab, new Vector3(_trafficLightPositions[0].x * 10 - 5, 0, _trafficLightPositions[0].y * 10 + 5), Quaternion.Euler(0,-35,0));
        t4.name = "4";
        var t2 =Instantiate(_trafficLightPrefab, new Vector3(_trafficLightPositions[1].x * 10 - 5, 0, _trafficLightPositions[1].y * 10 - 5), Quaternion.Euler(0, -125, 0));
        t2.name = "2";
        var t3 =Instantiate(_trafficLightPrefab, new Vector3(_trafficLightPositions[2].x * 10 + 5, 0, _trafficLightPositions[2].y * 10 + 5), Quaternion.Euler(0, 55, 0));
        t3.name = "3";
        var t1 =Instantiate(_trafficLightPrefab, new Vector3(_trafficLightPositions[3].x * 10 + 5, 0, _trafficLightPositions[3].y * 10 - 5), Quaternion.Euler(0, 145, 0));
        t1.name = "1";

        _trafficLights.Add(t1);
        _trafficLights.Add(t2);
        _trafficLights.Add(t3);
        _trafficLights.Add(t4);




       

        
        // _cam.transform.position = new Vector3((float)_width/2 -0.5f, (float)_height / 2 - 0.5f,-10);
    }

    public Tile GetTileAtPosition(Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) return tile;
        return null;
    }

    // Move Object to a tile
    public void MoveObjectToTile(GameObject obj, Vector2 pos, WebSocket websocket, int activeCars) {
        if (_tiles.TryGetValue(pos, out var tile)) {
            // Move object slowly to the tile
            StartCoroutine(MoveCar(obj, tile, websocket, activeCars));
            
        }
    }

    public Vector3 GetTileCenter(Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) {
            return tile.transform.position;
        }
        return Vector3.zero;
    }

    public bool isTileEnd(Vector2 pos) {
        for (int i = 0; i < _endPositions.Count; i++) {
            if (pos == _endPositions[i]) {
                return true;
            }
        }
        return false;
    }

    // MoveObjectToTileCoroutine
    IEnumerator MoveCar(GameObject obj, Tile tile, WebSocket websocket, int activeCars) {
        var startPos = obj.transform.position;
        var endPos = tile.transform.position;

        // Rotate the car to the right direction
        obj.transform.LookAt(endPos);


        var t = 0f;
        while (t < 1 && obj != null) {
            t += Time.deltaTime * speed;
            obj.transform.position = Vector3.Lerp(startPos, endPos, t);
            yield return null;
        }
        _movedCarsCount++;



        if (_movedCarsCount == activeCars) {
            _movedCarsCount = 0;
            // _activeCarsCount = 0;
            websocket.SendText("Cars moved");
        }
    }

    public void setLightState(int id, TrafficLight state){

        // Loop through traffic light children with id
        var current_traffic_light = _trafficLights[id];
        var color = (int) state;

        // Loop through children
        foreach (Transform child in current_traffic_light.transform) {

            if (child.name == color.ToString()) {
                child.gameObject.SetActive(true);
                
            } else {
                child.gameObject.SetActive(false);
            }
        }




    }

}

// q: How to remove added files from git?
// a: git rm --cached <file>