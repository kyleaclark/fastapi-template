# FastAPI-Template

- Authored by Kyle Clark - [kyleaclark.com](https://kyleaclark.com)
- Python FastAPI production ready template with Poetry dependency management

___

### App Environment

- Python 3.10.7
- Poetry dependency management
- Setup instructions are specific to macOS. Steps may vary.

#### Setup Prerequisites

1. Install pyenv for python version management - https://github.com/pyenv/pyenv
2. Update pyenv if previously installed e.g. via brew `brew upgrade pyenv`
3. Install poetry for python dependency management - https://python-poetry.org/docs/#installation
4. Update poetry if necessary (optional): `poetry self update`
4. Add pyenv path to profile e.g. add `export PYENV_ROOT="$HOME/.pyenv` + `export PATH="$PYENV_ROOT/bin:$PATH"`
5. Add poetry path to profile e.g. add `export PATH="$HOME/.poetry/bin/:PATH`
6. Install python version: `pyenv install 3.10.7`

#### Python Environment

1. Set python version within the repo directory: `pyenv local 3.10.7`
2. Set the poetry env version of python: `poetry env use ~/.pyenv/versions/3.10.7/bin/python`
3. Install python application dependencies: `poetry install`
   
#### Python Execution

1. Run text game via terminal: `poetry run python main.py`
2. Run tests via terminal: `poetry run python -m pytest -p no:cacheprovider tests`

#### Optional: PyCharm Setup

1. Open PyCharm Preferences
2. Open Project Interpeter > Add existing Virtualenv Environment e.g. `/Users/<username>/Library/Caches/pypoetry/virtualenvs/<poetry-name>/bin/python3`
3. Open Tools > Python Integrated Tools > Default test runner: pytest
4. Run text game: Right-click on `main.py` and choose Run
5. Run tests via pytest: Right-click on `tests` and choose Run

- Note: Steps may vary for different PyCharm versions.

___

### Docker Build

#### Docker Build & Run App

```
docker build --target application -f Dockerfile -t fastapi-template .
docker run --user=appuser -p 8000:8000 --env APP_ENV=DEV fastapi-template
```

#### Docker Build & Run Tests

```
docker build --target testing -f Dockerfile -t fastapi-template-testing .
docker run --user=appuser --env APP_ENV=DEV fastapi-template-testing
```

___

### Poetry Reference

- Poetry documentation - https://python-poetry.org/docs/
- `poetry install` - Install dependencies from poetry.lock - https://python-poetry.org/docs/cli/#install
- `poetry update` - Update poetry.lock from pyproject.toml - https://python-poetry.org/docs/cli/#update
- `poetry add` - Add a dependency into pyproject.toml - https://python-poetry.org/docs/cli/#add
- `poetry remove` - Remove a dependency in pyproject.toml and update poetry.lock - https://python-poetry.org/docs/cli/#remove
