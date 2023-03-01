import labelbox as lb
from labelbox.schema.media_type import MediaType
from labelbox.schema.queue_mode import QueueMode
from chatgpt_hackathon import get_project_with_name

def register_team(client, team_name:str):
    """ Creates a Labelbox Project and Model given a team name
    Args:
        client    :   Required (labelbox.Client) - Labelbox Client object
        team_name :   Required (str) - Desired team name
    Returns:

    """
    ontology_id = "cleovlhqq10hm07wj2b5laj54"
    models = list(client.get_models(where=(lb.Model.name==team_name)))
    if models:
        raise ValueError(f"Project already exists with team name {team_name} - please resolve within the Labelbox UI")    
    projects = list(client.get_projects(where=(lb.Project.name==team_name)))
    if projects:
        raise ValueError(f"Project already exists with team name {team_name} - please resolve within the Labelbox UI")
    model = client.create_model(name=team_name, ontology_id=ontology_id)
    project = client.create_project(name=team_name, media_type=MediaType.Text, queue_mode=QueueMode.Batch)
    project.setup_editor(client.get_ontology("cleovlhqq10hm07wj2b5laj54"))    
    print(f"Team {team_name} has registered a Labelbox Model and Project - good luck!")
