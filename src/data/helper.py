from data.types import Content, InputData

# ##TODO:maybe using pydantic should be enough
# def validate_json(data: any) -> bool:
#     try:
#         json_data = data
#         try:
#             validate(instance=json_data, schema=schema)
#             print("JSON data adheres to the schema.")
#         except jsonschema.exceptions.ValidationError as e:
#             print("JSON data does not adhere to the schema.")
#             print(e)
#     except ValueError as e:
#         return False

#     return True


def get_content_list(json_data: InputData) -> list[Content]:
    return json_data.message.content
