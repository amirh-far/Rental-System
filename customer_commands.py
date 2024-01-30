from util import pd_run_query_and_print_table, execute_query, get_inventory_id, insert_db

def customer_help():
    print(
        "commands:\n"
        "(1) store-info\n"
        "(2) update-profile-info\n"
        "(3) films-by-category\n"
        "(4) highest-rated-films\n"
        "(5) highest-rated-films-category\n"
        "\n"
        "(6) search-film-actor\n"
        "(7) search-film-category\n"
        "(8) search-film-title\n"
        "(9) search-film-language\n"
        "(10) search-film-year\n"
        "\n"
        "(11) rental-film-count\n"
        "(12) customer-rental-list\n"
        "(13) new-reservation\n"
        "(14) customer-active-rents-close\n"
        "(15) active-rents-list\n"
        "(16) payment-info"
    )

def get_customer_command(engine, user_info):
    while True:
        customer_help()
        command = input("choose command: ")
        if command == "exit":
            break
        elif command == "store-info" or command == "1":
            store_info(engine)
        elif command == "update-profile-info" or command == "2":
            update_profile_info(engine, user_info)
        elif command == "films-by-category" or command == "3":
            films_by_category(engine)

        elif command == "highest-rated-films" or command == "4":
            highest_rated_films(engine)
        elif command == "highest-rated-films-category" or command == "5":
            highest_rated_films_category(engine)

        elif command == "search-film-actor" or command == "6":
            search_film_actor(engine)
        elif command == "search-film-category" or command == "7":
            search_film_category(engine)
        elif command == "search-film-title" or command == "8":
            search_film_title(engine)
        elif command == "search-film-language" or command == "9":
            search_film_language(engine)
        elif command == "search-film-year" or command == "10":
            search_film_year(engine)
            
        elif command == "rental-film-count" or command == "11":
            rental_film_count(engine)
        elif command == "customer-rental-list" or command == "12":
            customer_rental_list(engine, user_info)
        elif command == "new-reservation" or command == "13":
            new_reservation(engine)
        elif command == "customer-active-rents-close" or command == "14":
            customer_active_rents_delete(engine, user_info)
        elif command == "active-rents-list" or command == "15":
            active_rents_list(engine, user_info)
        elif command == "payment-info" or command == "16":
            payment_info(engine, user_info)

def store_info(engine):
    q = f"""
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
    """
    pd_run_query_and_print_table(q, engine)

def update_profile_info(engine, user_info):
    first_name = input("new first name: ")
    last_name = input("new last name: ")
    email = input("new email: ")
    username = input("new username: ")
    password = input("new password: ")
    q = f"""
        update customer
        set first_name = '{first_name}', last_name = '{last_name}' , email = '{email}', username = '{username}', password = '{password}'
        where customer_id = {user_info["customer_id"][0]};
        """
    execute_query(q, engine)
    print("profile updated successfully")

def films_by_category(engine):
    q = f"""
        select
            title,
            rating,
            category.name as category_name
        from film
        join film_category on film.film_id = film_category.film_id
        join category on film_category.category_id = category.category_id
        order by category.name
        limit 30;
    """
    pd_run_query_and_print_table(q, engine)

def highest_rated_films(engine):
    q = f"""
        select
            title,
            rating
        from film
        order by rating DESC
        limit 30;
        """
    pd_run_query_and_print_table(q, engine)

def highest_rated_films_category(engine):
    q = f"""
select
    category.name,
    max(rating)
from film
join film_category on film.film_id = film_category.film_id
join category on film_category.category_id = category.category_id
group by category.name
having max(rating)
limit 30;
"""
    pd_run_query_and_print_table(q, engine)

def search_film_actor(engine):
    actor = input("enter actor name: ")
    f_name, l_name = actor.split(" ")
    q = f"""
        select film.film_id,
            film.title,
            actor.first_name,
            actor.last_name,
            film.release_year,
            film.rating
        from film
        join film_actor on film.film_id = film_actor.film_id
        join actor on film_actor.actor_id = actor.actor_id
        where actor.first_name= '{f_name}' and actor.last_name = '{l_name}';
        """
    pd_run_query_and_print_table(query=q, engine=engine)


