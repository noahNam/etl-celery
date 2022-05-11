from http import HTTPStatus

from fastapi.responses import ORJSONResponse

from modules.application.use_case_output import UseCaseFailureOutput


def success_response(result):
    return ORJSONResponse(
        status_code=HTTPStatus.OK,
        content=result,
    )


def failure_response(
    output: UseCaseFailureOutput, status_code: int = HTTPStatus.BAD_REQUEST
):
    return ORJSONResponse(
        status_code=status_code,
        content=output.value,
    )
