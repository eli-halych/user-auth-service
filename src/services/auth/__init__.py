from typing import Optional

from fastapi import FastAPI, Header, Response
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

app = FastAPI()

@app.post("/create/")
def login() -> Response:
    pass

@app.post("/login/")
def login(
   authorization: Optional[str] = Header(None)
) -> Response:
    if not authorization == "":
        return Response(status_code=HTTP_401_UNAUTHORIZED)
    return Response(status_code=HTTP_200_OK)

@app.post("/update/")
def login(
   authorization: Optional[str] = Header(None)
) -> Response:
    pass

@app.post("/remove/")
def login(
   authorization: Optional[str] = Header(None)
) -> Response:
    pass

