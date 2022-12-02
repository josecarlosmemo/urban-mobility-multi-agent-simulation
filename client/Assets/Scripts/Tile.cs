using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Tile : MonoBehaviour
{
    private bool _isEnd = false;


    // Start is called before the first frame update
    void Start()
    {
         
        
    }

    void Awake() {
       
    }




    // Update is called once per frame
    void Update()
    {
       
        // Check if the tile is the end of the road
        if (GetComponent<Collider>() != null) {

            

            // Check if an object with layer vehicle is colliding with the tile
            if (Physics.CheckSphere(transform.position, 0.5f, LayerMask.GetMask("Vehicle"))) {
                Debug.Log("End of the road");
            }

            
            

            


           
        }
        
    }

    void OnDrawGizmos() {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, 0.5f);
    }
}
