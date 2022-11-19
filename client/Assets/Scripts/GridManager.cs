using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridManager : MonoBehaviour {
    [SerializeField] private int _width, _height;

    [SerializeField] private Tile _tilePrefab;

    [SerializeField] private Transform _cam;

    private Dictionary<Vector2, Tile> _tiles;

    void Start() {
        GenerateGrid();
    }

    void GenerateGrid() {
        _tiles = new Dictionary<Vector2, Tile>();
        for (int x = 0; x < _width; x++) {
            for (int y = 0; y < _height; y++) {
                var spawnedTile = Instantiate(_tilePrefab, new Vector3(x * 10, 0, y * 10), Quaternion.identity);
                spawnedTile.name = $"Tile {x} {y}";

                // TODO Make this dynamic

                if ((x < 6 && y < 6) || (x > 11 && y > 11) || (x > 11 && y < 6) || (x < 6 && y > 11)) {
                    // Change the color of the tile
                    spawnedTile.GetComponent<Renderer>().material.color = Color.red;
                }


                _tiles[new Vector2(x, y)] = spawnedTile;
            }
        }

        _cam.transform.position = new Vector3((float)_width/2 -0.5f, (float)_height / 2 - 0.5f,-10);
    }

    public Tile GetTileAtPosition(Vector2 pos) {
        if (_tiles.TryGetValue(pos, out var tile)) return tile;
        return null;
    }
}