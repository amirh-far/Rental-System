from sqlalchemy import create_engine
import os
import pandas as pd
from tabulate import tabulate
import getpass

from util import insert_db, username_available_check
from manager_commands import get_mgr_command
from customer_commands import get_customer_command
from constraints import mgr_number_of_stores_constraint

USER_INFO = None
STORE_INFO = None
MANAGER_BOOL = False
ENGINE = None


def connect_to_database():
    global ENGINE
    host = "localhost"
    user = "root"
    password = "amir1680"
    database = "rental_sys"

    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
    ENGINE = engine
    return engine


def menu():
    while True:
        print(
            "(1) login\n"
            "(2) customer registeration\n"
            "(3) store registration\n"
            "(4) exit"
        )
        menu_selection = input("choose a number: ")

        try:
            menu_selection = int(menu_selection)
            if menu_selection > 4 or menu_selection < 1:
                raise ValueError
            return menu_selection
        except:
            print("please enter a number: 1, 2, 3 or 4")


def login():
    global USER_INFO
    global STORE_INFO
    global MANAGER_BOOL
    while True:
        username = input("username: ")
        password = getpass.getpass("password: ")

        customer_login_q = f"""
            select *
            from
                customer
            where
                username = '{username}' and password = '{password}'
        """
        user_info = pd.read_sql_query(customer_login_q, ENGINE)
        # table = tabulate(user_info, headers="keys", tablefmt='grid')
        if not user_info.empty:
            MANAGER_BOOL = False
            USER_INFO = user_info
            return
        
        manager_login_q = f"""
            select *
            from
                staff
            where
                username = '{username}' and password = '{password}'
        """
        user_info = pd.read_sql_query(manager_login_q, ENGINE)

        if not user_info.empty:
            MANAGER_BOOL = True
            USER_INFO = user_info
            mgr_id = user_info["staff_id"][0]
            mgr_store_q = f"""
                    select *
                    from
                        mgr_store
                    where mgr_id={mgr_id};
                """
            mgr_store_df = pd.read_sql_query(mgr_store_q, ENGINE)
            store_id = mgr_store_df["store_id"][0]      
            select_store_q = f"""
                select *
                from
                    store
                where store_id={store_id};
            """
            selected_store_df = pd.read_sql_query(select_store_q, ENGINE)
            STORE_INFO = selected_store_df     
            # store_table = tabulate(STORE_INFO, headers="keys", tablefmt='grid')
            # print(store_table)

            return
        
        print("invalid username or password. try again.")



def customer_register():
    global USER_INFO
    global MANAGER_BOOL
    MANAGER_BOOL = False

    while True:
        username = input("username: ")
        password = getpass.getpass("password: ")
        password2 = getpass.getpass("password again: ")
        f_name = input("first_name: ")
        l_name = input("last_name: ")
        email = input("email: ")


        if password == password2 and username_available_check(username, False, ENGINE):
            q = f"""
            insert into customer (first_name, last_name, email,username, password)
            values ('{f_name}', '{l_name}', '{email}', '{username}', '{password}');
            """
            insert_db(q, ENGINE)
            
            customer_login_q = f"""
                select *
                from
                    customer
                where
                    username = '{username}' and password = '{password}'
            """
            USER_INFO = pd.read_sql_query(customer_login_q, ENGINE)

            return
        
        else:
            print("username already taken or password mismatch")


