using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraManager : MonoBehaviour
{

    // ARRAY OF CAMERAS
    [SerializeField] private Camera[] _cameras;
    private int _currentCameraIndex = 0;
    private Camera _carCamera;


    // Start is called before the first frame update
    void Start()
    {
        // SET ALL CAMERAS TO FALSE
        foreach (var camera in _cameras)
        {
            camera.gameObject.SetActive(false);
        }

        // SET FIRST CAMERA TO TRUE
        _cameras[_currentCameraIndex].gameObject.SetActive(true);
        
    }



    // CHANGE CAMERA
    public void ChangeCamera() {
        if (_carCamera != null) {
            _carCamera.gameObject.SetActive(false);
            _carCamera = null;
        } else {
            // SET CURRENT CAMERA TO FALSE
            _cameras[_currentCameraIndex].gameObject.SetActive(false);
            // INCREMENT CURRENT CAMERA INDEX
            _currentCameraIndex++;
        }

        // IF CURRENT CAMERA INDEX IS GREATER THAN THE NUMBER OF CAMERAS, RESET TO 0
        if (_currentCameraIndex >= _cameras.Length) {
            _currentCameraIndex = 0;
        }

        // SET NEW CAMERA TO TRUE
        _cameras[_currentCameraIndex].gameObject.SetActive(true);
    }

    public void CarView(Camera carCamera) {
        if (_carCamera != null) {
            _carCamera.gameObject.SetActive(false);
        } else {
            // SET CURRENT CAMERA TO FALSE
            _cameras[_currentCameraIndex].gameObject.SetActive(false);
        }
        _carCamera = carCamera;
        // SET NEW CAMERA TO TRUE
        // get camera from children
        carCamera.gameObject.SetActive(true);
    }
}
