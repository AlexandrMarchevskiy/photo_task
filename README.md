# Фотоальбом API


<h4>Регистрация пользователя с получением токена: </h4>
http://localhost:8000/api/v1/signup

{
  "username": "test",
  "password": "test"
}

<h4>Вход по имени и паролю: </h4>
http://localhost:8000/api/v1/login

<hr>
<h4>Вывод списка альбомов принадлежащих пользователю: </h4>

http://localhost:8000/api/v1/albums   

<h4>Вывод отдельного альбома : </h4>
http://localhost:8000/api/v1/albums/{id}

<h4>Изменение доступных полей альбома | удаление альбома: </h4>
http://localhost:8000/api/v1/albums/{id}/edit

<h4>Создать новый альбом : </h4>
http://localhost:8000/api/v1/albums/create

<hr>

<h4>Загрузить фото в альбом : </h4>
http://localhost:8000/api/v1/albums/photo/upload

<h4>Изменение полей фото | удаление фото : </h4>
http://localhost:8000/api/v1/albums/photo/{id}

<h4>Получение списка фото принадлежащих пользователю: </h4>
http://localhost:8000/api/v1/albums/photo

<hr>

<h3>Документация</h3>

http://localhost:8000/swagger/
http://localhost:8000/redoc/