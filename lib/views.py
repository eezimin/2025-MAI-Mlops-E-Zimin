from aiohttp.web import Response
from aiohttp.web import View

from aiohttp_jinja2 import render_template

from lib.image import image_to_img_src
from lib.image import PolygonDrawer
from lib.image import open_image
import mlflow
import numpy as np

class IndexView(View):
    template = "index.html"
    # обработчики get и post методов в http протоколе
    async def get(self) -> Response:
        # self.template - путь
        # self.template - запрос
        # {} - словарь с переменными (контекст)
        # ctx = {'error': 'Some default error'}
        ctx = {}
        return render_template(self.template, self.request, ctx)
        # from datetime import datetime
        # now = datetime.now()
        # return Response(
        #     text="""
        #         <h1>Всё работает</h1>
        #         <p>теперь загляни в <pre>lib/views.py</pre></p>
        #         <p>{now.isoformat()}</p>
        #     """,
        #     headers={"content-type": "text/html"}, # html документ
        # )


    async def post(self) -> Response:
        try:
            form = await self.request.post()
            # загружаем изображения
            image = open_image(form["image"].file) # name='image' в html
            # вырезаем и обводим в квадрат
            draw = PolygonDrawer(image)
            # готовим модель
            model = self.request.app["model"]
            words = []
            # for coords, word, accuracy in await model.readtext(image):
            for coords, word, accuracy in model.readtext(image):
                draw.highlight_word(coords, word)
                # обрезанное из-е
                cropped_img = draw.crop(coords)
                # бинари передаем plain текстом, чтобы не было ссылки
                cropped_img_b64 = image_to_img_src(cropped_img)
                words.append(
                    {
                        "image": cropped_img_b64,
                        "word": word,
                        "accuracy": accuracy,
                    }
                )
            # возвращает PIL объект картинки
            # а image_to_img_src переводит в текст
            image_b64 = image_to_img_src(draw.get_highlighted_image())
            # заполненный контекст в конце. Это словарь с переменными
            ctx = {"image": image_b64, "words": words}

            # ✅ ЛОГИРОВАНИЕ в MLflow
            with mlflow.start_run():
                mlflow.set_tag("source", "web_form_upload")
                mlflow.log_param("num_words", len(words))
                mlflow.log_param("words", ",".join([w["word"] for w in words]))
                mlflow.log_param("image_size", image.size)

                if words:
                    avg_accuracy = np.mean([w["accuracy"] for w in words])
                    max_accuracy = max([w["accuracy"] for w in words])
                    min_accuracy = min([w["accuracy"] for w in words])

                    mlflow.log_metric("avg_accuracy", avg_accuracy)
                    mlflow.log_metric("max_accuracy", max_accuracy)
                    mlflow.log_metric("min_accuracy", min_accuracy)

                highlighted_image_path = "/tmp/highlighted.png"
                draw.get_highlighted_image().save(highlighted_image_path)
                mlflow.log_artifact(highlighted_image_path)   
                        
        except Exception as err:
            # если ошибка, то возникает error
            ctx = {"error": str(err)}
            # контекст передается в шаблон
        return render_template(self.template, self.request, ctx)
