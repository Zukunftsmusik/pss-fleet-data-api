from unittest import mock

import pytest
from fastapi.exceptions import RequestValidationError

from src.api.exception_handlers import handle_request_validation
from src.api.models.exceptions import ServerError


async def test_handle_request_validation_raises_server_error_on_onhandled_validation_error():
    @mock.patch("src.api.exception_handlers._raise_body_parameter_error")
    def _raise_body_parameter_error(*args, **kwargs):
        pass

    @mock.patch("src.api.exception_handlers._raise_header_parameter_error")
    def _raise_header_parameter_error(*args, **kwargs):
        pass

    @mock.patch("src.api.exception_handlers._raise_path_parameter_error")
    def _raise_path_parameter_error(*args, **kwargs):
        pass

    @mock.patch("src.api.exception_handlers._raise_query_parameter_error")
    def _raise_query_parameter_error(*args, **kwargs):
        pass

    error = {
        "type": "",
        "loc": ("somewhere", "abcxyz"),
        "msg": "",
        "input": None,
    }
    exc = RequestValidationError([error])

    with pytest.raises(ServerError):
        await handle_request_validation(None, exc)
