# hmom3 Online game

*Is under developing*

![alt text](preview/preview.png?raw=true)

## Deploy on server
[deploy] <- last working version


## Features
- Can select your favorite fraction;
- Make buildings;
- Store resources.


## History
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
- Apply logic to increase gold amount;
- Add page for statistics.

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
   
