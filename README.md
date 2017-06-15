# A simple content management system for Django

This is the repository for py-monocle-cms, the content management system I use for my homepage, monoclecat.de.
py-monocle-cms is meant for small, multilingual sites that are built as a blog with one user-account being the maintainer, 
having superuser rights. 

Features are:

* Easy image upload and automatic thumbnail generation
* The landing page lists the content of all pages like a blog
* The content of pages is written in [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), 
no html required!

## Installation

This short guide covers the installation from scratch. If you want to embed the app into your existing project, 
I believe you are knowledgeable enough to leave out the steps aimed at configuring newly created projects. 

1. If you haven't done so yet, create a new django project, as described 
[in Django Tutorial 01](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)
To save you the click: `cd` to your desired directory and create a project with the command 
`django-admin startproject mysite`. Run `python3 manage.py migrate` to initialize the project. 

2. Jump into the newly created directory with `cd mysite/` and clone the py-monocle-cms app into the newly created 
project by running `git clone https://github.com/monoclecat/py-monocle-cms.git`.

3. Now open `mysite/settings.py` and add these lines to the `INSTALLED_APPS` list. 
```
    'py-monocle-cms.apps.MonocleCmsConfig',
    'bootstrap3',
    'markdown',
    'crispy_forms',
```

4. Next, open `mysite/urls.py`. In this very sparsely populated file you should find this piece of code: 
 
```
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('testsite.urls')),
]
```

Add the following line of code in the urlpatterns and add the `include` import to the first line:

```
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('mysite.urls')),
]
```



