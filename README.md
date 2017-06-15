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
project by running `git clone https://github.com/monoclecat/py_monocle_cms.git`.

