from unittest import mock

import pytest
from fastapi.exceptions import RequestValidationError

from src.api.exception_handlers import _raise_body_parameter_error
from src.api.models.error import RequestValidationErrorOut
from src.api.models.exceptions import ServerError


def test__raise_body_parameter_error_raises_server_error_on_onhandled_validation_error():
    @mock.patch("src.api.exception_handlers._raise_nested_body_parameter_error")
    def _raise_nested_body_parameter_error(*args, **kwargs):
        pass

    @mock.patch("src.api.exception_handlers._raise_non_nested_body_parameter_error")
    def _raise_non_nested_body_parameter_error(*args, **kwargs):
        pass

    error = {
        "type": "",
        "loc": ("body", "abcxyz"),
        "msg": "",
        "input": None,
    }
    exc = RequestValidationError([error])
    raised_error = RequestValidationErrorOut(**error)

    with pytest.raises(ServerError):
        _raise_body_parameter_error(raised_error, exc)
