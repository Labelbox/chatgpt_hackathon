from chatgpt_hackathon import get_model_with_name
import requests
import json
import requests
import json
import openai

def initiate_fine_tuning(api_key, client, team_name, training_round):
    """ For a given training round, generates a training file to-be-passed to OpenAI and a dictionary with data row ID and input data
    """
    model_run = get_model_run(client, team_name, training_round)
    print(f"Exporting labels...")
    labels = model_run.export_labels(download=True)
    print(f"Export complete")    
    data_row_id_to_model_input = {}
    my_file = open("completions.jsonl", "w")
    print(f"Creating training file...")
    for label in labels:
        text = get_text(label)
        chatgpt_dict = {
            "prompt" : f"{get_text(label)}#-#-#-#-#",
            "completion" : f"{label['Label']['classifications'][0]['answer']['value']}#####"
        }
        data_row_id_to_model_input[label["DataRow ID"]] = chatgpt_dict
        as_string = json.dumps(chatgpt_dict)
        my_file.write(f"{as_string}\n")      
    print(f"Success: Created training file with name `completions.jsonl`")   
    print(f"Connecting with OpenAI...")
    openai_key = requests.post("https://us-central1-saleseng.cloudfunctions.net/get-openai-key", data=json.dumps({"api_key" : api_key}))
    openai_key = openai_key.content.decode()
    if "Error" in openai_key:
        raise ValueError(f"Incorrect API key - please ensure that your Labelbox API key is correct and try again")
    else:
        openai.api_key = openai_key
    print(f"Success: Connected with OpenAI")        
    # Load training file into OpenAI
    training_file = openai.File.create(
        file=open(training_file_name,'r'), 
        purpose='fine-tune'
    )
    # Initiate training
    fine_tune_job = openai.FineTune.create(
        api_key=openai_key, 
        training_file=training_file["id"], 
        model = 'ada'
    )
    fune_tune_job_id = fine_tune_job["id"]
    print(f'Fine-tune Job with ID `{fune_tune_job_id}` initiated')
    return fune_tune_job_id, data_row_id_to_model_input
  
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
