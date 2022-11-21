using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridManager : MonoBehaviour {
    [SerializeField] private int _mapSize = 18;
    [SerializeField] private int _nLanes = 3;

    [SerializeField] private Material _grassMaterial;
    [SerializeField] private Material _roadMaterial;
    

    [SerializeField] private Tile _tilePrefab;

    [SerializeField] private Transform _cam;

    private Dictionary<Vector2, Tile> _tiles;

    void Start() {
        GenerateGrid();
    }

    void GenerateGrid() {
        _tiles = new Dictionary<Vector2, Tile>();
        for (int x = 0; x < _mapSize; x++) {
            for (int y = 0; y < _mapSize; y++) {
                var spawnedTile = Instantiate(_tilePrefab, new Vector3(x * 10, 0, y * 10), Quaternion.identity);
                spawnedTile.name = $"Tile {x} {y}";


                int laneMin = (_mapSize - _nLanes * 2) / 2;
                int laneMax = laneMin + _nLanes * 2;
                int laneMid = laneMin + _nLanes;

                if (laneMin <= x && x < laneMax && laneMin <= y && y < laneMax){
                    // self.tiles[i].append(TypesTiles.INTERSECTION)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (y == 0 && laneMin <= x && x < laneMid || y == _mapSize - 1 && laneMid <= x && x < laneMax || x == 0 && laneMid <= y&& y < laneMax || x == _mapSize - 1 && laneMin <= y && y< laneMid){
                    // spawn_points.append((i, j))
                    // self.tiles[i].append(TypesTiles.SPAWN)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (y == laneMin - 1 && laneMin <= x&& x < laneMid || y == laneMax && laneMid <= x && x < laneMax || x == laneMin - 1 && laneMid <= y && y < laneMax || x == laneMax && laneMin <= y&& y < laneMid){
                    // self.tiles[i].append(TypesTiles.TRAFFIC_LIGHT)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if ((y == laneMin - 3 || y == laneMin - 5) && laneMin <= x&& x < laneMid || (y == laneMax + 2 || y == laneMax + 4) && laneMid <= x&& x < laneMax || (x == laneMin - 3 || x == laneMin - 5) && laneMid <= y && y < laneMax || (x == laneMax + 2 || x == laneMax + 4) && laneMin <= y && y < laneMid){
                    // self.tiles[i].append(TypesTiles.SWITCH_LANE)
                    spawnedTile.GetComponent<Renderer>().material = _roadMaterial;


                } else if (0 <= x && x < laneMin && laneMin <= y && y < laneMid || laneMax <= x && x < _mapSize && laneMid <= y && y < laneMax || 0 <= y && y < laneMin && laneMid <= x && x < laneMax || laneMax <= y && y < _mapSize && laneMin <= x && x < laneMid){
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

                // TODO: Add IF to check if tile is end point
                    




                // // TODO Make this dynamic

                // if ((x < 6 && y < 6) || (x > 11 && y > 11) || (x > 11 && y < 6) || (x < 6 && y > 11)) {
                //     // Change the color of the tile
                //     spawnedTile.GetComponent<Renderer>().material.color = Color.red;
                // }


                _tiles[new Vector2(x, y)] = spawnedTile;
            }
        }

        // _cam.transform.position = new Vector3((float)_width/2 -0.5f, (float)_height / 2 - 0.5f,-10);
    }

    public Tile GetTileAtPosition(Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) return tile;
        return null;
    }

    // Move Object to a tile
    public void MoveObjectToTile(GameObject obj, Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) {
            obj.transform.position = tile.transform.position;
        }
    }

    public Vector3 GetTileCenter(Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) {
            return tile.transform.position;
        }
        return Vector3.zero;
    }





}

// q: How to remove added files from git?
// a: git rm --cached <file>