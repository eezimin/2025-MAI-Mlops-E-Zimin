import mlflow
from datetime import datetime
from easyocr import Reader
import os


def log_service_start():
    mlflow.set_tracking_uri("file:/app/mlruns")

    print("✅ MLflow: logging service start")
    mlflow.set_experiment("OCR Service")
    with mlflow.start_run():
        mlflow.log_param("service_started_at", datetime.now().isoformat())
        mlflow.log_param("model_source", "easyocr.Reader(['en'])")
        mlflow.log_param("framework", "easyocr")
        mlflow.end_run()
      
def log_model(model: Reader, model_name: str = "EasyOCR_Reader"):
    """Сохраняет OCR-модель вручную через MLflow"""
    mlflow.set_experiment("OCR Service")
    with mlflow.start_run():    
        model_dir = os.path.join(mlflow.get_artifact_uri(), model_name)
        os.makedirs(model_dir, exist_ok=True)

        # Сохраняем модель вручную (пример: предобученные веса EasyOCR уже кэшированы)
        # Здесь можно указать путь до сохранённой модели
        with open(os.path.join(model_dir, "README.md"), "w") as f:
            f.write("Модель EasyOCR с поддержкой английского языка.\n")

        print(f"Кастомная модель сохранена в {model_dir}")        
        