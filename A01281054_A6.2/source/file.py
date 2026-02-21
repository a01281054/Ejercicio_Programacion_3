# pylint: disable=invalid-name
'''

This program gathers hotel and customer data to create reservations
as a hotel management system. It can create files with hotel,
customer and reservation information, as well as modify it and
delete it.
'''

from abc import ABC, abstractmethod


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




