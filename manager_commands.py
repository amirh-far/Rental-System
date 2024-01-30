from util import pd_run_query_and_print_table, execute_query, get_address_id
from constraints import customer_rental_number_constraint, rental_duration_constraint, customer_no_service

def mgr_help():
    print(
        "commands:\n"
        "(1) get-customer-info\n"
        "(2) get-rental-info\n"
        "(3) get-active-rental\n"
        "(4) check-reservations\n"
        "(5) create-rental\n"
        "(6) update-store-info\n"
        "\n"
        "(7) highest-rated-films\n"
        "(8) highest-rated-films-category\n"
        "\n"
        "(9) search-film-actor\n"
        "(10) search-film-category\n"
        "(11) search-film-title\n"
        "(12) search-film-language\n"
        "(13) search-film-year\n"
        "\n"
        "(14) store-payments\n"
        "(15) payments-per-customer\n"
        "(16) payments-per-film\n"
        "\n"
        "(17) best-seller-category\n"
        "(18) best-seller-film\n"
        "(19) best-seller-actor\n"


    )

def get_mgr_command(engine, user_info):
    while True:
        mgr_help()
        command = input("choose command: ")
        if command == "exit":
            break
        elif command == "get-customer-info" or command == "1":
            get_customer_info(engine, user_info)
        elif command == "get-rental-info" or command == "2":
            get_rental_info(engine, user_info)
        elif command == "get-active-rental" or command == "3":
            get_active_rental(engine, user_info)
        elif command == "check-reservations" or command == "4":
            check_reservations(engine, user_info)
        elif command == "create-rental" or command == "5":
            create_rental(engine, user_info)
        elif command == "update-store-info" or command == "6":
            update_store_info(engine, user_info)

        elif command == "highest-rated-films" or command == "7":
            highest_rated_films(engine)
        elif command == "highest-rated-films-category" or command == "8":
            highest_rated_films_category(engine)

        elif command == "search-film-actor" or command == "9":
            search_film_actor(engine)
        elif command == "search-film-category" or command == "10":
            search_film_category(engine)
        elif command == "search-film-title" or command == "11":
            search_film_title(engine)
        elif command == "search-film-language" or command == "12":
            search_film_language(engine)
        elif command == "search-film-year" or command == "13":
            search_film_year(engine)

        elif command == "store-payments" or command == "14":
            store_payments(engine, user_info)
        elif command == "payments-per-customer" or command == "15":
            payments_per_customer(engine, user_info)
        elif command == "payments-per-film" or command == "16":
            payements_per_film(engine, user_info)
        elif command == "best-seller-category" or command == "17":
            best_seller_category(engine, user_info)
        elif command == "best-seller-film" or command == "18":
            best_seller_film(engine, user_info)
        elif command == "best-seller-actor" or command == "19":
            best_seller_actor(engine, user_info)

def get_customer_info(engine, user_info):
    q = f"""
        select customer.first_name, customer.last_name, customer.email
        from rental
        join customer on rental.customer_id = customer.customer_id
        join staff on rental.staff_id = staff.staff_id and staff.staff_id = {user_info["staff_id"][0]}
        limit 10;
    """
    pd_run_query_and_print_table(query=q, engine=engine)

def get_rental_info(engine, user_info):
    q = f"""
        select
            film.title,
            count(rental.rental_id) as rental_count,
            film.rating,
            count(inventory.inventory_id) as number_in_inventory
        from rental
        right join inventory on rental.inventory_id = inventory.inventory_id
        join film on inventory.film_id = film.film_id
        where staff_id={user_info["staff_id"][0]}
        group by film.film_id
        limit 10;
    """
    pd_run_query_and_print_table(query=q, engine=engine)

def get_active_rental(engine, user_info):
    q = f"""
        select rental_id,
            rental_date,
            return_date,
            first_name,
            last_name,
            email
        from rental
        join customer on rental.customer_id = customer.customer_id
        where return_date > NOW() and rental.staff_id={user_info["staff_id"][0]};
    """
    pd_run_query_and_print_table(query=q, engine=engine)

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


def store_payments(engine, user_info):
    q = f"""
        select
            inventory.store_id,
            sum(amount)
        from payment
        join rental on payment.rental_id = rental.rental_id
        join inventory on rental.inventory_id = inventory.inventory_id
        where rental.staff_id = {user_info["staff_id"][0]}
        group by inventory.store_id;
        """
    pd_run_query_and_print_table(query=q, engine=engine)

