# Basic health check.
# If you really want to be a nerd about this:
# https://datatracker.ietf.org/doc/html/draft-inadarei-api-health-check-00
import secrets
from importlib import metadata

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/health", tags=["health"])
security = HTTPBasic()

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    __version__ = "develop"
finally:
    del metadata


@router.get("/")
async def health_check(
    fail: bool = False, credentials: HTTPBasicCredentials = Depends(security)  # noqa
):
    # If you think "Why so complicated just to check if two strings are identical?", the answer is:
    # to avoid timing attacks. If done this way a successful check and a failed check will always
    # take the same amount of time. If done "naively" the negative check would short circuit and we
    # could see a significant timing difference between an incorrect username and an incorrect
    # password, allowing us to find valid usernames by brute forcing.
    # see
    # https://fastapi.tiangolo.com/advanced/security/http-basic-auth/?h=basic+auth#check-the-username
    # and https://docs.python.org/3/library/secrets.html#secrets.compare_digest
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"health"
    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"checkpw"
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    if not fail:
        return {
            "version": __version__,
            "request_processor_up": True,
            "database_connection_ok": True,
            "external_api_reachable": True,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "request_processor_up": True,
                "database_connection_ok": False,
                "external_api_reachable": True,
            },
        )
