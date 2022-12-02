using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;

public class GridManager : MonoBehaviour {
    [SerializeField] private int _mapSize = 18;
    [SerializeField] private int _nLanes = 3;

    [SerializeField] private Material _grassMaterial;
    [SerializeField] private Material _roadMaterial;
    

    [SerializeField] private Tile _tilePrefab;

    [SerializeField] private Transform _cam;

    private Dictionary<Vector2, Tile> _tiles;

    private int _activeCarsCount = 0;
    private int _movedCarsCount = 0;
    // Private coordinate array
    private Vector2[] _trafficLightPositions;

    void Start() {
        GenerateGrid();
    }

    void GenerateGrid() {
        _tiles = new Dictionary<Vector2, Tile>();

        int laneMin = (_mapSize - _nLanes * 2) / 2;
        int laneMax = laneMin + _nLanes * 2;
        int laneMid = laneMin + _nLanes;

        for (int x = 0; x < _mapSize; x++) {
            for (int y = 0; y < _mapSize; y++) {
                var spawnedTile = Instantiate(_tilePrefab, new Vector3(x * 10, 0, y * 10), Quaternion.identity);
                spawnedTile.name = $"Tile {x} {y}";



                if (laneMin <= x && x < laneMax && laneMin <= y && y < laneMax){
                    // self.tiles[i].append(TypesTiles.INTERSECTION)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (y == 0 && laneMin <= x && x < laneMid || y == _mapSize - 1 && laneMid <= x && x < laneMax || x == 0 && laneMid <= y&& y < laneMax || x == _mapSize - 1 && laneMin <= y && y< laneMid){
                    spawnedTile.name = "End";
                    // spawn_points.append((i, j))
                    // self.tiles[i].append(TypesTiles.SPAWN)
                    // spawnedTile.GetComponent<Renderer>().material = _roadMaterial;
                    spawnedTile.GetComponent<Renderer>().material.color = Color.blue;

                    // Add collider to tile
                    spawnedTile.gameObject.AddComponent<BoxCollider>();

                    // detect if car is in tile
                    

                    

                    






                } else if (y == laneMin - 1 && laneMin <= x&& x < laneMid || y == laneMax && laneMid <= x && x < laneMax || x == laneMin - 1 && laneMid <= y && y < laneMax || x == laneMax && laneMin <= y&& y < laneMid){
                    // self.tiles[i].append(TypesTiles.TRAFFIC_LIGHT)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if ((y == laneMin - 3 || y == laneMin - 5) && laneMin <= x&& x < laneMid || (y == laneMax + 2 || y == laneMax + 4) && laneMid <= x&& x < laneMax || (x == laneMin - 3 || x == laneMin - 5) && laneMid <= y && y < laneMax || (x == laneMax + 2 || x == laneMax + 4) && laneMin <= y && y < laneMid){
                    // self.tiles[i].append(TypesTiles.SWITCH_LANE)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (y == 0 && laneMid <= x && x < laneMax || x == 0 && laneMin <= y && y < laneMid || y == _mapSize - 1 && laneMin <= x && x < laneMid || x == _mapSize - 1 && laneMid <= y && y < laneMax) {
                    // self.tiles[i].append(TypesTiles.END_STREET)
                    // spawnedTile.GetComponent<Renderer>().material = _roadMaterial;

                    // Change color to red
                    spawnedTile.GetComponent<Renderer>().material.color = Color.red;
                    
                    
                }

               else if (0 <= x && x < laneMin && laneMin <= y && y < laneMid || laneMax <= x && x < _mapSize && laneMid <= y && y < laneMax || 0 <= y && y < laneMin && laneMid <= x && x < laneMax || laneMax <= y && y < _mapSize && laneMin <= x && x < laneMid){
                    // self.tiles[i].append(TypesTiles.REVERSED_STREET)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (laneMin <= x && x < laneMax || laneMin <= y && y < laneMax){
                    // self.tiles[i].append(TypesTiles.STREET)
                    // Add material
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;

                } else {

                    // Add material to the tile
                    spawnedTile.GetComponent<MeshRenderer>().material = _grassMaterial;

                }

                //







            


                _tiles[new Vector2(x, y)] = spawnedTile;
            }
        }
        // TODO: Add IF to check if tile is end point
         _trafficLightPositions = new Vector2[4];
         _trafficLightPositions[0] = new Vector2(laneMax, laneMin); // Top
         _trafficLightPositions[1] = new Vector2(laneMax - 1, laneMax); // Right
         _trafficLightPositions[2] = new Vector2(laneMin, laneMin - 1); // Left
         _trafficLightPositions[3] = new Vector2(laneMin - 1, laneMax - 1); // Bottom 


        
        // _cam.transform.position = new Vector3((float)_width/2 -0.5f, (float)_height / 2 - 0.5f,-10);
    }

    public Tile GetTileAtPosition(Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) return tile;
        return null;
    }

    // Move Object to a tile
    public void MoveObjectToTile(GameObject obj, Vector2 pos, WebSocket websocket) {
        if (_tiles.TryGetValue(pos, out var tile)) {
            // Move object slowly to the tile
            StartCoroutine(MoveCar(obj, tile, websocket));
            
        }
    }

    public Vector3 GetTileCenter(Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) {
            return tile.transform.position;
        }
        return Vector3.zero;
    }

    public bool isTileEnd(Vector2 pos) {
        for (int i = 0; i < _trafficLightPositions.Length; i++) {
            if (pos == _trafficLightPositions[i]) {
                return true;
            }
        }
        return false;
    }

    // MoveObjectToTileCoroutine
    IEnumerator MoveCar(GameObject obj, Tile tile, WebSocket websocket) {
        var startPos = obj.transform.position;
        var endPos = tile.transform.position;

        // Rotate the car to the right direction
        obj.transform.LookAt(endPos);


        var t = 0f;
        while (t < 1) {
            t += Time.deltaTime;
            obj.transform.position = Vector3.Lerp(startPos, endPos, t);
            yield return null;
        }
        _movedCarsCount++;
        if (_movedCarsCount == _activeCarsCount) {
            _movedCarsCount = 0;
            _activeCarsCount = 0;
            websocket.SendText("Cars moved");
        }
    }

}

// q: How to remove added files from git?
// a: git rm --cached <file>