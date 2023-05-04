import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import ExceptionMiddleware
from starlette.middleware.cors import CORSMiddleware
from supertokens_python import (InputAppInfo, SupertokensConfig, get_all_cors_headers, init)
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python.recipe import session, thirdpartyemailpassword, emailpassword
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.thirdpartyemailpassword import (Apple, Discord, Github, Google, GoogleWorkspaces)
import os

app = FastAPI(debug=True)
app.add_middleware(get_middleware())

init(
    supertokens_config=SupertokensConfig(
        connection_uri='http://second-light-supertokens-core:3567'
    ),
    app_info=InputAppInfo(
        app_name='Supertokens',
        api_domain='http://localhost:5002',
        website_domain='http://localhost:8080',
        api_base_path='/auth'
    ),
    framework='fastapi',
    recipe_list=[
        session.init(),
        thirdpartyemailpassword.init(
            providers=[
                Google(
                    client_id=os.getenv('GOOGLE_CLIENT_ID'),
                    client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
                ),
                Github(
                    client_id=os.getenv('GITHUB_CLIENT_ID'),
                    client_secret=os.getenv('GITHUB_CLIENT_SECRET')
                )
            ]
        )
    ],
    telemetry=False
)

app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)

@app.get('/sessioninfo')
async def get_session_info(session_: SessionContainer = Depends(verify_session())):
    return JSONResponse({
        'sessionHandle': session_.get_handle(),
        'userId': session_.get_user_id(),
        'accessTokenPayload': session_.get_access_token_payload(),
    })


@app.get("/")
async def hello():
    return {"message": "Hello, world!"}


@app.exception_handler(405)
def f_405(_, __: Exception):
    return PlainTextResponse('', status_code=404)


app = CORSMiddleware(  # type: ignore
    app=app,
    allow_origins=[
        'http://localhost:8080',
        'http://localhost:3567',
        'http://localhost:5002',
        'http://localhost:3000',
    ],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)  # type: ignore
