using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using NativeWebSocket;

public class WebSocketClient : MonoBehaviour
{
    // Server URL
    [SerializeField] private string _serverUrl = "ws://localhost:8765";

    // Grid manager
    [SerializeField] private GridManager _grid;

    // GameObjects
    [SerializeField] private GameObject _carPrefab;

    // WebSocket
    WebSocket websocket;

    async void Start()
    {
        websocket = new WebSocket(_serverUrl);

        websocket.OnOpen += () =>
        {
            Debug.Log("Connection open!");
        };

        // websocket.OnError += (e) =>
        // {
        //     Debug.Log("Error! " + e);
        // };

        // websocket.OnClose += (e) =>
        // {
        //     Debug.Log("Connection closed!");
        // };

        websocket.OnMessage += (bytes) => {
            var message = System.Text.Encoding.UTF8.GetString(bytes);

            // Parse the message
            var car = JsonUtility.FromJson<ListCars>(message);

            // Move cars
            foreach (var c in car.cars)
            {
                // _grid.MoveObjectToTile(_carPrefab, new Vector2(c.x, c.y), websocket);
            }


            // Wait for 10 seconds

            // Debug.Log("OnMessage!");
            // Debug.Log(bytes);

            // // getting the message as a string
            // // Debug.Log("OnMessage! " + message);
        };

        // Keep sending messages at every 0.3s
        InvokeRepeating("SendWebSocketMessage", 0.0f, 1.0f);

        // waiting for messages
        await websocket.Connect();
    }

    // Update is called once per frame
    void Update()
    {
        #if !UNITY_WEBGL || UNITY_EDITOR
            websocket.DispatchMessageQueue();
        #endif
    }

    async void SendWebSocketMessage() {
        if (websocket.State == WebSocketState.Open) {
            // Sending bytes
            //await websocket.Send(new byte[] { 10, 20, 30 });
            // Sending plain text
            await websocket.SendText("18");
            await websocket.SendText("3");
            await websocket.SendText("1");
        }
    }

    private async void OnApplicationQuit() {
        await websocket.Close();
    }





}
