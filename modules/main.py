import uvicorn

from modules.adapter.infrastructure.fastapi.app import app

if __name__ == "__main__":
    uvicorn.run(
        "modules.main:app",
        host=app.extra.get("app_host"),
        port=app.extra.get("app_port"),
        reload=app.extra.get("reload"),
        loop="uvloop",
    )
