#Water - garden app

Simple flask app which will help users better maintain their house plants.  
The app will remind every user by email each time their flowers need to be water.

Hope it will improve your relationship with flowers and keep your place more green!

## How to run it

####Install requirements:
```bash
conda env create -f environment.yml
```

```bash
conda activate Water-garden
```

```bash
pip install -e .
```
####In app.py define SECRET_KEY to any string:

Example:

*app.config['SECRET_KEY'] = "895f9a59f56f4as1f5s4f7"*

####Final step:

```bash
python run.py
```

***
#Flask

Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.

Flask offers suggestions, but doesn't enforce any dependencies or project layout. It is up to the developer to choose the tools and libraries they want to use. There are many extensions provided by the community that make adding new functionality easy.
Installing

###Install and update using pip:

```bash
pip install -U Flask
```


###A Simple Example

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
```bash
$ flask run
```

  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
