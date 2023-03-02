import labelbox as lb

def get_model_run(client:lb.Client, model_name:str, training_round):
    """ For a given model, iterates through names to get the right model run
    """
    model = get_model_with_name(client, model_name)
    found_model_run = False
    for model_run in model.model_runs():
        if model_run.name == str(training_round):
            found_model_run = True
            break
    if not found_model_run:
        raise ValueError(f"No model run for team name {model_name} with run name {training_round}")    
    return model_run

def get_model_with_name(client:lb.Client, model_name:str):
    """ Gets a single model given a model name -- errors out if there are no models with that name, or if there are more than one
    """
    models = list(client.get_models(where=(lb.Model.name==model_name)))
    if not models:
        raise ValueError(f"No models exist with name {model_name} - please ensure your Model's Name corresponds with a team name - if your team has not created a model yet, please do so")
    elif len(models)!=1:
        raise ValueError(f"Multiple models exist with name {model_name} - please resolve this, as each team should have a unique name and only one model each")
    model = models[0] 
    return model  
  
def get_project_with_name(client:lb.Client, project_name:str):
    """ Gets a single project given a project name -- errors out if there are no projects with that name, or if there are more than one
    """
    projects = list(client.get_projects(where=(lb.Project.name==project_name)))
    if not projects:
        raise ValueError(f"No projects exist with name {project_name} - please ensure your Project's Name corresponds with a team name - if your team has not created a project yet, please do so")
    elif len(projects)!=1:
        raise ValueError(f"Multiple projects exist with name {project_name} - please resolve this, as each team should have a unique name and only one project each")
    project = projects[0] 
    return project

  
