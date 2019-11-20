<h1 align="center">Fyyur 🔥</h1>
<p>
  <img src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/wanderindev/fyyur/blob/master/README.md">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://github.com/wanderindev/fyyur/graphs/commit-activity">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://github.com/wanderindev/fyyur/blob/master/LICENSE.md">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://twitter.com/JavierFeliuA">
    <img alt="Twitter: JavierFeliuA" src="https://img.shields.io/twitter/follow/JavierFeliuA.svg?style=social" target="_blank" />
  </a>
</p>

>Fyyur is the first project for the 2019 Udacity Full-stack Developer Nanodegree.  The project
>is associated to the SQL and Data Modeling for the Web course.  The starter code and project instructions
>can be found [here.](https://github.com/udacity/FSND/tree/master/projects/01_fyyur/starter_code)

## How to use
Clone the repository:
```sh
git clone https://github.com/wanderindev/fyyur.git
cd fyyur
``` 
Create a virtual environment, activate it, and install the requirements:
```sh
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
Deploy a Postgresql instance in a Docker container:
```sh
cd postgresql
docker-compose up --build
```
In a new terminal window, from the project's root, upgrade the database:
```sh
flask db upgrade
```
Run the application:
```sh
export FLASK_APP=run
flask run
```
## Configuration
Configuration values are located in ```config.py```. If using a database other
than the instance running in Docker, the connection string can be modified there.

Upon the first request, the application will populate the database with fake
data.  This feature can be turn off changing the value for ```POPULATE_DB``` in ```config.py```
to ```False```.

 ## Author

👤 **Javier Feliu**

* Twitter: [@JavierFeliuA](https://twitter.com/JavierFeliuA)
* Github: [@wanderindev](https://github.com/wanderindev)

[Starter code](https://github.com/udacity/FSND/tree/master/projects/01_fyyur/starter_code) 
provided by [Udacity](https://www.udacity.com/).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [Javier Feliu](https://github.com/wanderindev).<br />

This project is [MIT](https://github.com/wanderindev/fyyur/blob/master/LICENSE.md) licensed.

***
_I based this README on a template generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_