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

    void Awake()
    {
        _data = _vehicleSOs[Random.Range(0, _vehicleSOs.Length)];
        UpdateVehicle();
        
    }

    private void UpdateVehicle() {

        if(_childVehicle != null) {
            Destroy(_childVehicle);
        }

        // utilizando los datos construir carrito
        _childVehicle = Instantiate<GameObject>(
            _data.model, 
            transform.position, 
            transform.rotation,
            transform
            );

        _childVehicle.transform.localScale = new Vector3(
            _data.scale, 
            _data.scale, 
            _data.scale
        );

        BoxCollider bc = gameObject.AddComponent<BoxCollider>();
        bc.size = new Vector3(_data.width * _data.scale, _data.height * _data.scale, _data.depth * _data.scale);
        bc.center = new Vector3(0, _data.height * _data.scale / 2, 0);
    }

    public void UpdateVehicle(VehicleSO newVehicle) {

        _data = newVehicle;
        UpdateVehicle();
    }

}
