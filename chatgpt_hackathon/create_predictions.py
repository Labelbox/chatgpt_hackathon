from chatgpt_hackathon import get_model_run, get_chatgpt_input, get_project_with_name
from labelbox.data.serialization import NDJsonConverter
from concurrent.futures import ThreadPoolExecutor
import labelbox.data.annotation_types as lb_types
import openai
import uuid
import requests
import json
from tqdm import tqdm
from labelbase.ontology import get_ontology_schema_to_name_path

def create_predictions(api_key, client, team_name, training_round, chatgpt_model_name):
    # Get openai key
    print(f"Connecting with OpenAI...")
    openai_key = requests.post("https://us-central1-saleseng.cloudfunctions.net/get-openai-key", data=json.dumps({"api_key" : api_key}))
    openai_key = openai_key.content.decode()
    if "Error" in openai_key:
        raise ValueError(f"Incorrect API key - please ensure that your Labelbox API key is correct and try again")
    else:
        openai.api_key = openai_key
    print(f"Success: Connected with OpenAI")  
    training_round = str(training_round)
    model_run = get_model_run(client, team_name, training_round)        
    print(f"Exporting labels...")
    labels = model_run.export_labels(download=True)
    print(f"Export complete - {len(labels)} labels")    
    ontology = get_project_with_name(client, team_name).ontology()
    ontology_name_path_to_schema = get_ontology_schema_to_name_path(ontology, invert=True)
    # Create predictions
    print(f"Creating predictions...")
    predictions = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(create_prediction, openai_key, chatgpt_model_name, label, ontology_name_path_to_schema) for label in labels]
        for future in tqdm(futures, total=len(labels)):
            prediction = future.result()
            predictions.append(prediction)
    ndjson_prediction = list(NDJsonConverter.serialize(predictions)) 
    # Upload the prediction label to the Model Run
    upload_job_prediction = model_run.add_predictions(
        name=str(uuid.uuid4()),
        predictions=ndjson_prediction
    )
    # Errors will appear for annotation uploads that failed.
    upload_job.wait_till_done()
    err = upload_job.errors
    print("Errors:", upload_job_prediction.err)
    # Return upload results
    return err

def create_prediction(openai_key, chatgpt_model_name, label, ontology_name_path_to_schema):
    chatgpt_dict, data_row_id = get_chatgpt_input(label)
    pred = openai.Completion.create(
        api_key = openai_key,
        model = chatgpt_model_name,
        prompt = chatgpt_dict["prompt"],
        max_tokens = 2,
        logprobs = 28,
        temperature = 0
    )
    name_path = None
    # Check the answer first to see if it matches the ontology
    answer = pred['choices'][0]["text"]
    answer_name_path = f"emotions///{answer}"
    # If the answer name path is not in the ontology, let's see if any name paths start with what ChatGPT generated
    if answer_name_path not in ontology_name_path_to_schema.keys():
        for ont_path in ontology_name_path_to_schema:
            if ont_path.startswith(answer_name_path):
                name_path = ont_path
                break
    # If the answer name path is in the ontology, let's match it to its schema id
    else:
        name_path = answer_name_path
    # If we still don't have a name path, let's check our tokens
    if not name_path:
        token = pred['choices'][0]['logprobs']['tokens'][0]+pred['choices'][0]['logprobs']['tokens'][1]
        token = token.replace("#","")
        tok_name_path = f"emotions///{token}"   
        # If the token name path is not in the ontology, let's see if any name paths start with what ChatGPT generated
        if tok_name_path not in ontology_name_path_to_schema.keys():
            for ont_path in ontology_name_path_to_schema:
                if ont_path.startswith(tok_name_path):
                    name_path = ont_path
                    break
      # If the token name path is in the ontology, let's match it to its schema id
        else:
            name_path = tok_name_path
    # Catches when ChatGPT didn't do a good job at predicting sentiment within the parameters of the use case
    if not name_path:
        name_path = "emotions///neutral"
    schema_id = ontology_name_path_to_schema[name_path]
    pred_answer = name_path.split("///")[1]
    radio_prediction = lb_types.ClassificationAnnotation(
        name="emotion", 
        value= lb_types.Radio(answer=lb_types.ClassificationAnswer(
            name=pred_answer,
            confidence= 1 + (int(pred['choices'][0]['logprobs']['token_logprobs'][0])/10)
        )))     
    label_prediction = lb_types.Label(
        data=lb_types.TextData(uid=data_row_id),
        annotations = [radio_prediction]
    )    
    return label_prediction
