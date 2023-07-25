# Might & Magic Online MMORPG

![Flake8](https://github.com/KuzenkovAG/hmom3/actions/workflows/ci.yml/badge.svg)
![Test](https://github.com/KuzenkovAG/hmom3/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/KuzenkovAG/hmom3/badge.svg?branch=main)](https://coveralls.io/github/KuzenkovAG/hmom3?branch=main)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

<div align="center" style="font-size: 18px;">
  <a href="http://momonline.pythonanywhere.com/">
    👉 Deploy on server 👈
  </a>
</div>

![alt text](screenshots/preview.png?raw=true)
![alt text](screenshots/town.jpg?raw=true)

## Deployment on server
[deploy] <- last working version

## Features
- Select your favorite fraction;
- Make buildings;
- Store resources.


## History
+ *v.0.5.1*  
Change buildings cost;
+ *v.0.5.0*  
Create page for trading resources;  
Trading available after building marketplace (by click on building).  
+ *v.0.4.0*  
Now increase gold incoming amount depend on administration building level;  
Now increase resources storage amount depend on storager level.  
+ *v.0.3.0*  
Add limit to resources;  
Add about page;  
Add page of resources incoming;  
+ *v.0.2.0*  
Add Inferno fraction;  
+ *v.0.1.0*  
Create ability to make buildings;


## Future plan
- Add ability to create Army;
- Add Heroes.

## Installation (windows)
1. Clone repository
```sh
git clone git@github.com:KuzenkovAG/hmom3.git
```
2. Install environment
```sh
cd hmom3/
```
```sh
py -3.9 -m venv venv
```
3. Activate environment
```sh
source venv/Scripts/activate
```
4. Install requirements
```sh
pip install -r requirements.txt
```
5. Make migrate
```sh
python hmom3/manage.py migrate
```
6. Fill DB
```sh
python hmom3/manage.py import_csv
```
7. Create superuser  <- for creation superuser need to use **ONLY** this command
```sh
python hmom3/manage.py create-superuser \
--username=admin \
--email=admin@mail.ru \
--password=admin
```
8. Run server
Before run make sure settings.DEBAG = True
```sh
python hmom3/manage.py runserver
```

   [deploy]: <http://momonline.pythonanywhere.com/>
   
