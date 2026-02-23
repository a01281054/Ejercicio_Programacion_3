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


class Hotel(ABC):
    '''This abstract class defines the hotel functionality.'''

    @abstractmethod
    def create_hotel(self, new_data_file):
        '''Abstract method to create a hotel entry from a JSON file.'''

    @abstractmethod
    def delete_hotel(self, selected_id):
        '''Abstract method to delete a hotel by its unique ID.'''

    @abstractmethod
    def display_hotel_info(self, hotel_id):
        '''Abstract method to display hotel info. by its unique ID.'''

    @abstractmethod
    def modify_hotel_info(self, hotel_id, new_name = None, new_rooms = None):
        '''Abstract method to modify hotel info. by its unique ID.'''

    @abstractmethod
    def reserve_room(self, hotel_id):
        '''Abstract method to reserve a hotel by decreasing available rooms
         by its unique ID.'''

    @abstractmethod
    def cancel_reservation(self, reservation_id,
                           res_file="master_reservations.json"):
        '''Abstract method to cancel hotel reservations by unique ID.'''


class Customer(ABC):
    '''This abstract class defines the customer functionality.'''

    @abstractmethod
    def create_customer(self, new_data_file):
        '''Abstract method to create customer into customers master file.'''

    @abstractmethod
    def delete_customer(self, selected_id):
        '''Abstract method to delete customer from customers master file.'''

    @abstractmethod
    def display_cust_info(self, customer_id):
        '''Abstract method to display customer info. from
        customers master file.'''

    @abstractmethod
    def modify_cust_info(self, customer_id,
                         new_name = None, new_email = None):
        '''Abstract method to modify customer info. of customers master file.'''


