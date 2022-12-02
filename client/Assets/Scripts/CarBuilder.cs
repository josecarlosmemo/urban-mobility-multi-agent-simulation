using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarBuilder : MonoBehaviour
{

    // CÓMO DETECTAR QUE OBJETO FUE CLICKEADO
    // https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnMouseDown.html

    private VehicleSO _data;
    [SerializeField] private VehicleSO[] _vehicleSOs;

    private GameObject _childVehicle;

    [SerializeField]
    private CameraManager _cameraManager;
    private Camera _camera;

    void Awake()
    {
        _data = _vehicleSOs[Random.Range(0, _vehicleSOs.Length)];
        UpdateVehicle();
        _camera = gameObject.transform.Find("Camera").GetComponent<Camera>();
    }
    




    private void UpdateVehicle() {

        if(_childVehicle != null) {
            Destroy(_childVehicle);
        }

        // utilizando los datos construir carrito
        _childVehicle = Instantiate<GameObject>(
            _data.model, 
            transform.position, 
            (_data.rotX == 0 && _data.rotY == 0 && _data.rotZ == 0) ? transform.rotation : Quaternion.Euler(_data.rotX, _data.rotY, _data.rotZ),
            transform
            );


        // If the vehicle has a translation, apply it
        if (_data.transX != 0 || _data.transY != 0 || _data.transZ != 0) {
            _childVehicle.transform.Translate(_data.transX, _data.transY, _data.transZ);
        }

        _childVehicle.transform.localScale = new Vector3(
            _data.scale, 
            _data.scale, 
            _data.scale
        );

        BoxCollider bc = gameObject.AddComponent<BoxCollider>();
        bc.size = new Vector3(_data.width * _data.scale + 2, _data.height * _data.scale + 2, _data.depth * _data.scale + 2);
        bc.center = new Vector3(0, _data.height * _data.scale / 2, 0);

        // add collider detection
        




    }

    public void UpdateVehicle(VehicleSO newVehicle) {

        _data = newVehicle;
        UpdateVehicle();
    }

    void OnTriggerEnter(Collider other) {
        if (_camera.gameObject.activeSelf) {
            // Deactivate camera
            _camera.gameObject.SetActive(false);
            _cameraManager.ChangeCamera();
        }
        Destroy(gameObject);
    }

    void OnMouseDown() {
        // Find active camera manager
        if (_cameraManager == null) {
            _cameraManager = FindObjectOfType<CameraManager>();
        }
        _cameraManager.CarView(_camera);
    }

}
