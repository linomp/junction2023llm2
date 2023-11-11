# Junction2023 LLm project

## Run the backend

1. Crate an .env file based on the .env.template file
2. Add open AI key to the .env file
3. On Linux run:
    ```bash
    source venv/bin/activate
    pip3 install -r requirements.txt
    python3 api/main.py
    ```

Server will run on port 8000, visit http://localhost:8000/docs