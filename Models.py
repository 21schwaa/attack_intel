#models.py 
#this pyhton code is to intilize models which will be called in both the analysis and interactive code
# you may change the models here if you wish
# please note that these are global 
import time
from gpt4all import GPT4All

#loads model for command generation on interactive prompt
def load_main_model():
    print("\nLoading Main Model...\n")
    time.sleep(2)
    model = GPT4All("whiterabbitneo-13b.Q8_0.gguf")
    print("Main Model Successfully Loaded\n")
    return model

#loads model for report and analysis generation for analysis mode
def load_analysis_model():
    print("\nLoading Analysis Model...\n")
    time.sleep(2)
    model = GPT4All("Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf")
    print("Analysis Model Successfully Loaded")
    return model



