# Car Clinic API Test Framework

An API testing framework built with python and pytest for testing the backend API for the Car Clinic application.

## Quick start

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt .
```

### Run tests

Default environment is `dev`:

```bash
pytest
```

Run only owner tests

```bash
pytest -m owner
```

Run against a specific environment:

```bash
pytest --env staging
```

Run with HTML report:

```bash
pytest --html=reports/report.html --self-contained-html
```

## Configuration

Environments live in `config/config.yaml`.

Example:

```yaml
environments:
  dev:
    base_url: "https://dev.example.com"
    timeout: 10
    verify_ssl: true
  integration:
    base_url: "https://integration.example.com"
    timeout: 15
    verify_ssl: true
```

## Design notes

- `ApiClient` centralizes HTTP logic.
- fixtures expose config and reusable clients to tests.
- markers make it easy to split test suites in CI/CD.
- contract tests validate the response structure using Pydantic.

## Future Enhancements

- Add tests for authentication and authorization
- Plug into CI/CD pipeline
- Add test data factories
- Add Allure for reporting
