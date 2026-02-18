import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Загружаем датасет Iris из библиотеки sklearn
iris = load_iris()
X = iris.data                # признаки: (длина/ширина чашелистика и лепестка)
y = iris.target.reshape(-1, 1)  # целевая переменная: 0, 1, 2 (виды)

# Преобразуем метки классов в формат one-hot encoding 

encoder = OneHotEncoder(sparse_output=False)
y_cat = encoder.fit_transform(y)

# Разделяем данные на обучающую и тестовую выборки (80% / 20%)
#    random_state фиксирует случайное разбиение для воспроизводимости
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42)

# Создаём простую полносвязную нейросеть:
#    - Входной слой: 4 нейрона (по числу признаков), неявно задаётся через input_shape
#    - Два скрытых слоя по 10 нейронов с активацией ReLU
#    - Выходной слой: 3 нейрона с функцией активации softmax (вероятности классов)
model = Sequential([
    Dense(10, activation='relu', input_shape=(4,)),
    Dense(10, activation='relu'),
    Dense(3, activation='softmax')
])

# Компилируем модель: оптимизатор Adam, функция потерь категориальная кросс-энтропия,
#    метрика качества — точность (accuracy)
model.compile(optimizer=Adam(0.01),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Обучаем модель на тренировочных данных (50 эпох, размер пакета 8)
#    verbose=0 подавляет вывод процесса обучения (чтобы не засорять консоль)
model.fit(X_train, y_train, epochs=50, batch_size=8, verbose=0)

# Оцениваем качество обученной модели на тестовых данных и выводим точность
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy: {acc:.2f}')

# Сохраняем модель в файл iris_model.h5 внутри папки model
#    Папка model должна существовать или быть создана заранее
model.save('model/iris_model.h5')