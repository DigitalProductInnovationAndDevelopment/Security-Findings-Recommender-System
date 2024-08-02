# Installation

## Docker Installation

1. **Build Docker Images:**
    ```bash
    docker compose build
    ```

2. **Run Docker Containers:**
    ```bash
    docker compose up
    ```

    - Add the -d flag to run containers in the background:
    ```bash
    docker compose up -d
    ```

## Local Development Installation

1. **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set Up Environment Variables:**
    - Ensure .env file is configured as per [Prerequisites](prerequisites.md).

3. **Install Dependencies:**
    ```bash
    pipenv install
    ```

4. **Run the Application:**
    - Activate the virtual environment:
    ```bash
    pipenv shell
    ```

    - Start the application:
    ```bash
    python src/app.py
    ```

## Post-Installatio

- Ensure all services are running.
- Verify installation by accessing the API and Dashboard.
- For more detailed setup instructions, please refer to the [Usage](usage.md) guide.

