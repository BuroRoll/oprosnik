from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.v1 import auth, users, surveys

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(surveys.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization", "Origin", "Accept"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
