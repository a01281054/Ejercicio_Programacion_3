# pylint: disable=invalid-name
'''
This program gathers hotel and customer data to create reservations
as a hotel management system. It can create files with hotel,
customer and reservation information, as well as modify it and
delete it.
'''

from abc import ABC, abstractmethod
import json
import sys
import os

from colorama.ansi import clear_screen


class Hotel(ABC):
    '''This abstract class defines the hotel functionality.'''

    @abstractmethod
    def create_hotel(self): pass
    @abstractmethod
    def delete_hotel(self): pass
    @abstractmethod
    def display_hotel_info(self): pass
    @abstractmethod
    def modify_hotel_info(self): pass
    @abstractmethod
    def reserve_room(self): pass
    @abstractmethod
    def cancel_reservation(self): pass


class Customer(ABC):
    '''This abstract class defines the customer functionality.'''

    @abstractmethod
    def create_customer(self): pass
    @abstractmethod
    def delete_customer(self): pass
    @abstractmethod
    def display_cust_info(self): pass
    @abstractmethod
    def modify_cust_info(self): pass


class Reservation(ABC):
    '''This abstract class defines the reservation functionality.'''

    @abstractmethod
    def create_reservation(self): pass
    @abstractmethod
    def cancel_reservation(self): pass


class HotelSystem(Hotel, Reservation):
    '''
    This class implements Hotel and Reservation as 2 abstractions.
    It manages the hotel information and the reservation logic.
    '''

    def __init__(self, master_file="master_hotels.json"):
        self.master_file = master_file

        # Initialize master file as an empty list if it doesn't exist
        if not os.path.exists(self.master_file):
            with open(self.master_file, 'w') as f:
                json.dump([], f)


    # Hotel information.
    def create_hotel(self, new_data_file):
        try:
            # 1. Read the unique source JSON file
            with open(new_data_file, 'r') as s_file:
                new_hotels = json.load(s_file)

            # Ensure we are dealing with a list
            if not isinstance(new_hotels, list):
                print(f"Error: {new_data_file} must contain a list of dictionaries.")
                return

            # 2. Read existing data from the master file
            with open(self.master_file, 'r') as m_file:
                master_list = json.load(m_file)

            # 3. Consolidate: Add the new list items to the master list
            # We use extend() to combine lists of dictionaries
            master_list.extend(new_hotels)

            # 4. Store: Save the updated list to the separate master file
            with open(self.master_file, 'w') as m_file:
                json.dump(master_list, m_file, indent=4)

            print(f"Import Successful: {len(new_hotels)} hotels added to {self.master_file}.")


        except FileNotFoundError:
            print(f"Error: Source file '{new_data_file}' not found.")

        except json.JSONDecodeError:
            print(f"Error: '{new_data_file}' is not a valid JSON file.")



    def delete_hotel(self): pass
    def display_hotel_info(self): pass
    def modify_hotel_info(self): pass
    def reserve_room(self): pass

    # Reservation system.
    def create_reservation(self): pass
    def cancel_reservation(self): pass


class CustomerSystem(Customer):

    def create_customer(self): pass
    def delete_customer(self): pass
    def display_cust_info(self): pass
    def modify_cust_info(self): pass


def main():
    system = HotelSystem()
    tc = sys.argv[1] # Test case file with hotel data.
    system.create_hotel(tc)

if __name__ == '__main__':
    main()