def store_registration():
        global USER_INFO
        global STORE_INFO
        global MANAGER_BOOL
        while True:
            username = input("username: ")
            password = getpass.getpass("password: ")
            password2 = getpass.getpass("password again: ")
            f_name = input("first_name: ")
            l_name = input("last_name: ")
            email = input("email: ")
            # username = "amirh"
            # password = "1234"
            # password2 = "1234"
            # f_name = "amir"
            # email = "far"
            # l_name = "lol"

            if password == password2 and username_available_check(username, True, ENGINE):
                # insert mgr user
                insert_mgr_q = f"""
                    insert into staff(first_name, last_name, email, username, password)
                    values ('{f_name}', '{l_name}', '{email}', '{username}', '{password}')
                """
                insert_db(insert_mgr_q, ENGINE)

                # get manager
                select_mgr_q = f"""
                    select *
                    from
                        staff
                    where username='{username}';
                """
                selected_mgr_df = pd.read_sql_query(select_mgr_q, ENGINE)
                USER_INFO = selected_mgr_df   
                manager_id = USER_INFO["staff_id"][0]
                
                if not mgr_number_of_stores_constraint(engine, manager_id):
                    print("You can\'t have more than 2 stores.")
                    return

                # get country
                country_q = f"""
                    select *
                    from
                        country
                    limit 10;
                """
                country_df = pd.read_sql_query(country_q, ENGINE)
                country_table = tabulate(country_df, headers="keys", tablefmt='grid')
                print(country_table)

                country_input = input("enter your country: ")

                selected_country_q = f"""
                    select *
                    from
                        country
                    where country='{country_input}';
                """
                selected_country_df = pd.read_sql_query(selected_country_q, ENGINE)        
                country_id = selected_country_df["country_id"][0]
                # get city
                city_q = f"""
                    select *
                    from
                        city
                    where country_id='{country_id}'
                    limit 10;
                """
                city_df = pd.read_sql_query(city_q, ENGINE)
                city_table = tabulate(city_df, headers="keys", tablefmt='grid') 
                print(city_table)

                city_input = input("enter your city: ")

                selected_city_q = f"""
                    select *
                    from
                        city
                    where city='{city_input}';
                """
                selected_city_df = pd.read_sql_query(selected_city_q, ENGINE)        
                city_id = selected_city_df["city_id"][0]

                # get address
                store_addr_input = input("enter your store address: ")
                insert_addr_q = f"""
                    insert into address (city_id, address, phone, postal_code)
                    values ({city_id}, '{store_addr_input}', 0, 0)
                """
    
                insert_db(insert_addr_q, ENGINE)

                # get address id
                get_addr_q = f"""
                    select *
                    from address
                    where
                        address = '{store_addr_input}'
                """
                address_id = pd.read_sql_query(get_addr_q, ENGINE)["address_id"][0]

                # insert store
                insert_addr_q = f"""
                    insert into store (address_id)
                    values ({address_id})
                """
                insert_db(insert_addr_q, ENGINE)

                # insert mgr_store
                select_store_q = f"""
                    select *
                    from
                        store
                    where address_id={address_id};
                """
                selected_store_df = pd.read_sql_query(select_store_q, ENGINE)
                STORE_INFO = selected_store_df       
                store_id = selected_store_df["store_id"][0]
     
                mgr_id = selected_mgr_df["staff_id"][0]

                insert_mgr_store = f"""
                    insert into mgr_store (mgr_id, store_id)
                    values ({mgr_id}, {store_id})
                """
                insert_db(insert_mgr_store, ENGINE)
                MANAGER_BOOL = True
                return
            else:
                print("username already taken or password mismatch")
                return            


if __name__ == "__main__":
    os.system("clear")
    print(
        """ ____            _        _   ____            _                 
|  _ \ ___ _ __ | |_ __ _| | / ___| _   _ ___| |_ ___ _ __ ___  
| |_) / _ \ '_ \| __/ _` | | \___ \| | | / __| __/ _ \ '_ ` _ \ 
|  _ <  __/ | | | || (_| | |  ___) | |_| \__ \ ||  __/ | | | | |
|_| \_\___|_| |_|\__\__,_|_| |____/ \__, |___/\__\___|_| |_| |_|
                                    |___/                       """
    )

    engine = connect_to_database()
    engine.connect
    menu_selection = menu()

    if menu_selection == 1:
        login()
    elif menu_selection == 2:
        customer_register()
    elif menu_selection == 3:
        store_registration()
    
    if not USER_INFO.empty:
        if MANAGER_BOOL:
            get_mgr_command(ENGINE, USER_INFO)
        else:
            get_customer_command(ENGINE, USER_INFO)


    