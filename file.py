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
    def create_hotel(self, new_data_file): pass
    @abstractmethod
    def delete_hotel(self, selected_id): pass
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

    # Master file initialization containing all hotels data.
    def __init__(self, master_file="master_hotels.json"):
        self.master_file = master_file

        # Check if master file exists, if not create a new one.
        if not os.path.exists(self.master_file):
            with open(self.master_file, 'w') as f:
                json.dump([], f)

    def create_hotel(self, new_data_file):
        '''Function to create hotel data into master file.'''

        try:
            # Read new hotel data from provided json file.
            with open(new_data_file, 'r') as s_file:
                new_hotels = json.load(s_file)

            # Read existing hotel data from master file.
            with open(self.master_file, 'r') as m_file:
                master_list = json.load(m_file)

            # Get all existing hotel IDs.
            existing_ids = {h.get('hotel_id') for h in master_list}
            added_count = 0 # New hotels count initialization.

            # Check to see if hotel data from provided file is new by hotel ID.
            for hotel in new_hotels:
                if hotel.get('hotel_id') not in existing_ids:
                    master_list.append(hotel)
                    added_count += 1

            # Write hotel data into json master file.
            with open(self.master_file, 'w') as m_file:
                json.dump(master_list, m_file, indent=4)

            print(f"Import finished: {added_count} new hotels added to {self.master_file}.")

        # Error handling if source file is not found.
        except FileNotFoundError:
            print(f"Error: Source file '{new_data_file}' not found.")

        # Error handling if json file data is invalid.
        except json.JSONDecodeError:
            print(f"Error: '{new_data_file}' is not a valid JSON file.")

    def delete_hotel(self, selected_id):
        '''Function to delete hotels by hotel ID from master file.'''

        # Read existing hotel data from json master file.
        with open(self.master_file, 'r') as m_file:
            master_list = json.load(m_file)

        # Initialization of length to keep track of hotel entries.
        initial_count = len(master_list)
        # Filter to keep all hotels except the hotel selected to be deleted.
        updated_list = [h for h in master_list if str(h.get('hotel_id')) != str(selected_id)]

        # Error handling by comparing hotel entries to check if a hotel has been deleted.
        if len(updated_list) == initial_count:
            print(f"Error: Hotel ID '{selected_id}' not found in {self.master_file}.")
            return

        # Store updated hotel data in json master file.
        with open(self.master_file, 'w') as m_file:
            json.dump(updated_list, m_file, indent=4)

        print(f"Success: Hotel with ID '{selected_id}' has been deleted.")

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

    command = sys.argv[1]
    arg = sys.argv[2]

    if command == "create":
        system.create_hotel(arg)
    elif command == "delete":
        system.delete_hotel(arg)

    '''
    tc = sys.argv[1] # Test case file with hotel data.
    system.create_hotel(tc)
    '''

if __name__ == '__main__':
    main()







