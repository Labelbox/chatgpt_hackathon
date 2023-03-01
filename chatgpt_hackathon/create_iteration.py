import labelbox as lb
from chatgpt_hackathon import get_project_with_name, get_model_with_name

def create_iteration(client, team_name, training_round):
    """ Takes data rows from a project and retrieves labels from the source project to create a model run
    """
    # Enforce training round as a string
    training_round = str(training_round)
    # Get source project which contains labels
    source_project = get_project_with_name(client, "goemotions")
    # Get team project with curated data rows
    project = get_project_with_name(client, team_name)
    # Create a model run
    model_run = create_model_run(client, team_name, training_round)
    print(f"Created model run for round {training_round} for team '{team_name}'")
    # Collect data rows from team project, labels from source project
    print(f"Adding labels to model run...")
    data_rows = []
    for batch in project.batches():
        data_rows = [data_row for data_row in batch.export_data_rows()]
    label_ids = [get_label_id_for_data_row_id(client, data_row.uid, source_project.uid)[0] for data_row in data_rows]
    # Enforce training size
    if str(training_round) == "1" and len(label_ids) > 2000:
        raise ValueError(f"Training round 1 limited to 2000 data rows - please reduce the number of data rows in your Project")
    if str(training_round) == "2" and len(label_ids) > 4000:
        raise ValueError(f"Training round 2 limited to 4000 data rows - please reduce the number of data rows in your Project")
    if str(training_round) == "3" and len(label_ids) > 6000:
        raise ValueError(f"Training round 3 limited to 6000 data rows - please reduce the number of data rows in your Project")        
    # Add labels to model run
    model_run.upsert_labels(label_ids)
    print(f"Success: Labels added to model run")
    # Return created model run
    return model_run
    
def create_model_run(client:lb.Client(), team_name:str, training_round:str):
    """ Creates a model run for a given model with a given model name
    """
    # Enforce training round name
    if training_round not in ["1", "2", "3"]:
        raise ValueError(f"Training round must be either 1, 2 or 3")
    # Get model
    model = get_model_with_name(client=client, team_name)
    # Create model run
    model_run = model.create_model_run(name=training_round)
    # Return model run
    return model_run

def get_label_id_for_data_row_id(client:lb.Client, data_row_id:str, project_id:str):
    """ Gets all labels as well as label / review times for a given data row in a given project
    Args:
        client            :   Required (labelbox.Client) - Labelbox Client object
        data_row_id       :   Required (str) - Labelbox data row ID
        project_id        :   Required (str) - Labelbox project ID
    Returns:
        List of label IDs
    """
    gql_query_str = """query get_labels($data_row_id:ID!, $project_id:ID!){project(where:{id:$project_id}){labels(first: 25, where:{dataRow:{id:$data_row_id}}){id}}}"""
    res = client.execute(query=gql_query_str, params={"data_row_id" : data_row_id, "project_id": project_id})['project']['labels']
    label_ids = [x['id'] for x in res]
    return label_ids      
