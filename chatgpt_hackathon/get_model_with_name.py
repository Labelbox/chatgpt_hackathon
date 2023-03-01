import labelbox as lb

def get_model_with_name(client:lb.client, model_name:str):
    """ Gets a single project given a project name -- errors out if there are no projects with that name, or if there are more than one
    Args:
        client        :   Required (lb.Client()) - Labelbox Client object
        model_name    :   Required (str) - Labelbox Model Name
    Returns:
        lb.Model() object
    """
    models = list(client.get_models(where=(lb.Model.name==model_name)))
    if not models:
        raise ValueError(f"No models exist with name {team_name} - please ensure your Model's Name corresponds with a team name - if your team has not created a model yet, please do so")
    elif len(models)!=1:
        raise ValueError(f"Multiple models exist with name {team_name} - please resolve this, as each team should have a unique name and only one model each")
    model = models[0] 
    return project
