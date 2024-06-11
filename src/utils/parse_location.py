import json




def parseLocation(location:str):
    """
    This function takes the string from the request and converts it to a data object.
    """
    
    
    
    json_data = json.loads(location)
    
    return json_data
    