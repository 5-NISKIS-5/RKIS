<!DOCTYPE html>
<html>

<head>
  <title>Классификация ирисов</title>
  <style>
    body {
      font-family: Arial;
      margin: 40px;
    }

    label {
      display: inline-block;
      width: 150px;
    }

    input {
      margin-bottom: 10px;
      padding: 5px;
    }

    button {
      padding: 10px 20px;
      font-size: 16px;
    }
  </style>
</head>

<body>
  <h1>Определение вида ириса</h1>
  <form method="post" action="predict.php">
    <label>Длина чашелистика (cm):</label>
    <input type="number" step="any" name="sepal_length" required><br>

    <label>Ширина чашелистика (cm):</label>
    <input type="number" step="any" name="sepal_width" required><br>

    <label>Длина лепестка (cm):</label>
    <input type="number" step="any" name="petal_length" required><br>

    <label>Ширина лепестка (cm):</label>
    <input type="number" step="any" name="petal_width" required><br>

    <button type="submit">Отправить</button>
  </form>
</body>

</html>