class Reservation(ABC):
    '''This abstract class defines the reservation functionality.'''

    @abstractmethod
    def create_reservation(self, customer_id, hotel_id,
                           customer_file="master_customers.json",
                           res_file="master_reservations.json"):
        '''Abstract method to create reservations using customers
        and hotel info. into a JSON master.'''

    @abstractmethod
    def cancel_reservation(self, reservation_id, res_file="master_reservations.json"):
        '''Abstract method to cancel reservations by unique ID.'''


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
            with open(self.master_file, 'w', encoding="utf-8") as f:
                json.dump([], f)

    def create_hotel(self, new_data_file):
        '''Function to create hotel data into master file.'''

        try:
            # Read new hotel data from provided json file.
            with open(new_data_file, 'r', encoding="utf-8") as s_file:
                new_hotels = json.load(s_file)

            # Read existing hotel data from master file.
            with open(self.master_file, 'r', encoding="utf-8") as m_file:
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
            with open(self.master_file, 'w', encoding="utf-8") as m_file:
                json.dump(master_list, m_file, indent=4)

            print(f"Import finished: {added_count} new hotels added to {self.master_file}.\n")

        # Error handling if source file is not found.
        except FileNotFoundError:
            print(f"Error: Source file '{new_data_file}' not found.\n")

        # Error handling if json file data is invalid.
        except json.JSONDecodeError:
            print(f"Error: '{new_data_file}' is not a valid JSON file.\n")

    def delete_hotel(self, selected_id):
        '''Function to delete hotels by hotel ID from master file.'''

        # Read existing hotel data from json master file.
        with open(self.master_file, 'r', encoding="utf-8") as m_file:
            master_list = json.load(m_file)

        # Initialization of length to keep track of hotel entries.
        initial_count = len(master_list)
        # Filter to keep all hotels except the hotel selected to be deleted.
        updated_list = [h for h in master_list if str(h.get('hotel_id')) != str(selected_id)]

        # Error handling by comparing hotel entries to check if a hotel has been deleted.
        if len(updated_list) == initial_count:
            print(f"Error: Hotel ID '{selected_id}' not found in {self.master_file}.\n")
            return

        # Store updated hotel data in json master file.
        with open(self.master_file, 'w', encoding="utf-8") as m_file:
            json.dump(updated_list, m_file, indent=4)

        print(f"Success: Hotel with ID '{selected_id}' has been deleted.\n")

    def display_hotel_info(self, hotel_id = "all"):
        '''Function to display hotels info. from json master file.'''

        # Read existing hotels information from master file.
        with open(self.master_file, 'r', encoding="utf-8") as m_file:
            master_list = json.load(m_file)

        # Check to see if there are not any registered hotels.
        if not master_list:
            print(f"\n The master file '{self.master_file}' does not have any registered hotels.\n")
            return

        # Determine which hotels to show based on hotel ID or if all are requested.
        if str(hotel_id).lower() == "all":
            display_list = master_list
        else:
            # Filter by the specific hotel ID and store info. in display list.
            display_list = [h for h in master_list if str(h.get('hotel_id')) == str(hotel_id)]

        # Check if the requested hotel ID exists.
        if not display_list:
            print(f"Error: No hotel found with ID '{hotel_id}'.\n")
            return

        # Get the hotel information from the list to be displayed and print.
        for hotel in display_list:
            h_id = hotel.get('hotel_id', 'N/A')
            name = hotel.get('name', 'N/A')
            loc = hotel.get('location', 'N/A')
            rooms = hotel.get('rooms', 0)
            a_rooms = hotel.get('available_rooms', 0)
            print(f"Hotel ID: {h_id:<3} | Name: {name:<15} | Location: {loc:<15} | "
                  f"Available rooms: {a_rooms:<5} | Total rooms: {rooms}\n")

        print(f"\nHotels displayed: {len(display_list)}.\n")

    def modify_hotel_info(self, hotel_id, new_name = None, new_rooms = None):
        '''Function to modify hotel name and number of rooms in json master file.'''

        try:
            # Read existing hotels information from master file.
            with open(self.master_file, 'r', encoding="utf-8") as m_file:
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
                print(f"Error: Hotel ID '{hotel_id}' not found.\n")
                return

            # Store hotel info. changes.
            with open(self.master_file, 'w', encoding="utf-8") as m_file:
                json.dump(master_list, m_file, indent=4)

            print(f"Success: Hotel ID '{hotel_id}' information updated.\n")

        # Error handling for invalid new rooms number.
        except ValueError:
            print("Error: The number of rooms must be a valid number.\n")

    def reserve_room(self, hotel_id):
        '''Function to reserve a room in a hotel by decrementing the count in json master file.'''

        # Read existing hotels information from master file.
        with open(self.master_file, 'r', encoding="utf-8") as m_file:
            master_list = json.load(m_file)

        found = False
        # Check hotel by ID to make modification in available rooms count
        for hotel in master_list:
            if str(hotel.get('hotel_id')) == str(hotel_id):
                current_rooms = hotel.get('available_rooms', 0)

                # Check if there are available rooms, then make reservation
                if current_rooms > 0:
                    hotel['available_rooms'] = current_rooms - 1
                    found = True
                    print(f"Success: Room reserved at {hotel['name']}. "
                          f"Remaining rooms: {hotel['available_rooms']}.\n")

                # Error handling, display message when there are not any available rooms
                else:
                    print(f"Error: No rooms available at {hotel['name']}.\n")
                    return
                break

        if not found:
            print(f"Error: Hotel ID '{hotel_id}' not found.\n")
            return

        # Write back information to master file
        with open(self.master_file, 'w', encoding="utf-8") as m_file:
            json.dump(master_list, m_file, indent=4)

    # Reservation system.
    def create_reservation(self, customer_id, hotel_id, customer_file = "master_customers.json",
                           res_file = "master_reservations.json"):
        '''Function to create a reservation.'''

        # Validate the Customer exists in their own database
        with open(customer_file, 'r', encoding="utf-8") as cf:
            customers = json.load(cf)
        if not any(str(c.get('customer_id')) == str(customer_id) for c in customers):
            print(f"Error: Customer ID '{customer_id}' not found in {customer_file}.")
            return

        # Validate Hotel exists and has rooms
        with open(self.master_file, 'r', encoding="utf-8") as hf:
            hotels = json.load(hf)

        target_hotel = next((h for h in hotels if str(h.get('hotel_id')) == str(hotel_id)), None)

        if not target_hotel:
            print(f"Error: Hotel ID '{hotel_id}' not found.\n")
            return

        if target_hotel.get('available_rooms', 0) <= 0:
            print(f"Error: No rooms available at {target_hotel['name']}.\n")
            return

        # Perform the physical reservation in the hotel database.
        self.reserve_room(hotel_id)

        # Create the link in the reservations database
        if not os.path.exists(res_file):
            with open(res_file, 'w', encoding="utf-8") as f:
                json.dump([], f)

        with open(res_file, 'r', encoding="utf-8") as rf:
            reservations = json.load(rf)

        new_res = {
            "reservation_id": len(reservations) + 1,
            "customer_id": customer_id,
            "hotel_id": hotel_id,
            "hotel_name": target_hotel['name']
        }
        reservations.append(new_res)

        with open(res_file, 'w', encoding="utf-8") as rf:
            json.dump(reservations, rf, indent=4)

        print(f"Success: Reservation #{new_res['reservation_id']} "
              f"created for Customer {customer_id}.\n")


    def cancel_reservation(self, reservation_id, res_file="master_reservations.json"):
        '''Function to cancel a reservation and return the room to the hotel inventory.'''

        # Check existing reservations.
        if not os.path.exists(res_file):
            print(f"Error: No reservations found in {res_file}.\n")
            return

        with open(res_file, 'r', encoding="utf-8") as rf:
            reservations = json.load(rf)

        # Find the reservation to get the hotel_id.
        res_to_cancel = next((r for r in reservations
                              if str(r.get('reservation_id')) == str(reservation_id)), None)

        if not res_to_cancel:
            print(f"Error: Reservation ID '{reservation_id}' not found.\n")
            return

        hotel_id = res_to_cancel.get('hotel_id')

        # Update Hotel Inventory (increment available_rooms).
        with open(self.master_file, 'r', encoding="utf-8") as hf:
            hotels = json.load(hf)

        for hotel in hotels:
            if str(hotel.get('hotel_id')) == str(hotel_id):
                hotel['available_rooms'] = hotel.get('available_rooms', 0) + 1
                break

        # Remove the selected reservation from the list
        updated_reservations = [r for r in reservations
                                if str(r.get('reservation_id')) != str(reservation_id)]

        # Save hotel master file and reservations master file.
        with open(self.master_file, 'w', encoding="utf-8") as hf:
            json.dump(hotels, hf, indent=4)

        with open(res_file, 'w', encoding="utf-8") as rf:
            json.dump(updated_reservations, rf, indent=4)

        print(f"Success: Reservation {reservation_id} cancelled. Room returned to inventory.\n")


