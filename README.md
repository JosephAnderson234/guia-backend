# GUIA BACKEND

This is a backend created for solve an specific project management need. It provides APIs to manage appointments and integrates with Google Calendar for scheduling events.

## Features
- Create appointments with multiple initial dates.
- Automatically schedule recurring events in Google Calendar.
- RESTful API built with FastAPI.
- Data validation using Pydantic.
- Google Calendar integration using Google API Client.
- Environment variable management with python-dotenv.
## Installation
1. Clone the repository:
   ```bash
   git clone [url]
   ```
2. Navigate to the project directory:
   ```bash
    cd GuiAProyect
    ```
3. Create a virtual environment:
   ```bash
    python -m venv .venv
    ```
4. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
5. Install the required packages:
   ```bash
    pip install -r requirements.txt
   ```
6. Set up environment variables:
   - Create a `.env` file in the root directory.
    - Copy the contents of `.env.example` into `.env`.
   - Add the necessary environment variables (e.g., Google API credentials).
7. Run the application:
   ```bash
    uvicorn app.main:app --reload
   ```


> For detailed instructions on setting up Google API credentials, refer to the [Google Calendar API documentation](https://developers.google.com/calendar/api/quickstart/python).