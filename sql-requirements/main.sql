show create table store;
use rental_sys;
select *
from
    city, country
where country.country_id = city.country_id and country='Canada';

insert into staff(first_name, last_name, address_id, picture, email, store_id, active, username, password, last_update);

select rental_id, customer.*
from rental
join customer on rental.customer_id = customer.customer_id
join staff on rental.staff_id = staff.staff_id and staff.staff_id = 2;

select
    film.title,
    count(rental.rental_id) as rental_count,
    film.rating,
    count(inventory.inventory_id) as number_in_inventory
from rental
right join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where staff_id=1
group by film.film_id;

select rental_id,
       rental_date,
       return_date,
       first_name,
       last_name,
       email
from rental
join customer on rental.customer_id = customer.customer_id
where return_date > NOW();

select film.film_id,
       film.title,
       category.name,
       film.release_year,
       film.rating
from film
join film_category on film.film_id = film_category.film_id
join category on film_category.category_id = category.category_id
where category.name = '{}' ;

select film.film_id,
       film.title,
       film.release_year,
       film.rating
from film
where film.title = '{}' ;


select
    film_id,
    title,
    rating,
    release_year,
    language.name as language_name
from film
join language on film.language_id = language.language_id
where language.name = '{}';

select
    film_id,
    title,
    rating,
    release_year
from film
where release_year = '{}';

select
    rental.staff_id,
    inventory.store_id,
    sum(amount)
from payment
join rental on payment.rental_id = rental.rental_id
join inventory on rental.inventory_id = inventory.inventory_id
group by inventory.store_id;

select
    inventory.store_id,
    first_name,
    last_name,
    email,
    sum(amount)
from payment
join rental on payment.rental_id = rental.rental_id
join inventory on rental.inventory_id = inventory.inventory_id
join customer on payment.customer_id = customer.customer_id
group by payment.customer_id, inventory.store_id;

select
    film.film_id,
    title,
    rating,
    sum(amount),
    store_id
from payment
join rental on payment.rental_id = rental.rental_id
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where rental.staff_id={}
group by film.film_id, store_id;

select
    category.name,
    sum(payment.amount) as earned
from category
join film_category on category.category_id = film_category.category_id
join film on film_category.film_id = film.film_id
join inventory on film.film_id = inventory.film_id
join rental on inventory.inventory_id = rental.inventory_id
join payment on rental.rental_id = payment.rental_id
where rental.staff_id = 2
group by category.name
order by earned DESC
limit 1;

select
    title,
    sum(payment.amount) as earned
from film
join inventory on film.film_id = inventory.film_id
join rental on inventory.inventory_id = rental.inventory_id
join payment on rental.rental_id = payment.rental_id
where rental.staff_id = 2
group by film.film_id
order by earned DESC
limit 1;

select
    first_name as actor_fist_name,
    last_name as actor_last_name,
    sum(payment.amount) as earned
from actor
join film_actor on actor.actor_id = film_actor.actor_id
join inventory on film_actor.film_id = inventory.film_id
join rental on inventory.inventory_id = rental.inventory_id
join payment on rental.rental_id = payment.rental_id
where rental.staff_id = 2
group by actor.actor_id
order by earned DESC
limit 1;

select
    address.address,
    phone,
    postal_code,
    city.city,
    country.country

from store
join address on store.address_id = address.address_id
join city on address.city_id = city.city_id
join country on city.country_id = country.country_id
join mgr_store on mgr_store.store_id = store.store_id
where mgr_store.mgr_id = 2;

update customer
set first_name = '{}', last_name = '{}' , email = '{}', username = '{}', password = '{}'
where username = '{}';

select
    title,
    rating,
    category.name as category_name
from film
join film_category on film.film_id = film_category.film_id
join category on film_category.category_id = category.category_id
order by category.name
limit 30;

select
    title,
    rating
from film
order by rating DESC;


select
    category.name,
    max(rating)
from film
join film_category on film.film_id = film_category.film_id
join category on film_category.category_id = category.category_id
group by category.name
having max(rating)
limit 30;

select
    title,
    count(rental.rental_id) as rent_count,
    rating
from rental
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
group by film.film_id
limit 30;

select
    title,
    rental_id
from rental
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where customer_id = 599
limit 30;

select
    inventory_id
from inventory
where store_id = 1 and film_id = 1
limit 1;

insert into reserve(inventory_id)
values ()

select
    rental_id,
    title
from rental
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where customer_id = 599 and return_date > NOW();

delete from rental
where rental_id = {}

select
    rental_id,
    title,
    rental_date,
    return_date,
    (NOW() - return_date) as remaining_time

from rental
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where return_date > NOW() and customer_id = {};

select
    payment_id,
    title,
    inventory.store_id,
    amount
from payment
join rental on payment.rental_id = rental.rental_id
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where payment.customer_id = 599

select
    reserve_id,
    inventory.store_id,
    title,
    accepted
from reserve
join inventory on reserve.inventory_id = inventory.inventory_id
join mgr_store on inventory.store_id = mgr_store.store_id
join film on inventory.film_id = film.film_id
where  mgr_store.mgr_id = {};

insert into rental(inventory_id, customer_id, rental_date, return_date)
values ()

select
    store.store_id,
    address.address,
    phone,
    postal_code,
    city.city,
    country.country
from store
join mgr_store on store.store_id = mgr_store.store_id
join address on store.address_id = address.address_id
join city on address.city_id = city.city_id
join country on city.country_id = country.country_id
where mgr_id = {}



update address

select
    address.address_id
from address
join store on address.address_id = store.address_id
join mgr_store on store.store_id = mgr_store.store_id
where  mgr_id = {}

update address
set address = '{}', phone = '{}', postal_code = '{}'

select
    count(*)
from rental
join inventory on rental.inventory_id = inventory.inventory_id
where rental.customer_id = {} and store_id = {}

select
    count(store_id)
from mgr_store
where mgr_id = {}

