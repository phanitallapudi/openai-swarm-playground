# OpenAI Swarm Playground

This is a demo implementation to test the capabilities of OpenAI's FastAPI application.

## Features

- FastAPI framework for building APIs quickly.
- Simple and easy-to-follow demo.
- Built to explore and experiment with OpenAI-powered functionalities.

---

## Requirements

Ensure you have the following installed on your system:

- **Python 3.10 or later**
- **pip** (Python package manager)
- **Git** (optional, for cloning the repository)

---

## Installation

Follow these steps to set up and run the project:

1. **Clone the Repository** (optional):

    ```bash
    git clone https://github.com/phanitallapudi/openai-swarm-playground.git
    cd openai-swarm-playground
    ```

2. **Install Python Dependencies**:

    It is recommended to create a virtual environment for the project:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

    Then install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Environment Variables**:

    Create a `.env` file in the root directory and set the necessary variables:

    Use .env.example for reference

4. **Run the Application**:

    Use the following command to start the FastAPI server:

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

    This will start the server on `http://127.0.0.1:8000`.

---

## Usage

Once the server is running, you can:

1. Visit the **Swagger UI** for API documentation and testing at:

    ```
    http://127.0.0.1:8000/docs
    ```

2. Visit the **ReDoc** documentation at:

    ```
    http://127.0.0.1:8000/redoc
    ```

3. Access your endpoints directly via any API client like `Postman`, `cURL`, or through your browser.

---
