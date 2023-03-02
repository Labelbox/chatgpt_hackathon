from chatgpt_hackathon import get_model_run, get_chatgpt_input
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
    openai_key = requests.post("https://us-central1-saleseng.cloudfunctions.net/get-openai-key", data=json.dumps({"api_key" : api_key}))
    openai_key = openai_key.content.decode()
    if "Error" in openai_key:
        raise ValueError(f"Incorrect API key - please ensure that your Labelbox API key is correct and try again")
    else:
        openai.api_key = openai_key  
    training_round = str(training_round)
    model_run = get_model_run(client, team_name, training_round)        
    print(f"Exporting labels...")
    labels = model_run.export_labels(download=True)
    print(f"Export complete - {len(labels)} labels")       
    # Create predictions
    print(f"Creating predictions and uploading to model run...")
    predictions = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(create_prediction, openai_key, chatgpt_model_name, label) for label in labels]
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

def create_prediction(openai_key, chatgpt_model_name, label):
    chatgpt_dict, data_row_id = get_chatgpt_input(label)
    pred = openai.Completion.create(
        api_key = openai_key,
        model = chatgpt_model_name,
        prompt = chatgpt_dict["prompt"],
        max_tokens = 1,
        logprobs = 4,
        temperature = 1
    )           
    radio_prediction = lb_types.ClassificationAnnotation(
        name="emotion", 
        value= lb_types.Radio(answer=lb_types.ClassificationAnswer(
            name=f"{pred['choices'][0]['logprobs']['tokens'][0]}",
            confidence= 1 + (int(pred['choices'][0]['logprobs']['token_logprobs'][0])/10)
        )))     
    label_prediction = lb_types.Label(
        data=lb_types.TextData(uid=data_row_id),
        annotations = [radio_prediction]
    )
    return label_prediction