class CustomerSystem(Customer):
    '''
    This class implements a system to manage customers information
    into a JSON file named master_customers. It has a list of
    dictionaries; the following information can be found in this
    file: customer_id, name, age, email.
    '''

    # Master file initialization containing all hotels data.
    def __init__(self, master_file="master_customers.json"):
        self.master_file = master_file

        # Check if master file exists, if not create a new one.
        if not os.path.exists(self.master_file):
            with open(self.master_file, 'w', encoding="utf-8") as f:
                json.dump([], f)

    def create_customer(self, new_data_file):
        '''Function to create customer data into master file.'''

        try:
            # Read new customer data from provided json file.
            with open(new_data_file, 'r', encoding="utf-8") as s_file:
                new_customers = json.load(s_file)

            # Read existing customer data from master file.
            with open(self.master_file, 'r', encoding="utf-8") as m_file:
                master_list = json.load(m_file)

            # Get all existing customer IDs.
            existing_ids = {c.get('customer_id') for c in master_list}
            added_count = 0  # New customer count initialization.

            # Check to see if hotel data from provided file is new by hotel ID.
            for customer in new_customers:
                if customer.get('customer_id') not in existing_ids:
                    master_list.append(customer)
                    added_count += 1

            # Write customer data into json master file.
            with open(self.master_file, 'w', encoding="utf-8") as m_file:
                json.dump(master_list, m_file, indent=4)

            print(f"Import finished: {added_count} new customers added to {self.master_file}.\n")

        # Error handling if source file is not found.
        except FileNotFoundError:
            print(f"Error: Source file '{new_data_file}' not found.\n")

        # Error handling if json file data is invalid.
        except json.JSONDecodeError:
            print(f"Error: '{new_data_file}' is not a valid JSON file.\n")


    def delete_customer(self, selected_id):
        '''Function to delete customers by customer ID from master file.'''

        # Read existing customer data from json master file.
        with open(self.master_file, 'r', encoding="utf-8") as m_file:
            master_list = json.load(m_file)

        # Initialization of length to keep track of customer entries.
        initial_count = len(master_list)
        # Filter to keep all customers except the customer selected to be deleted.
        updated_list = [c for c in master_list if str(c.get('customer_id')) != str(selected_id)]

        # Error handling by comparing customer entries to check if a customer has been deleted.
        if len(updated_list) == initial_count:
            print(f"Error: Customer ID '{selected_id}' not found in {self.master_file}.\n")
            return

        # Store updated customer data in json master file.
        with open(self.master_file, 'w', encoding="utf-8") as m_file:
            json.dump(updated_list, m_file, indent=4)

        print(f"Success: Customer with ID '{selected_id}' has been deleted.\n")

    def display_cust_info(self, customer_id="all"):
        '''Function to display customers info. from json master file.'''

        # Read existing customers information from master file.
        with open(self.master_file, 'r', encoding="utf-8") as m_file:
            master_list = json.load(m_file)

        # Check to see if there are not any registered customers.
        if not master_list:
            print(f"\n The master file '{self.master_file}' "
                  f"does not have any registered customers.\n")
            return

        # Determine which customers to show based on customer ID or if all are requested.
        if str(customer_id).lower() == "all":
            display_list = master_list
        else:
            # Filter by the specific customer ID and store info. in display list.
            display_list = [c for c in master_list if str(c.get('customer_id')) == str(customer_id)]

        # Check if the requested customer ID exists.
        if not display_list:
            print(f"Error: No customer found with ID '{customer_id}'.\n")
            return

        # Get the customer information from the list to be displayed and print.
        for customer in display_list:
            c_id = customer.get('customer_id', 'N/A')
            name = customer.get('name', 'N/A')
            age = customer.get('age', 0)
            email = customer.get('email', 'N/A')
            print(f"Customer ID: {c_id:<3} | Name: {name:<15} | Age: {age:<15} | "
                  f"Email: {email:<5}\n")

        print(f"\nCustomers displayed: {len(display_list)}.\n")

    def modify_cust_info(self, customer_id, new_name = None, new_email = None):
        '''Function to modify customers name and email in json master file.'''

        try:
            # Read existing customers information from master file.
            with open(self.master_file, 'r', encoding="utf-8") as m_file:
                master_list = json.load(m_file)

            found = False
            for customer in master_list:
                # Check/select the customer to be modified by its customer ID from master file.
                if str(customer.get('customer_id')) == str(customer_id):
                    # Update customer name.
                    if new_name:
                        customer['name'] = new_name

                    # Update customer email.
                    if new_email:
                        customer['email'] = new_email
                    found = True
                    break

            # Check to see if the customer selected by its ID is valid.
            if not found:
                print(f"Error: Customer ID '{customer_id}' not found.\n")
                return

            # Store customer info. changes.
            with open(self.master_file, 'w', encoding="utf-8") as m_file:
                json.dump(master_list, m_file, indent=4)

            print(f"Success: Customer ID '{customer_id}' information updated.\n")

        # Error handling for invalid email.
        except ValueError:
            print("Error: Email must be a valid input.\n")




