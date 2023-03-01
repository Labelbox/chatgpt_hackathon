import labelbox as lb

def get_project_with_name(client:lb.client, project_name:str):
    """ Gets a single project given a project name -- errors out if there are no projects with that name, or if there are more than one
    Args:
        client        :   Required (lb.Client()) - Labelbox Client object
        project_name  :   Required (str) - Labelbox Project Name
    Returns:
        lb.Project() object
    """
    projects = list(client.get_projects(where=(lb.Project.name==project_name)))
    if not projects:
        raise ValueError(f"No projects exist with name {team_name} - please ensure your Project's Name corresponds with a team name - if your team has not created a project yet, please do so")
    elif len(projects)!=1:
        raise ValueError(f"Multiple projects exist with name {team_name} - please resolve this, as each team should have a unique name and only one project each")
    project = projects[0] 
    return project
