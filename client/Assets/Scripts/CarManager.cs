using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using NativeWebSocket;



public class CarManager : MonoBehaviour
{

    // List of car prefabs
    [SerializeField] private GameObject _carPrefab;

    // Number of cars to spawn
    [SerializeField] private int _mapSize = 18;
    [SerializeField] private int _numCars = 1;
    [SerializeField] private int _numLanes = 3;

    [SerializeField] private GridManager _grid;

    // Dictionary of cars and gameobjects
    private Dictionary<int, GameObject> _cars;



    [SerializeField] private string _serverUrl = "ws://localhost:8765";

    public WebSocket websocket;




    // Start is called before the first frame update
    async void Start()
    {
        websocket = new WebSocket(_serverUrl);

        websocket.OnOpen += () =>
        {
            Debug.Log("Connection open!");
        };


        websocket.OnMessage += (bytes) => {
            var message = System.Text.Encoding.UTF8.GetString(bytes);

            if (message != "Done") { 

            var list_cars = JsonUtility.FromJson<ListCars>(message);

            Debug.Log(list_cars.t);

            if (list_cars.t == 0){
                Debug.Log("First Step");
                _cars = new Dictionary<int, GameObject>();

                foreach (var c in list_cars.cars)
                {
                    var car = c;
                    var carObject = Instantiate(_carPrefab, _grid.GetTileCenter(new Vector2(car.x, car.y)), Quaternion.identity);
                    
                    _cars.Add(car.id, carObject);
                }


            } else {
                foreach (var car in list_cars.cars)
                {
                    var carObject = _cars[car.id];
                    _grid.MoveObjectToTile(carObject, new Vector2(car.x, car.y), websocket);
                }
            }

        }

        };

        InvokeRepeating("SendWebSocketMessage", 0.0f, 1.0f); //TODO Change this



        await websocket.Connect();

        
    }

    // Update is called once per frame
    void Update()
    {
        // TODO Don't know if this is necessary
        #if !UNITY_WEBGL || UNITY_EDITOR
            websocket.DispatchMessageQueue();
        #endif
        
    }

    async void SendWebSocketMessage() {
        if (websocket.State == WebSocketState.Open) {
            await websocket.SendText(_mapSize.ToString());
            await websocket.SendText(_numLanes.ToString());
            await websocket.SendText(_numCars.ToString());
        }
    }




    private async void OnApplicationQuit() {
        await websocket.Close();
    }
}
