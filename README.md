# Django Tree Menu
### Описание
**Django Tree Menu** — проект, в котором при помощи template tag реализовано древовидное меню. Чтобы добавить меню в любой html шаблон, достаточно:
- Прописать `{% load menu %}` в начале файла  
- Добавить template tag `{% draw_menu "menu_name" %}` в любом месте  
Создавать меню, настраивать разделы и указывать ссылки можно в стандартной админке Django.  
Каждое меню требует ровно одного запроса к базе данных  

*Приложение "homepage" добавлено исключительно для демонстрации*
### Стек технологий
- Python
- Django
- Django Debug Toolbar
### Автор
**Имя:** Эмилар Локтев  
**Почта:** emilar-l@yandex.ru  
**Telegram** @itsme_emichka  
### Как запустить проект
1. Клонировать репозиторий:  
   `git clone https://github.com/itsme-emichka/tree_menu_django.git`  
2. Перейти в директорию проекта:  
   `cd tree_menu_django`  
3.  Создать и активировать виртуальное окружение:  
   - Windows — `python -m venv venv`  
     Linux/MacOS — `python3 -m venv venv`  
- Windows — `source venv/Scripts/activate`  
  Linux/MacOS — `source venv/bin/activate`  
4. Поставить зависимости:  
`pip install -r requirements.txt`
5.  Перейти в директорию с файлом `manage.py`:  
   `cd tree_menu`
6. Применить миграции:  
`python manage.py migrate`    
7. Запустить сервер:  
   `python manage.py runserver`