import json
import jsonschema
from jsonschema import validate

from src.data.types import schema, Response, Content


def validate_json(str: str) -> bool:
    try:
        json_data = json.loads(str)
        try:
            validate(instance=json_data, schema=schema)
            print("JSON data adheres to the schema.")
        except jsonschema.exceptions.ValidationError as e:
            print("JSON data does not adhere to the schema.")
            print(e)
    except ValueError as e:
        return False

    return True


def get_content_list(json_data: Response) -> list[Content]:
    return json_data['message']['content']
