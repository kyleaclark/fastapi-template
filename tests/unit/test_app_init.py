from fastapi import FastAPI

from app.config.app_init import create_app


def test_create_app():
    result = create_app()
    assert isinstance(result, FastAPI)
