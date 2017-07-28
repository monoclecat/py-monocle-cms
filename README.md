# A simple content management system for Django

This is the repository for py-monocle-cms, the content management system I use for my homepage, monoclecat.de.
py-monocle-cms is meant for small, multilingual sites that are built as a blog with one user-account being the maintainer, 
having superuser rights. 

# Features

## Easy image upload and automatic thumbnail generation

Upload, tag and add images to your posts in no time using py_monocle_cms's intergalactic time-bending image management system. 
It's as easy as counting to 3! The image upload page also integrates a gallery, allowing you to sort images by tag, upload date 
and unique ID.

## Nicely styled newsfeed on the landing page

The pages you write are directly added to the newsfeed on the front page of your site. Of course there is a checkbox you can click if 
you don't a page to experience the limelight. 

## No html coding required

Write the content of your pages in nice-and-tidy [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), 
which gives you plenty of styling options. Integrating images is easier than you might think! Instead of you needing to 
enter the filepath, you just need to enter the image's unique ID (in the example it is 4), shown on the image upload page & gallery. Along with that 
you can set the size (small, medium or large). 

Example: `![Text that's shown when the image can't be loaded](4 small "Here's a cat!")`

Gives you something like this, just with the image and text centered in the page: 

![Text that's shown when the image can't be loaded](https://raw.githubusercontent.com/monoclecat/py_monocle_cms/master/media/cat.jpg)

_Here's a cat!_

#### Multiple images in a row

If you want to display multiple images in a row, do not leave a blank line between the image includes like so:

```
![Text](ID SIZE "Description")
![Text](ID SIZE "Description")
![Text](ID SIZE "Description")
```

_Please note that none of the descriptions will be displayed_

__If you want the images to stand for themselves and each have their descriptions below them, add a blank line between the 
image includes.__


## All modifiable 

In the source I added comments and explanations to some of the more sophisticated functions. I encourage you to adapt the 
code to your needs, modify the templates and report any bugs you find to: contact@monoclecat.de

# Installation

This short guide covers the installation from scratch. If you want to embed the app into your existing project, 
I believe you are knowledgeable enough to leave out the steps aimed at configuring newly created projects. 

_Note: I use Python 3 for installation of the cms and beyond. You will encounter strange errors if you begin a command line with "python" instead of "python3". In the Django tutorial and in other places you might find a command beginning with "python". To execute the command in Python3, just make it a "python3"._

1. If you haven't done so yet, create a new django project, as described 
[in Django Tutorial 01](https://docs.djangoproject.com/en/1.11/intro/tutorial01/). 
To save you the click: Switch to your desired root directory in a terminal and create a project with the command 
`django-admin startproject mysite`. Enter the newly created directory and run `python3 manage.py migrate` to initialize the project. 

2. Download the py_monocle_cms app like so: `django-admin startapp --template=https://github.com/monoclecat/py_monocle_cms/archive/master.zip py_monocle_cms`.

    _If you get an error saying "certificate verify failed", you need to install the certificates by running `/Applications/Python\ 3.6/Install\ Certificates.command`. Now delete the empty py_monocle_cms folder and repeat the step._ 
    
    Downloading the zip-archive of py_monocle_cms removes the .git directory so it's not not a git repository anymore. 
    If you want to make commits, you will need to re-init the repository and sync it: 
    
    ```
    git init
    git remote add origin https://github.com/monoclecat/py_monocle_cms.git
    git fetch
    git reset origin/master
    ```

3.  Next, open `mysite/settings.py`. Add the following to the list of `INSTALLED_APPS`: 

    _Note: You might get an error saying that the packages mentioned below are missing. In this case you must install them first: `pip3 install APPNAME`_.
    
    ```
    'py_monocle_cms.apps.PyMonocleCmsConfig',
    'bootstrap3',
    'markdown',
    'crispy_forms',
    ```
    
    In `TEMPLATES`, change `'DIRS': [],` to `'DIRS': [os.path.join(BASE_DIR, 'templates')],` and add 
    `'django.template.context_processors.media'` to the `context_processors` element of `OPTIONS`.
    
    Append the following lines to settings.py:

    ```
    STATICFILES_DIRS = ["py_monocle_cms/static",]
    STATIC_ROOT = 'static'
    MEDIA_ROOT = 'py_monocle_cms/media'
    MEDIA_URL = '/py_monocle_cms/media/'
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    ```
    
4.  Run `python3 manage.py migrate` once more. 
    
5.  In `mysite/urls.py`, change 

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
To create a super-user, execute the command `python3 manage.py createsuperuser`. 
Enter username, email and password and you're ready to go. Now you can not only log into the admin part of your webpage 
under `http://127.0.0.1:8000/login/`, you can also access the database tables and users under `http://127.0.0.1:8000/admin/`.
It is very important that you keep these login credentials secret!
