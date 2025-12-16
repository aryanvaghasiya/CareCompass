from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import logging
import os

# Create a logs directory if it doesn't exist
log_dir = '/app/logs' # This will be mounted from the named volume 'app_logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_dir, 'application.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
app = FastAPI()

app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)

# Static files and templates setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Container API URLs
specialty_predictor_url = "http://127.0.0.1:8082/predict"
doctor_recommendation_url = "http://127.0.0.1:8000/recommend/"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage."""
    app_logger.info("Home page accessed.")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, symptoms: str = Form(...)):
    """Process the input symptoms."""
    app_logger.info(f"Processing symptoms: {symptoms}")
    try:
        # Send symptoms to the Specialty Predictor container
        response = requests.post(
            specialty_predictor_url,
            json={"symptoms": symptoms},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        specialty_data = response.json()
        specialties = [spec["speciality"] for spec in specialty_data["top_specialists"]]
        app_logger.info(f"Predicted specialties: {specialties}")

        # Send specialties to the Doctor Recommendation container
        doctor_response = requests.post(
            doctor_recommendation_url,
            json={"specialists": specialties},
            headers={"Content-Type": "application/json"},
        )
        doctor_response.raise_for_status()
        doctor_data = doctor_response.json()["recommendations"]
        app_logger.info(f"Recommended doctors: {doctor_data}")

        return templates.TemplateResponse(
            "results.html",
            {
                "request": request,
                "symptoms": symptoms,
                "specialties": specialties,
                "recommendations": doctor_data,
            },
        )
    except Exception as e:
        app_logger.error(f"Error processing symptoms: {e}", exc_info=True)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(e)},
        )
