
"""Notification microservice - FastAPI + Eureka."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
import py_eureka_client.eureka_client as eureka_client

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))
EUREKA_URL = os.getenv(
    "EUREKA_URL",
    "http://localhost:8761/eureka"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Enregistrement dans Eureka au démarrage
    print("Connecting NOTIFICATION to Eureka...")

    client = await eureka_client.init_async(
        eureka_server=EUREKA_URL,
        app_name="NOTIFICATION",
        instance_id=f"notification:{PORT}",
        instance_host="127.0.0.1",
        instance_ip="127.0.0.1",
        instance_port=PORT,
        home_page_url=f"http://127.0.0.1:{PORT}/",
        status_page_url=(
            f"http://127.0.0.1:{PORT}"
            "/api/notifications/hello"
        ),
        health_check_url=(
            f"http://127.0.0.1:{PORT}"
            "/api/notifications/hello"
        )
    )

    print(f"NOTIFICATION registered with Eureka on port {PORT}")

    try:
        yield
    finally:
        # Désenregistrement à l'arrêt
        await client.stop()
        print("NOTIFICATION stopped and unregistered from Eureka")


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice "
        "(Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; "
        "the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[
        {
            "url": f"http://localhost:{PORT}",
            "description": "Local"
        }
    ],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(notification.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )
