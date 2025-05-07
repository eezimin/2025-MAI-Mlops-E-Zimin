from aiohttp.web import run_app
from lib.app import create_app
from lib.models import create_model
from lib.mlflow_helper import log_service_start, log_model


def main() -> None:
    print("OCR service is starting...")

    log_service_start()
    
    # Создаем модель и логируем её в MLflow
    model = create_model()
    log_model(model)

    app = create_app()
    run_app(app, port=8000)


if __name__ == "__main__":
    main()