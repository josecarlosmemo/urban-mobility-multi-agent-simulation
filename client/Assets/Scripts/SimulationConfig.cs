using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimulationConfig : MonoBehaviour
{
    // Get 3 text areas from the UI
    [SerializeField] private TMPro.TMP_InputField _mapSize;
    [SerializeField] private TMPro.TMP_InputField _numAgents;
    [SerializeField] private TMPro.TMP_InputField _numLanes;

    // Start
    void Start()
    {
        // Try to get the values from the PlayerPrefs
        if (PlayerPrefs.HasKey("mapSize")) _mapSize.text = PlayerPrefs.GetInt("mapSize").ToString();
        if (PlayerPrefs.HasKey("numAgents")) _numAgents.text = PlayerPrefs.GetInt("numAgents").ToString();
        if (PlayerPrefs.HasKey("numLanes")) _numLanes.text = PlayerPrefs.GetInt("numLanes").ToString();

        // Set the default values
        if (_mapSize.text == "") _mapSize.text = "20";
        if (_numAgents.text == "") _numAgents.text = "100";
        if (_numLanes.text == "") _numLanes.text = "2";
       
    }




  
}
