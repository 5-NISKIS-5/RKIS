<?php
// predict.php - получает данные из формы, отправляет их в FastAPI и отображает результат

// Проверяем, что запрос был отправлен методом POST (безопасность)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // Извлекаем значения из массива $_POST (приходят из формы)
  $sepal_length = $_POST['sepal_length'];
  $sepal_width  = $_POST['sepal_width'];
  $petal_length = $_POST['petal_length'];
  $petal_width  = $_POST['petal_width'];

  // URL, по которому доступен FastAPI (должен быть запущен)
  $url = 'http://127.0.0.1:8000/predict';

  // Формируем строку запроса в формате application/x-www-form-urlencoded
  // http_build_query преобразует массив в строку вида "ключ=значение&..."
  $data = http_build_query([
    'sepal_length' => $sepal_length,
    'sepal_width'  => $sepal_width,
    'petal_length' => $petal_length,
    'petal_width'  => $petal_width
  ]);

  // Настройки контекста для HTTP-запроса
  $options = [
    'http' => [
      'header'  => "Content-type: application/x-www-form-urlencoded\r\n", // заголовок, указывающий тип данных
      'method'  => 'POST',                                                 // метод запроса
      'content' => $data,                                                  // тело запроса
      'timeout' => 10                                                      // таймаут ожидания ответа (сек)
    ]
  ];

  // Создаём контекст потока
  $context = stream_context_create($options);

  // Выполняем POST-запрос к FastAPI и получаем ответ
  $result = file_get_contents($url, false, $context);

  // Проверяем, не произошла ли ошибка при запросе
  if ($result === FALSE) {
    // Получаем информацию о последней ошибке
    $error = error_get_last();
    echo "<h2>Ошибка при обращении к сервису предсказания:</h2>";
    echo "<p>" . htmlspecialchars($error['message']) . "</p>";
    echo '<a href="index.php">Назад</a>';
    exit;
  }

  // Декодируем JSON-ответ от FastAPI в ассоциативный массив
  $response = json_decode($result, true);
  // Извлекаем предсказание (если ключа нет, подставляем 'неизвестно')
  $prediction = $response['prediction'] ?? 'неизвестно';
}
?>
<!-- HTML-часть для отображения результата -->
<!DOCTYPE html>
<html>

<head>
  <title>Результат</title>
</head>

<body>
  <h1>Результат классификации</h1>
  <p>Введённые параметры:</p>
  <ul>
    <li>Sepal length: <?php echo htmlspecialchars($sepal_length); ?> cm</li>
    <li>Sepal width: <?php echo htmlspecialchars($sepal_width); ?> cm</li>
    <li>Petal length: <?php echo htmlspecialchars($petal_length); ?> cm</li>
    <li>Petal width: <?php echo htmlspecialchars($petal_width); ?> cm</li>
  </ul>
  <h2>Предсказанный вид: <?php echo htmlspecialchars($prediction); ?></h2>
  <a href="index.php">Новое предсказание</a>
</body>

</html>