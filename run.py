from aiohttp.web import run_app
from lib.app import create_app
from lib.mlflow_helper import log_service_start  # <-- добавили импорт
import datetime

def main() -> None:
    print("OCR service is starting...")

    # Логируем запуск сервиса в MLflow
    log_service_start()

    # Создаем и запускаем приложение
    app = create_app()
    run_app(app, port=8000)
    # Если нужно с хостом:
    # run_app(app, host='0.0.0.0', port=8000)


if __name__ == "__main__":
    main()