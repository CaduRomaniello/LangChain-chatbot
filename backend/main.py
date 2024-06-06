from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from modules.appointment_setting.controller import router as appointment_setting_router
from modules.chat.controller import router as chat_router

app = FastAPI(
    title="Appointment-Setting",
    version="V1"
)

app.include_router(appointment_setting_router)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Redirect / -> Swagger-UI documentation
@app.get("/")
def main_function():
    """
    # Redirect
    to documentation (`/docs/`).
    """
    return RedirectResponse(url="/docs/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)