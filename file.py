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
    def display_hotel_info(self, hotel_id): pass
    @abstractmethod
    def modify_hotel_info(self, hotel_id, new_name, new_rooms): pass
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

    def display_hotel_info(self, hotel_id = "all"):
        '''Function to display hotels info. from json master file.'''

        # Read existing hotels information from master file.
        with open(self.master_file, 'r') as m_file:
            master_list = json.load(m_file)

        # Check to see if there are not any registered hotels.
        if not master_list:
            print(f"\n The master file '{self.master_file}' does not have any registered hotels.")
            return

        # Determine which hotels to show based on hotel ID or if all are requested.
        if str(hotel_id).lower() == "all":
            display_list = master_list
        else:
            # Filter by the specific hotel ID and store info. in display list.
            display_list = [h for h in master_list if str(h.get('hotel_id')) == str(hotel_id)]

        # Check if the requested hotel ID exists.
        if not display_list:
            print(f"Error: No hotel found with ID '{hotel_id}'.")
            return

        # Get the hotel information from the list to be displayed and print.
        for hotel in display_list:
            h_id = hotel.get('hotel_id', 'N/A')
            name = hotel.get('name', 'N/A')
            loc = hotel.get('location', 'N/A')
            rooms = hotel.get('rooms', 0)
            print(f"Hotel ID: {h_id:<5} | Name: {name:<20} | Location: {loc:<20} | Total rooms: {rooms}")

        print(f"\nHotels displayed: {len(display_list)}.\n")

    def modify_hotel_info(self, hotel_id, new_name = None, new_rooms = None):
        '''Function to modify hotel name and number of rooms in json master file.'''

        try:
            # Read existing hotels information from master file.
            with open(self.master_file, 'r') as m_file:
                master_list = json.load(m_file)

            found = False
            for hotel in master_list:
                # Check/select the hotel to be modified by it hotel ID from master file.
                if str(hotel.get('hotel_id')) == str(hotel_id):
                    # Update hotel name.
                    if new_name:
                        hotel['name'] = new_name

                    # Update number of rooms in hotel.
                    if new_rooms is not None:
                        hotel['rooms'] = int(new_rooms)
                    found = True
                    break

            # Check to see if the hotel selected by its ID is valid.
            if not found:
                print(f"Error: Hotel ID '{hotel_id}' not found.")
                return

            # Store hotel info. changes.
            with open(self.master_file, 'w') as m_file:
                json.dump(master_list, m_file, indent=4)

            print(f"Success: Hotel ID '{hotel_id}' information updated.")

        # Error handling for invalid new rooms number.
        except ValueError:
            print("Error: The number of rooms must be a valid number.")


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

    # Checks command input to select hotel system feature.
    match command:
        case "create":
            #arg = sys.argv[2]
            system.create_hotel(arg)
        case "delete":
            #arg = sys.argv[2]
            system.delete_hotel(arg)
        case "display":
            system.display_hotel_info(arg)
        case "modify":
            # Checks command line whether only hotel name or rooms are to be modified.
            if len(sys.argv) == 4:
                h_id = sys.argv[2]
                val = sys.argv[3]

                # Check if the value is a number (rooms) or string (name).
                if val.isdigit():
                    system.modify_hotel_info(h_id, new_rooms = val)
                else:
                    system.modify_hotel_info(h_id, new_name = val)

            # Checks command line if hotel name and rooms will be modified.
            elif len(sys.argv) == 5:
                system.modify_hotel_info(sys.argv[2], sys.argv[3], sys.argv[4])

            # Error handling if no hotel ID was given or no value to be changed.
            else:
                print("Error: modify requires hotel ID and at least one value to change.")

if __name__ == '__main__':
    main()







