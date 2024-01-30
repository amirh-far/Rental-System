from tabulate import tabulate
import pandas as pd
from sqlalchemy import text

def insert_db(query, engine):
    with engine.connect() as connection:
        connection.execute(text(query))
        connection.commit()

def execute_query(query, engine):
    with engine.connect() as connection:
        connection.execute(text(query))
        connection.commit()

def pd_run_query_and_print_table(query, engine):
    df = pd.read_sql_query(query, engine)
    table = tabulate(df, headers="keys", tablefmt='grid') 
    print(table)

def username_available_check(username, mgr=False, engine=None):
    if mgr:
        username_available_q = f"""
                    select *
                    from
                        staff
                    where
                        username = '{username}'
                """
    else:
        username_available_q = f"""
                select *
                from
                    customer
                where
                    username = '{username}'
            """
    with engine.connect() as connection:
        username_check_result = connection.execute(text(username_available_q)).fetchone()
    
    if username_check_result:
        return False
    else:
        return True
    
def get_inventory_id(engine, q):
    inventory_df = pd.read_sql_query(q, engine)
    inventory_id = inventory_df["inventory_id"][0]
    return inventory_id

def get_address_id(engine, q):
    address_df = pd.read_sql_query(q, engine)
    address_id = address_df["address_id"][0]
    return address_id

def count_rentals(engine, q):
    count_df = pd.read_sql_query(q, engine)
    count = count_df["cnt"][0]
    return count

def count_stores(engine, q):
    stores_df = pd.read_sql_query(q, engine)
    count = stores_df["cnt"][0]
    return count
def count_delays(engine, q):
    delays_df = pd.read_sql_query(q, engine)
    count = delays_df["cnt"][0]
    return count