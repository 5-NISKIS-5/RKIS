import numpy as np
from fastapi import FastAPI, Form                 # Form для получения данных из POST-запроса
from tensorflow.keras.models import load_model    # для загрузки сохранённой модели

# Создаём экземпляр FastAPI
app = FastAPI()

# Загружаем предварительно обученную модель из файла .h5
# Модель должна лежать в папке model относительно этого файла
model = load_model('model/iris_model.h5')

# Список названий классов в том же порядке, в котором модель выдаёт вероятности
# (порядок соответствует one-hot кодировке при обучении)
class_names = ['setosa', 'versicolor', 'virginica']

# Эндпоинт для предсказания. Он принимает POST-запросы с параметрами формы.
@app.post("/predict")
async def predict(
    sepal_length: float = Form(...),   # обязательное поле формы (длина чашелистика)
    sepal_width: float = Form(...),    # ширина чашелистика
    petal_length: float = Form(...),   # длина лепестка
    petal_width: float = Form(...)     # ширина лепестка
):
    """
    Получает четыре параметра цветка, передаёт их в модель Keras,
    возвращает JSON с ключом 'prediction', содержащим название вида.
    """
    # Преобразуем полученные значения в массив numpy формы (1, 4) — одна строка, 4 признака
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    
    # Выполняем предсказание. model.predict возвращает массив вероятностей для каждого класса.
    # Для одного примера берём первый (и единственный) элемент — probabilities[0].
    probabilities = model.predict(input_data)[0]
    
    # Определяем индекс класса с максимальной вероятностью
    predicted_class = np.argmax(probabilities)
    
    # Получаем название класса по индексу
    predicted_name = class_names[predicted_class]
    
    # Возвращаем результат в виде JSON-объекта
    return {"prediction": predicted_name}