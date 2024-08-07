# Installation

## Docker Installation

**Short-Hand Command**
Build (if needed) and run the Docker containers in the background:

```bash
docker compose up -d
```

For more control, follow the:

**Step-by-Step Guide**

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

   - Ensure .env file is configured as per [Prerequisites](01-prerequisites.md).

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

## Next Steps

Now, that you have [Prerequisites](01-prerequisites.md) and [Installation](02-installation.md) completed, you can proceed to the [Usage](03-usage.md) guide to access the application and available routes.
