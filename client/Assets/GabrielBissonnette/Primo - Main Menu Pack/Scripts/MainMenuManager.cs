using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Audio;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class MainMenuManager : MonoBehaviour
{
    #region Variables

    [Header("On/Off")]
    [Space(5)] [SerializeField] bool showBackground;
    [SerializeField] bool showSocial1;
    [SerializeField] bool showSocial2;
    [SerializeField] bool showSocial3;
    [SerializeField] bool showVersion;
    [SerializeField] bool showFade;

    [Header("Scene")]
    [Space(10)] [SerializeField] string sceneToLoad;

    [Header("Sprites")]
    [Space(10)] [SerializeField] Sprite logo;
    [SerializeField] Sprite background;
    [SerializeField] Sprite buttons;

    [Header("Color")]
    [Space(10)] [SerializeField] Color32 mainColor;
    [SerializeField] Color32 secondaryColor;

    [Header("Version")]
    [Space(10)] [SerializeField] string version = "v.0105";

    [Header("Texts")]
    [Space(10)] [SerializeField] string play = "Play";
    [SerializeField] string settings = "Settings";
    [SerializeField] string quit = "Quit";

    [Header("Social")]
    [Space(10)] [SerializeField] Sprite social1Icon;
    [SerializeField] string social1Link;
    [Space(5)]
    [SerializeField] Sprite social2Icon;
    [SerializeField] string social2Link;
    [Space(5)]
    [SerializeField] Sprite social3Icon;
    [SerializeField] string social3Link;
    List<string> links = new List<string>();

    [Header("Audio")]
    [Space(10)] [SerializeField] float defaultVolume = 0.8f;
    [SerializeField] AudioClip uiClick;
    [SerializeField] AudioClip uiHover;
    [SerializeField] AudioClip uiSpecial;


    // Components
    [Header("Components")]
    [SerializeField] GameObject homePanel;
    [SerializeField] GameObject settingsPanel;
    [SerializeField] GameObject bannerPanel;
    [SerializeField] Image social1Image;
    [SerializeField] Image social2Image;
    [SerializeField] Image social3Image;
    [SerializeField] Image logoImage;
    [SerializeField] Image backgroundImage;

    [Header("Fade")]
    [Space(10)] [SerializeField] Animator fadeAnimator;

    [Header("Color Elements")]
    [Space(5)] [SerializeField] Image[] mainColorImages;
    [SerializeField] TextMeshProUGUI[] mainColorTexts;
    [SerializeField] Image[] secondaryColorImages;
    [SerializeField] TextMeshProUGUI[] secondaryColorTexts;
    [SerializeField] Image[] buttonsElements;

    [Header("Texts")]
    [Space(10)] [SerializeField] TextMeshProUGUI playText;
    [SerializeField] TextMeshProUGUI settingsText;
    [SerializeField] TextMeshProUGUI quitText;
    [SerializeField] TextMeshProUGUI versionText;   

    [Header("Settings")]
    [Space(10)] [SerializeField] Slider volumeSlider;
    [SerializeField] TMP_Dropdown resolutionDropdown;

    [Header("Audio")]
    [SerializeField] AudioSource audioSource;

    Resolution[] resolutions;

    #endregion

    void Start()
    {
        SetStartUI();
        ProcessLinks();
        SetStartVolume();
        //PrepareResolutions();
    }

    private void SetStartUI()
    {
        //fadeAnimator.SetTrigger("FadeIn");
        homePanel.SetActive(true);
        settingsPanel.SetActive(false);
    }

    public void UIEditorUpdate()
    {
        // Used to update the UI when not in play mode

        #region Sprites

        // Logo
        if (logoImage != null)
        {
            logoImage.sprite = logo;
            logoImage.color = mainColor;
            logoImage.SetNativeSize();
        }

        // Background
        if (backgroundImage != null)
        {
            backgroundImage.gameObject.SetActive(showBackground);
            backgroundImage.sprite = background;
            backgroundImage.SetNativeSize();
        }

        // Main Color Images
        for (int i = 0; i < mainColorImages.Length; i++)
        {
            mainColorImages[i].color = mainColor;
        }

        // Main Color Texts
        for (int i = 0; i < mainColorTexts.Length; i++)
        {
            mainColorTexts[i].color = mainColor;
        }

        // Secondary Color Images
        for (int i = 0; i < secondaryColorImages.Length; i++)
        {
            secondaryColorImages[i].color = secondaryColor;
        }

        // Secondary Color Texts
        for (int i = 0; i < secondaryColorTexts.Length; i++)
        {
            secondaryColorTexts[i].color = secondaryColor;
        }

        // Buttons Elements
        for (int i = 0; i < buttonsElements.Length; i++)
        {
            buttonsElements[i].sprite = buttons;
        }

        // Fade
        fadeAnimator.gameObject.SetActive(showFade);

        #endregion


        #region Texts

        if (playText != null)
            playText.text = play;

        if (settingsText != null)
            settingsText.text = settings;

        if (quitText != null)
            quitText.text = quit;

        // Version number
        versionText.gameObject.SetActive(showVersion);
        if (versionText != null)
            versionText.text = version;

        #endregion


        #region Social

        if (social1Image != null)
        {
            social1Image.sprite = social1Icon;
            social1Image.gameObject.SetActive(showSocial1);
        }

        if (social2Image != null)
        {
            social2Image.sprite = social2Icon;
            social2Image.gameObject.SetActive(showSocial2);
        }

        if (social3Image != null)
        {
            social3Image.sprite = social3Icon;
            social3Image.gameObject.SetActive(showSocial3);
        }

        #endregion
    }

    #region Links
    public void OpenLink(int _index)
    {
        if(links[_index].Length > 0)
            Application.OpenURL(links[_index]);
    }

    private void ProcessLinks()
    {
        if (social1Link.Length > 0)
            links.Add(social1Link);

        if (social2Link.Length > 0)
            links.Add(social2Link);

        if (social3Link.Length > 0)
            links.Add(social3Link);
    }
    #endregion


    #region Levels
    public void LoadLevel()
    {
        // Fade Animation
        fadeAnimator.SetTrigger("FadeOut");

        StartCoroutine(WaitToLoadLevel());
    }

    IEnumerator WaitToLoadLevel()
    {
        yield return new WaitForSeconds(1f);

        // Scene Load
        SceneManager.LoadScene(sceneToLoad);
    }

    public void Quit()
    {
        Application.Quit();
    }
    #endregion


    #region Audio

    public void SetVolume(float _volume)
    {
        // Adjust volume
        AudioListener.volume = _volume;

        // Save volume
        PlayerPrefs.SetFloat("Volume", _volume);
    }

    void SetStartVolume()
    {
        if (!PlayerPrefs.HasKey("Volume"))
        {
            PlayerPrefs.SetFloat("Volume", defaultVolume);
            LoadVolume();
        }
        else
        {
            LoadVolume();
        }
    }

    public void LoadVolume()
    {
        volumeSlider.value = PlayerPrefs.GetFloat("Volume");
    }

    public void UIClick()
    {
        audioSource.PlayOneShot(uiClick);
    }

    public void UIHover()
    {
        audioSource.PlayOneShot(uiHover);
    }

    public void UISpecial()
    {
        audioSource.PlayOneShot(uiSpecial);
    }

    #endregion


    #region Graphics & Resolution Settings

    public void SetQuality(int _qualityIndex)
    {
        QualitySettings.SetQualityLevel(_qualityIndex);
    }

    public void SetFullscreen(bool isFullscreen)
    {
        Screen.fullScreen = isFullscreen;
    }

    public void PrepareResolutions()
    {
        resolutions = Screen.resolutions;
        resolutionDropdown.ClearOptions();

        List<string> options = new List<string>();

        int currentResolutionIndex = 0;

        for (int i = 0; i < resolutions.Length; i++)
        {
            string option = resolutions[i].width + " x " + resolutions[i].height;

            if(!options.Contains(option))
                options.Add(option);

            if(i == resolutions.Length - 1)
            {
                currentResolutionIndex = i;
            }
        }

        resolutionDropdown.AddOptions(options);
        resolutionDropdown.value = currentResolutionIndex;
        resolutionDropdown.RefreshShownValue();
    }

    public void SetResolution(int _resolutionIndex)
    {
        Resolution resolution = resolutions[_resolutionIndex];
        Screen.SetResolution(resolution.width, resolution.height, Screen.fullScreen);
    }

    #endregion
}
