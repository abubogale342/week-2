# Project Name

A brief description of your project.

## Project Structure

```
.
├── .vscode/               # VS Code settings
│   └── settings.json
├── .github/               # GitHub configurations
│   └── workflows/
│       └── unittests.yml  # CI/CD pipeline configuration
├── src/                   # Source code
│   └── __init__.py
├── notebooks/             # Jupyter notebooks
│   ├── __init__.py
│   └── README.md
├── tests/                 # Test files
│   └── __init__.py
├── scripts/               # Utility scripts
│   └── __init__.py
├── .gitignore
├── requirements.txt       # Project dependencies
└── README.md
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

```bash
pytest tests/
```

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details. week-2
