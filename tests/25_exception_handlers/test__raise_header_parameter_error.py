import pytest
from fastapi.exceptions import RequestValidationError

from src.api.exception_handlers import _raise_header_parameter_error
from src.api.models.error import RequestValidationErrorOut
from src.api.models.exceptions import ServerError


def test__raise_header_parameter_error():
    exc = RequestValidationError(
        [
            {
                "type": "missing",
                "loc": ("header", "Random"),
                "msg": "Field required",
                "input": None,
            }
        ]
    )
    error = RequestValidationErrorOut(**exc._errors[0])
    with pytest.raises(ServerError):
        _raise_header_parameter_error(error, exc)
