<p>
  <img src="https://github.com/amirh-far/Rental-System/blob/main/readme-images/rental-sys.png"/>
</p>

Rental System built with MySQL, Python & Pandas using Sakila Database.

<p align="center">
  <img src="https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue"/>
  <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"/>
</p>

## About

This project has an emphasis on using SQL Queries to master main and key queries.<br>
To interact with the user, I used Python. So user can enter his/her commands via Terminal.<br>
The database used in this project is Sakila Database which is documented at this [link](https://dev.mysql.com/doc/sakila/en/).<br>
E-R Diagram is also availabe in the Repo in this [link](https://github.com/amirh-far/Rental-System/blob/main/E-R%20Diagram.jpg).<br>
Two types of user is availabe: Customer and Manager.<br>
To register as a customer choose 2 in order to register as a customer and choose 3 to register a store and register as a manager.

## Features
- Menu Features
    - login
    - customer registeration
    - store registration<br>
- Below theres a full list of different commands, which can be performed. Every command is executed with at least one query.<br> 
- Cutomer Commands
    - store-info
    - update-profile-info
    - films-by-category
    - highest-rated-films
    - highest-rated-films-category
    - search-film-actor
    - search-film-category
    - search-film-title
    - search-film-language
    -  search-film-year
    -  rental-film-count
    -  customer-rental-list
    -  new-reservation
    -  customer-active-rents-close
    -  active-rents-list
    -  payment-info
- Manager Commands
    - get-customer-info
    - get-rental-info
    - get-active-rental
    - check-reservations
    - create-rental
    - update-store-info
    - highest-rated-films
    - highest-rated-films-category
    - search-film-actor
    - search-film-category
    - search-film-title
    - search-film-language
    - search-film-year
    - store-payments
    - payments-per-customer
    - payments-per-film
    - best-seller-category
    - best-seller-film
    - best-seller-actor

### Installation
1. install MySQL on your Machine. [link](https://dev.mysql.com/downloads/installer/)
2. clone the repo
```bash
git clone https://github.com/amirh-far/Rental-System.git
```
3. login in your SQL via Terminal and execute these commands one by one
```bash
create database rental_sys;
use rental_sys;
source /path/to/the/sql/file/in/folder:sakila-db/sakila-schema.sql
source /path/to/the/sql/file/inside/folder:sakila-db/sakila-data.sql
source /path/to/the/sql/file/inside/folder:sql-requirements/table_modifications.sql
```
If you have any questions and errors in step 3, let me know.<br>
4. install python 3.11 or any version. [Install Python](https://www.python.org/downloads/release/python-3117/)
5. create a Python Vritual Environment based on your machine. on Unix:
```bash
python -m venv venv
```
6. activate the environment. on Unix:
```bash
cd your/repo/path
source venv/bin/activate
```
7. run pip install
```bash
pip install -r requirements.txt
```
8. run main.py
```bash
python main.py
```
You are good to go. Use register customer or store registration to proceed.

## Screenshots
### Menu
<p>
  <img src="https://github.com/amirh-far/Rental-System/blob/main/readme-images/menu.png" height="320" width="320" />
</p>

### Get Rental Info
<p>
  <img src="https://github.com/amirh-far/Rental-System/blob/main/readme-images/get-rental-info.png"/>
</p>

### Highest Rated Films Category
<p>
  <img src="https://github.com/amirh-far/Rental-System/blob/main/readme-images/%20highest-rated-films-category.png"/>
</p>

### Payment Info
<p>
  <img src="https://github.com/amirh-far/Rental-System/blob/main/readme-images/payment-info.png"/>
</p>

### Rental Film Count
<p>
  <img src="https://github.com/amirh-far/Rental-System/blob/main/readme-images/rental-film-count.png"/>
</p>

### Search Film via Category
<p>
  <img src="https://github.com/amirh-far/Rental-System/blob/main/readme-images/search-film-category.png"/>
</p>

## Contributing

Feel free to contribute to this project. Also if you have any questions, errors etc. let me know.<br>
You can reach out to me via Gmail, LinkedIn or Telegram. Links are available in my github profile in this [link](https://github.com/amirh-far).


