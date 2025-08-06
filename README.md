# Backend-приложение – собственная система аутентификации и авторизации.

## Стэк и зависимости.

Для разработки приложения используется Python версии 12 и выше. В контейнере - python:3.12.3-bookworm

Приложение разрабатывается с FastApi, SQLAlchemy ORM, PostgreSQL.

Все зависимости указаны в pyproject.toml.


## Окружение

Перед клонированием приложения необходимо локально создать виртуальное окружение.

После клонирования проверить и по необходимости внести в .gitignore название папки окружения.

Убедиться, что в .gitignore внесены .env и certs/.

В корне проекта создать папку .env c переменными окружения по образцу файла .env.template.

В корне проекта создать папку certs/ и перейти в папку. Выполнить команды bash:

               mkdir certs && cd certs
               openssl genrsa -out jwt-private.pem 2048
               openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
Убедитесь, что ключи - серые - не подсвечены, как и .env.


## Техническое задание

**Необходимо реализовать backend-приложение – собственную систему аутентификации и авторизации.**

### Логика

Предусмотрена регистрация пользователя.

Пользователь авторизуется по email и хэшированному паролю, создаются access и refresh jwt-токены со сроками жизни.

Авторизованный пользователь может просматривать свой профиль, разлогиниться и удалить (мягко is_active = False) свой профиль.

Пользователь может выполнять действия в соответствии с назначенной ролью и правами на действие.

Данная система реализована созданием соответствующих связанных моделей в базе данных.

Для демонстрации использована mosk-модель Order - в виде словаря.

При создании приложения создается супер-пользователь superuser с action - main. Он имеет право на создание и распределение ролей, ресурсов и прав.


## Примеры реализации

**Регистрация**

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5db856cb-8800-4d3f-9e57-0d0bd85fef5c" />

**Авторизация**

Возможна через эндпоинт и через форму.

Эндпоинт:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3ca929f1-3a4d-40aa-8825-2e066aad7b09" />

Форма:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8735f122-5d38-4bea-88a7-06d92b593951" />

После аторизации получает свой профиль.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9c7a450c-123c-4fdc-bf89-b7a01642f6fb" />

Обновляет любое поле профиля

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bc14f091-b2cf-4a4a-9c0c-32314f2969ca" />
Обновим 2 поля.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6b20e875-da33-40bd-be9c-145de5dbc27a" />

Мягко удаляет профиль

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d67446e5-87f7-420f-8a71-58bcd657e843" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/16bcaf4b-904a-4fc7-896c-07305dda1cac" />

Теперь, в базе данных он неактивирован (последний в списке)

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0738ee3b-da6b-4e2c-bb99-0ac3a760c35c" />


После удаления он уже  получит ошибку

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/367c70e8-f0e2-423a-8751-42695585b378" />


Любой пользователь без авторизации получит ошибку:

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6aa961b7-1dcf-4cc2-8fb0-1f6c932dac15" />

**Роли и права.**

#### Администратор, после авторизации может:

Создавать, удалять и просматривать роли;

<img width="1920" height="798" alt="image" src="https://github.com/user-attachments/assets/4875ed58-825c-48a6-97e4-ac1cf1a593c8" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ba290c8a-8ba9-41b2-b312-c5d1fc471f61" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c452462f-0cb3-45eb-bf1f-64fe3149744f" />

Создавать, удалять и просматривать ресурсы;

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5cc4fd95-26b8-41bf-8886-62c5c7be2f84" />

Создавать, удалять и просматривать разрешения;

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/16468997-a523-455a-836d-13388f87cfa8" />

Создает связи ролей и разрешений;

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b117ffd9-8cae-4667-8a24-dde71ee3d1d7" />

Создает связи пользователей и ролей.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cac1875d-66df-4795-8374-99ed8ee72fee" />

**При дальнейшей разработке необходимо добавить обновление и удаление этих связей**


### Действия пользователей по ролям.

##### Авторизуем пользователя с правом создания заказов. И создадим заказ.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/3c6d9cd0-64a9-4cd9-8b1e-72f151c2ae5a" />

Но другие действия ему не доступны, например посмотреть заказы.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/6c279cff-ecda-45cb-9ea4-5a040386bf58" />

##### Авторизуем пользователя с правом просмотра заказов.

У него получилось посмотреть заказы.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1ca98129-d1ff-4cc9-ad9e-81dd365ed07c" />

Но он не может создавать или удалять.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bf4b47c5-f7f9-4681-b14f-dab4c809feb5" />

#### Дадим имеющему право читать и право удаления.

Для этого авторизуем администратора.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c4ee4ad6-70d5-4d35-8d25-c656c4b9dd03" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bd97ee49-983b-42bf-aa81-d68a120bba3c" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0b767e9d-9bf2-4214-b1e7-d31d43939cf6" />

Теперь, авторизуем этого пользователя , удалим последний заказ и проверим спписок заказов.
