import pygame
from gtts import gTTS
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

ip = 'ROUTER_IP'
password = 'ROUTER_PASSWORD'
enable_tts = True


def speak(text_to_say):
    target_file = "speech.mp3"
    audio = gTTS(text=text_to_say, lang="en", tld="us", slow=False)
    audio.save(target_file)

    pygame.mixer.init()
    pygame.mixer.music.load(target_file)
    pygame.mixer.music.play()
    try:
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except KeyboardInterrupt:
        pass  # Handle the exception when trying to CTRL-C out of the script
    finally:
        pygame.mixer.quit()
        print("---FINISHED SPEAKING---")


def get_param_message(param):
    value = client.device.signal().get(param)
    strength_level = 'UNKNOWN'
    numeric_value = float(str(value).replace("dB", "").replace("m", ""))
    if param == 'rsrq':
        if numeric_value >= -10:
            strength_level = 'Excellent'
        elif -10 < numeric_value <= -15:
            strength_level = 'Good'
        elif -15 < numeric_value <= -20:
            strength_level = 'Poor'
        else:
            strength_level = "No signal"
    elif param == 'rsrp':
        if numeric_value >= -80:
            strength_level = 'Excellent'
        elif -80 < numeric_value <= -90:
            strength_level = 'Good'
        elif -90 < numeric_value <= -100:
            strength_level = 'Poor'
        else:
            strength_level = "No signal"
    elif param == 'rssi':
        if numeric_value >= -65:
            strength_level = 'Excellent'
        elif -65 < numeric_value >= -75:
            strength_level = 'Good'
        elif -75 < numeric_value <= -95:
            strength_level = 'Poor'
        else:
            strength_level = "No signal"
    elif param == 'sinr':
        if numeric_value >= 20:
            strength_level = 'Excellent'
        elif 13 < numeric_value <= 20:
            strength_level = 'Good'
        elif 0 < numeric_value <= 13:
            strength_level = 'Poor'
        else:
            strength_level = "No signal"
    return param.upper() + "\t" + str(value) + "\t" + strength_level + ","


print("---INFORMATION---")
print(
    "RSSI - Received Signal Strength Indicator, it's a negative value, and the closer to 0, the stronger the signal.\n"
    "RSRP - Reference Signal Received Power is the power of the LTE Reference Signals spread over the full bandwidth and narrowband\n"
    "RSRQ - Reference Signal Received Quality, indicates the quality of the received reference signal.\n"
    "SINR - Signal to Interference plus Noise Ratio, indicates the throughput capacity of the channel.")
print("---VALUES---")
while True:
    with Connection(f'http://admin:{password}@{ip}') as connection:
        client = Client(connection)

        # Parameters
        rsrq = get_param_message('rsrq')
        rsrp = get_param_message('rsrp')
        rssi = get_param_message('rssi')
        sinr = get_param_message('sinr')

        message = f'{rsrq}\n{rsrp}\n{rssi}\n{sinr}'
        print("Param\tValue\tStrength")
        print("============================")
        print(message)
        print("============================")
        if enable_tts:
            speak(message)
