from chatgpt_hackathon import get_model_run
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
    print(f"Export complete - {len(labels)} labels")    
    data_row_id_to_model_input = {}
    training_file_name = "completions.jsonl"
    my_file = open(training_file_name, "w")
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
    print(f"Success: Created training file with name `{training_file_name}`")   
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

def get_text(label):
    """ Gets text for a given asset in GCS
    Args:
    Returns:
    """
    gs_url = label['Labeled Data']
    https_url = f"https://storage.googleapis.com/{gs_url[5:]}"
    text = requests.get(https_url).content.decode()
    return text  
