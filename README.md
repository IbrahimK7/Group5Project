# Demo Flask App

This is a simple Flask application that provides a "Hello World" API endpoint.

## Project Structure

```
demo-flask-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   └── config.py
├── tests
│   └── test_hello.py
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd demo-flask-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the Flask application, execute the following command:

```
python run.py
```

The application will be available at `http://127.0.0.1:5000/api/hello`.

## Usage

You can access the "Hello World" endpoint by navigating to:

```
http://127.0.0.1:5000/api/hello
```

This will return a JSON response:

```json
{"message": "Hello from Flask!"}
```

## Running Tests

To run the unit tests for the application, use the following command:

```
pytest
```

## License

This project is licensed under the MIT License.