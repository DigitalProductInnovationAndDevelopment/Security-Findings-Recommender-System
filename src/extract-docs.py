import app as app
from fastapi.openapi.docs import get_swagger_ui_html
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output",
        help="Output path for documentation",
        required=False,
        default=os.path.join(os.getcwd(), ".docs"),
    )
    args = parser.parse_args()
    output_path = args.output
    print(f"Generating documentation in {output_path}")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    schema = app.app.openapi()
    with open(os.path.join(output_path, "swagger.json"), "w") as file:
        file.write(schema.__str__())
    html = get_swagger_ui_html(openapi_url="./swagger.json", title="API Documentation")
    with open(os.path.join(output_path, "index.html"), "wb") as file:
        file.write(html.body)
