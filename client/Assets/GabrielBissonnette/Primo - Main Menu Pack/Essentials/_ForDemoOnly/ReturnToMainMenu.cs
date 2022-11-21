using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class ReturnToMainMenu : MonoBehaviour
{
    public void LoadMainMenu()
    {
        SceneManager.LoadScene("Demo1");
    }
}
