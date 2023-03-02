import labelbox.data.annotation_types as lb_types
from labelbox.data.serialization import NDJsonConverter
import openai
import time
import uuid
from datetime import datetime
from datetime import datetime
from pytz import timezone

def fine_tune_chatgpt(labelbox_key, client, team_name, training_round, training_file_name, data_row_id_to_model_input):
    # Get openai key
    openai.api_key = openai_key
    # Load training file into OpenAI
    training_file = openai.File.create(
        file=open(training_file_name,'r'), 
        purpose='fine-tune'
    )
    # Initiate training
    fine_tune_job = openai.FineTune.create(api_key=openai_key, training_file=training_file["id"], model = 'ada')
    print(f'Fine-tune initiated -- will check training status every 10 minutes until complete')
    # Check training status every 5 minutes
    tz = timezone('EST')  
    training = True
    while training:
        now = datetime.now(tz) 
        current_time = now.strftime("%H:%M:%S")
        res = openai.FineTune.list_events(id=fine_tune_job["id"])
        for event in res["data"]:
            if event["message"] == "Fine-tune succeeded":
                training = False
                break
        if training:
            print(f"{current_time} - Model training in progress, will check again in 5 minutes")
            time.sleep(300)
    print(f"{current_time} - Model training complete")            
    # Get ChatGPT Model Name
    for event in res["data"]:
        if (len(event["message"]) > 15) and (event["message"][:14] == "Uploaded model"):
            chatgpt_model_name = event["message"].split(": ")[1]    
    print(f"ChatGPT Model Name: `{chatgpt_model_name}` -- save this for hackaton submission")      
    # Create predictions
    print(f"Creating predictions and uploading to model run...")
    predictions = []
    for data_row_id in list(data_row_id_to_input.keys())[:2]:    
        pred = openai.Completion.create(
            api_key = openai_key,
            model = chatgpt_model_name,
            prompt = data_row_id_to_input[data_row_id]["prompt"],
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
        predictions.append(label_prediction)
    ndjson_prediction = list(NDJsonConverter.serialize(predictions)) 
    # Upload the prediction label to the Model Run
    upload_job_prediction = model_run.add_predictions(
        name="prediction_upload_job"+str(uuid.uuid4()),
        predictions=ndjson_prediction
    )
    # Errors will appear for annotation uploads that failed.
    print("Errors:", upload_job_prediction.errors)
    # Return the chatgpt model name
    return chatgpt_model_name
