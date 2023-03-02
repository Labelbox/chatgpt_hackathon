from chatgpt_hackathon import get_model_with_name

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
