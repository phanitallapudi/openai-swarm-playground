from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.logging_middleware import LoggingMiddleware

from app.routes.swarm_route import router as swarm_route

app = FastAPI(
    title="Swarm Playground",
    swagger_ui_parameters={"syntaxHighlight": False}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(swarm_route, prefix="/api", tags=["Swarm Agent"])

@app.get("/")
async def root():
    return FileResponse("app/client/build/index.html")

@app.exception_handler(404)
async def exception_404_handler(request, exc):
    return FileResponse("app/client/build/index.html")

app.mount("/", StaticFiles(directory="app/client/build/"), name="ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)