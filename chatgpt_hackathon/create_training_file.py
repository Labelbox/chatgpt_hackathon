import requests
import json
from chatgpt_hackathon import get_model_with_name

def create_training_file(client, team_name, training_round):
    """ For a given training round, generates a training file to-be-passed to OpenAI and a dictionary with data row ID and input data
    """
    model_run = get_model_run(client, team_name, training_round)
    labels = model_run.export_labels(download=True)
    data_row_id_to_model_input = {}
    my_file = open("completions.jsonl", "w")
    for label in labels:
        text = get_text(label)
        chatgpt_dict = {
            "prompt" : f"{get_text(label)}#-#-#-#-#",
            "completion" : f"{label['Label']['classifications'][0]['answer']['value']}#####"
        }
        data_row_id_to_model_input[label["DataRow ID"]] = chatgpt_dict
        as_string = json.dumps(chatgpt_dict)
        my_file.write(f"{as_string}\n")      
    return "completions.jsonl", data_row_id_to_model_input
  
def get_model_run(client, team_name, training_round):
    """ For a given model, iterates through names to get the right model run
    """
    model = get_model_with_name(client, team_name)
    found_model_run = False
    for model_run in model.model_runs():
        if model_run.name == str(training_round):
            found_model_run = True
            break
    if not found_model_run:
        raise ValueError(f"No model run for team name {team_name} with run name {training_round}")    
    return model_run

def get_text(label):
    """ Gets text for a given asset in GCS
    Args:
    Returns:
    """
    gs_url = label['Labeled Data']
    https_url = f"https://storage.googleapis.com/{gs_url[5:]}"
    text = requests.get(https_url).content.decode()
    return text  
