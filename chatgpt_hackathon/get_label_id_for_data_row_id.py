import labelbox as lb

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
