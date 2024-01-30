alter table customer add column username varchar(50);
alter table customer add column password varchar(50);

# insert into customer
#     (first_name, last_name, email, username, password)
# values (1, 'amir', 'far', 'amir@gmail.com', 1, 'amir1680', 'amir123');
#
# insert into staff(first_name, last_name, address_id, email, store_id, username, password)
# values ('mgr', 'far', 2, 'amir@gmail.com', 1, 'mgr', '1234');

alter table customer
drop column store_id;

alter table customer
drop foreign key fk_customer_address;

alter table customer
drop column address_id;

alter table customer
drop column active;

alter table staff
drop foreign key fk_staff_address;

alter table staff
drop column address_id;

alter table staff
drop column picture;

alter table staff
drop column active;

alter table address
drop column location;

alter table address
drop column district;


create table mgr_store (
    mgr_id  tinyint unsigned NOT NULL,
    store_id tinyint unsigned NOT NULL,
    primary key (mgr_id, store_id),
    foreign key (mgr_id) references staff(staff_id),
    foreign key (store_id) references store(store_id)
)

alter table staff
drop foreign key fk_staff_store;

alter table staff
drop column store_id;

alter table store
drop foreign key fk_store_staff;

alter table store
drop column manager_staff_id;

create table reserve (
    reserve_id smallint unsigned not null auto_increment,
    inventory_id mediumint unsigned NOT NULL,
    primary key (reserve_id),
    foreign key (inventory_id) references inventory(inventory_id)
);

show create table rental;

alter table reserve
add column accepted bool;

create table rental_delay(
    delay_id smallint unsigned not null auto_increment,
    rental_id int NOT NULL,
    primary key (delay_id),
    foreign key (rental_id) references rental(rental_id)
)

select
    count(delay_id)
from rental_delay
join rental on rental_delay.rental_id = rental.rental_id
where customer_id = {}
