from fastapi import FastAPI

from routers.v1 import auth, items

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()

app.include_router(auth.router)
app.include_router(items.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