def main():
    '''Main function.'''
    system_hotel = HotelSystem()
    system_customer = CustomerSystem()

    command = sys.argv[1]
    hot_cust = sys.argv[2]

    # Checks command input to select hotel system feature.
    match command:
        case "create":
            arg = sys.argv[3]
            if hot_cust == "hotel":
                system_hotel.create_hotel(arg)
            elif hot_cust == "customer":
                system_customer.create_customer(arg)

        case "delete":
            arg = sys.argv[3]
            if hot_cust == "hotel":
                system_hotel.delete_hotel(arg)
            elif hot_cust == "customer":
                system_customer.delete_customer(arg)

        case "display":
            arg = sys.argv[3]
            if hot_cust == "hotel":
                system_hotel.display_hotel_info(arg)
            elif hot_cust == "customer":
                system_customer.display_cust_info(arg)

        case "modify":
            if hot_cust == "hotel":
                # ... your existing hotel modify logic ...
                if len(sys.argv) == 5:
                    h_id, val = sys.argv[3], sys.argv[4]
                    if val.isdigit():
                        system_hotel.modify_hotel_info(h_id, new_rooms=val)
                    else:
                        system_hotel.modify_hotel_info(h_id, new_name=val)
                elif len(sys.argv) == 6:
                    system_hotel.modify_hotel_info(sys.argv[3], sys.argv[4], sys.argv[5])

            elif hot_cust == "customer":
                # Logic for modifying customer (Name or Email)
                if len(sys.argv) == 5:
                    c_id, val = sys.argv[3], sys.argv[4]
                    # Since both are strings, we can check for an '@' to guess if it's an email
                    if "@" in val:
                        system_customer.modify_cust_info(c_id, new_email = val)
                    else:
                        system_customer.modify_cust_info(c_id, new_name = val)
                elif len(sys.argv) == 6:
                    # Modify both: python file.py modify customer <id> <name> <email>
                    system_customer.modify_cust_info(sys.argv[3], sys.argv[4], sys.argv[5])
                else:
                    print("Error: modify customer requires ID and at least one value.")

        case "reserve":
            arg = sys.argv[3]
            system_hotel.reserve_room(arg)

        case "book":
            if len(sys.argv) == 4:
                c_id = sys.argv[2]
                h_id = sys.argv[3]
                system_hotel.create_reservation(c_id, h_id)
            else:
                print("Error: book requires Customer ID and Hotel ID.\n")

        case "cancel":
            system_hotel.cancel_reservation(sys.argv[2])

if __name__ == '__main__':
    main()