def search_film_category(engine):
    category = input("enter category name: ")
    q = f"""
        select film.film_id,
            film.title,
            category.name,
            film.release_year,
            film.rating
        from film
        join film_category on film.film_id = film_category.film_id
        join category on film_category.category_id = category.category_id
        where category.name = '{category}' ;
        """
    pd_run_query_and_print_table(query=q, engine=engine)


def search_film_title(engine):
    film_name = input("enter film name: ")
    q = f"""
        select film.film_id,
            film.title,
            film.release_year,
            film.rating
        from film
        where film.title = '{film_name}' ;
        """
    pd_run_query_and_print_table(query=q, engine=engine)


def search_film_language(engine):
    language = input("enter film language: ")   
    q = f"""
        select
            film_id,
            title,
            rating,
            release_year,
            language.name as language_name
        from film
        join language on film.language_id = language.language_id
        where language.name = '{language}'
        limit 30;    
        """
    pd_run_query_and_print_table(query=q, engine=engine)


def search_film_year(engine):
    year = input("enter film year: ")
    q = f"""
    select
        film_id,
        title,
        rating,
        release_year
    from film
    where release_year = {year}
    limit 20;
    """
    pd_run_query_and_print_table(query=q, engine=engine)

def rental_film_count(engine):
    q = f"""
        select
            title,
            count(rental.rental_id) as rent_count,
            rating
        from rental
        join inventory on rental.inventory_id = inventory.inventory_id
        join film on inventory.film_id = film.film_id
        group by film.film_id
        limit 30;
        """
    pd_run_query_and_print_table(q, engine)

def customer_rental_list(engine, user_info):
    q = f"""
        select
            title,
            rental_id
        from rental
        join inventory on rental.inventory_id = inventory.inventory_id
        join film on inventory.film_id = film.film_id
        where customer_id = {user_info["customer_id"][0]}
        limit 30;
        """
    pd_run_query_and_print_table(q, engine)

def new_reservation(engine):
    store_id = input("enter store id: ")
    film_id = input("enter film id: ")

    get_inventory_id_q = f"""
        select
            inventory_id
        from inventory
        where store_id = {store_id} and film_id = {film_id}
        limit 1;
        """
    inventory_id = get_inventory_id(engine, get_inventory_id_q)

    insert_q = f"""
        insert into reserve(inventory_id)
        values ({inventory_id})
        """
    insert_db(insert_q, engine)
    print("successfully reserved.")

def customer_active_rents_delete(engine, user_info):
    active_rents_q = f"""
        select
            rental_id,
            title
        from rental
        join inventory on rental.inventory_id = inventory.inventory_id
        join film on inventory.film_id = film.film_id
        where customer_id = {user_info["customer_id"][0]} and return_date > NOW()
        limit 30;
        """
    pd_run_query_and_print_table(active_rents_q, engine)

    rent_id = input("choose rent id to close: ")
    delete_rent_q = f"""
        delete from rental
        where rental_id = {rent_id}
        """
    execute_query(delete_rent_q, engine)
    print("selected rent closed")

def active_rents_list(engine, user_info):
    q = f"""
    select
        rental_id,
        title,
        rental_date,
        return_date,
        (NOW() - return_date) as remaining_time

    from rental
    join inventory on rental.inventory_id = inventory.inventory_id
    join film on inventory.film_id = film.film_id
    where return_date > NOW() and customer_id = {user_info["customer_id"][0]};
    """
    pd_run_query_and_print_table(q, engine)

def payment_info(engine, user_info):
    q = f"""
        select
            payment_id,
            title,
            inventory.store_id,
            amount
        from payment
        join rental on payment.rental_id = rental.rental_id
        join inventory on rental.inventory_id = inventory.inventory_id
        join film on inventory.film_id = film.film_id
        where payment.customer_id = {user_info["customer_id"][0]}
        limit 30;
        """
    pd_run_query_and_print_table(q, engine)