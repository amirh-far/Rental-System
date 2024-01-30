from util import count_rentals, count_stores, count_delays
from datetime import datetime


def customer_rental_number_constraint(engine, customer_id, store_id):
    q = f"""
        select 
            count(*) as cnt
        from rental
        join inventory on rental.inventory_id = inventory.inventory_id
        where rental.customer_id = {customer_id} and store_id = {store_id}
        """
    
    count = count_rentals(engine, q)

    if count >= 3:
        return False
    else:
        return True
    
def mgr_number_of_stores_constraint(engine, manager_id):
    q = f"""
        select
            count(store_id) as cnt
        from mgr_store
        where mgr_id = {manager_id}
        """
    count = count_stores(engine, q)

    if count >= 2:
        return False
    else:
        return True
    
def rental_duration_constraint(rental_date, return_date):
    date_format = "%Y-%m-%d"
    rental_date = datetime.strptime(rental_date, date_format)
    return_date = datetime.strptime(return_date, date_format)

    days_difference = (return_date - rental_date).days

    if days_difference < 1 or days_difference > 14:
        return False
    else:
        return True
    
def rental_payment_value_mismatch_constraint(payment_amount, rental_date, return_date):
    date_format = "%Y-%m-%d"
    rental_date = datetime.strptime(rental_date, date_format)
    return_date = datetime.strptime(return_date, date_format)

    days_difference = (return_date - rental_date).days

    if payment_amount != days_difference*2:
        return False
    else:
        return True
    
def customer_no_service(engine, customer_id):
    q = f"""
        select
            count(delay_id) as cnt
        from rental_delay
        join rental on rental_delay.rental_id = rental.rental_id
        where customer_id = {customer_id}
        """
    count = count_delays(engine, q)

    if count > 10:
        return False
    else:
        return True
    