def payments_per_customer(engine, user_info):
    q = f"""
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
        where rental.staff_id = {user_info["staff_id"][0]}
        group by payment.customer_id, inventory.store_id
        limit 30;
        """
    pd_run_query_and_print_table(query=q, engine=engine)

def payements_per_film(engine, user_info):
    q = f"""
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
        where rental.staff_id={user_info["staff_id"][0]}
        group by film.film_id, store_id
        limit 30;
        """
    pd_run_query_and_print_table(query=q, engine=engine)

def best_seller_category(engine, user_info):
    q = f"""
        select
            category.name,
            sum(payment.amount) as earned
        from category
        join film_category on category.category_id = film_category.category_id
        join film on film_category.film_id = film.film_id
        join inventory on film.film_id = inventory.film_id
        join rental on inventory.inventory_id = rental.inventory_id
        join payment on rental.rental_id = payment.rental_id
        where rental.staff_id = {user_info["staff_id"][0]}
        group by category.name
        order by earned DESC
        limit 1;
        """
    pd_run_query_and_print_table(query=q, engine=engine)

def best_seller_film(engine, user_info):
    q = f"""
        select
            title,
            sum(payment.amount) as earned
        from film
        join inventory on film.film_id = inventory.film_id
        join rental on inventory.inventory_id = rental.inventory_id
        join payment on rental.rental_id = payment.rental_id
        where rental.staff_id = {user_info["staff_id"][0]}
        group by film.film_id
        order by earned DESC
        limit 1;
        """
    pd_run_query_and_print_table(query=q, engine=engine)


def best_seller_actor(engine, user_info):
    q = f"""
        select
            first_name as actor_fist_name,
            last_name as actor_last_name,
            sum(payment.amount) as earned
        from actor
        join film_actor on actor.actor_id = film_actor.actor_id
        join inventory on film_actor.film_id = inventory.film_id
        join rental on inventory.inventory_id = rental.inventory_id
        join payment on rental.rental_id = payment.rental_id
        where rental.staff_id = {user_info["staff_id"][0]}
        group by actor.actor_id
        order by earned DESC
        limit 1
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

def check_reservations(engine, user_info):
    q = f"""
        select
            reserve_id,
            inventory.store_id,
            film.film_id,
            title,
            accepted
        from reserve
        join inventory on reserve.inventory_id = inventory.inventory_id
        join mgr_store on inventory.store_id = mgr_store.store_id
        join film on inventory.film_id = film.film_id
        where  mgr_store.mgr_id = {user_info["staff_id"][0]};
        """
    pd_run_query_and_print_table(q, engine)

def create_rental(engine, user_info):
    store_id = input("enter store id: ")
    customer_id = input("enter customer id: ")
    inventory_id = input("enter inventory id: ")
    rental_date = input("enter rental date: ")
    return_date = input("enter return date: ")

    # constraints
    if not customer_rental_number_constraint(engine, customer_id, store_id):
        print("this customer can not have more rentals from your store")
        return
    if not rental_duration_constraint(rental_date, return_date):
        print("Your rental can not be less than a day or more than two weeks.")
        return
    if not customer_no_service(engine, customer_id):
        print("this customer has had more than 10 delays and can not rent a film anymore.")
        return

    insert_q = f"""
        insert into rental(inventory_id, customer_id, staff_id, rental_date, return_date)
        values ({inventory_id}, {customer_id}, {user_info["staff_id"][0]}, '{rental_date}', '{return_date}')
        """
    execute_query(insert_q, engine)
    print("successfully created rental")

def update_store_info(engine, user_info):
    stores_q = f"""
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
        where mgr_id = {user_info["staff_id"][0]}
        limit 30;
        """
    pd_run_query_and_print_table(stores_q, engine)

    selected_store_id = input("select a store: ")
    
    address_q = f"""
        select
            address.address_id
        from address
        join store on address.address_id = store.address_id
        where store_id = {selected_store_id}
        """
    
    address_id = get_address_id(engine, address_q)
    
    address = input("enter new address: ")
    phone = input("enter new phone: ")
    postal_code = input("enter new postal code: ")

    update_addr_q = f"""
        update address
        set address = '{address}', phone = {phone}, postal_code = {postal_code}
        where address_id = {address_id};
        """    
    execute_query(update_addr_q, engine)
    print("store information updated successfully")
