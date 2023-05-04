from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, widget
from supertokens_python import InputAppInfo, SupertokensConfig, init
from supertokens_python.recipe import session
from supertokens_python.framework.fastapi import get_middleware as supertokens_middleware

app = FastAPI()
app.include_router(user.router)
app.include_router(widget.router)

init(
    supertokens_config=SupertokensConfig(connection_uri='http://second-light-supertokens-core:3567'),
    app_info=InputAppInfo(
        app_name='Supertokens',
        api_domain='http://localhost:5002',
        website_domain='http://localhost:8080',
        api_base_path='/auth'
    ),
    framework='fastapi',
    recipe_list=[session.init()],
    telemetry=False
)

app.add_middleware(supertokens_middleware())
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5002)
