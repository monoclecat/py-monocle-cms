# A simple content management system for Django

This is the repository for py-monocle-cms, the content management system I use for my homepage, monoclecat.de.
py-monocle-cms is meant for small, multilingual sites that are built as a blog with one user-account being the maintainer, 
having superuser rights. 

## Features

### Easy image upload and automatic thumbnail generation

Upload, tag and add images to your posts in no time using py_monocle_cms's intergalactic time-bending image management system. 
It's as easy as counting to 3! The image upload page also integrates a gallery, allowing you to sort images by tag, upload date 
and unique ID.

### Nicely styled newsfeed on the landing page

The pages you write are directly added to the newsfeed on the front page of your site. Of course there is a checkbox you can click if 
you don't a page to experience the limelight. 

### No html coding required

Write the content of your pages in nice-and-tidy [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), 
which gives you plenty of styling options. Integrating images is easier than you might think! Instead of you needing to 
enter the filepath, you just need to enter the image's unique ID, shown on the image upload page & gallery. Along with that 
you can set the size (small, medium or large). 

Example: `![Text that's shown when the image can't be loaded](4 small "Here's a cat!")`

Gives you: 

![Text that's shown when the image can't be loaded](https://github.com/monoclecat/py_monocle_cms/media/image/d20458f78f0640018a9df13fcd0ffea2.medium.jpg)
_Here's a cat!_

* Easy image upload and automatic thumbnail generation
* The landing page lists the content of all pages like a blog
* The content of pages is written in [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), 
no html required!

## Installation

This short guide covers the installation from scratch. If you want to embed the app into your existing project, 
I believe you are knowledgeable enough to leave out the steps aimed at configuring newly created projects. 

_Note: I use Python 3 for installation of the cms and beyond. You will encounter strange errors if you begin a command line 
with "python" instead of "python3". In the Django tutorial and in other places you might find a command beginning with "python". To execute the command
in Python3, just make it a "python3"._

1. If you haven't done so yet, create a new django project, as described 
[in Django Tutorial 01](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)
To save you the click: `cd` to your desired directory and create a project with the command 
`django-admin startproject mysite`. Run `python3 manage.py migrate` to initialize the project. 

2. Jump into the newly created directory with `cd mysite/` and clone the py-monocle-cms app into the newly created 
project by running `git clone https://github.com/monoclecat/py_monocle_cms.git`.

3.  Next, open `mysite/settings.py`.

    Add the following to the list of `INSTALLED_APPS`:
    
    ```
    'py_monocle_cms.apps.PyMonocleCmsConfig',
    'bootstrap3',
    'markdown',
    'crispy_forms',
    ```
    
    In `TEMPLATES`, change `DIRS: [],` to `DIRS: [os.path.join(BASE_DIR, 'templates')],` and add 
    `'django.template.context_processors.media'` to the `context_processors` element of `OPTIONS`.
    
    Append the following lines to settings.py:

    ```
    STATICFILES_DIRS = ["py_monocle_cms/static",]
    STATIC_ROOT = 'static'
    MEDIA_ROOT = 'py_monocle_cms/media'
    MEDIA_URL = '/py_monocle_cms/media/'
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    ```
    
4.  In `mysite/urls.py`, change 

    ```
    from django.conf.urls import url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
    ]
    ```
    
    to 
    
    ```
    from django.conf.urls import url, include
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^', include('py_monocle_cms.urls')),
    ]
    ```
    
In your terminal, change to the root directory of your Django project and run `python3 managy.py runserver`. 
The app should run as desired and when visiting the address `127.0.0.1:8000` in your browser, you should see 
the an empty webpage. If this is the case, congratulations! You are almost ready to fill your site with content. 

The last step is to create a super-user, will you will use to log in to your site and modify it. 
To create a super-user, execute the command `python manage.py createsuperuser`. 
Enter username, email and password and you're ready to go. Now you can not only log into the admin part of your webpage 
under `http://127.0.0.1:8000/login/`, you can also access the database tables and users under `http://127.0.0.1:8000/admin/`.
It is very important that you keep these login credentials secret!
