import mlflow
from datetime import datetime

def log_service_start():
    mlflow.set_tracking_uri("file:/app/mlruns")

    print("✅ MLflow: logging service start")
    mlflow.set_experiment("OCR Service")
    with mlflow.start_run():
        mlflow.log_param("service_started_at", datetime.now().isoformat())
        mlflow.log_param("model_source", "easyocr.Reader(['en'])")
        mlflow.log_param("framework", "easyocr")
        mlflow.end_run()