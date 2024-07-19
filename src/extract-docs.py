import app as app
from fastapi.openapi.docs import get_swagger_ui_html
import os

if __name__ == "__main__":
    output_path = os.path.join(os.getcwd(), ".docs")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    schema = app.app.openapi()
    with open(os.path.join(output_path, "swagger.json"), "w") as file:
        file.write(schema.__str__())
    html = get_swagger_ui_html(openapi_url="./swagger.json", title="API Documentation")
    with open(os.path.join(output_path, "index.html"), "wb") as file:
        file.write(html.body)
