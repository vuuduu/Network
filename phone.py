"""
File:          phone.py
Author         Vu Nguyen
Date:          12/4/2020
Section:       31
Description:   This is a phone file that contain a
               phone class
"""

"""
    This code defines the basic functionality that you need from a phone.
    When these functions are called they should communicate with the
    switchboards to find a path
"""


class Phone:
    def __init__(self, number, switchboard):
        """
        :param number: the phone number without area code
        :param switchboard: the switchboard to which the number is attached.
        """
        self.number = number
        self.switchboard = switchboard
        self.busy = None

    def connect(self, other_phone_number):
        """
        :param other_phone_number: the other phone number without the area code
        :return: **this you must decide in your implementation**
        """
        self.busy = other_phone_number  # other_phone_number is object.

    def disconnect(self):
        """
        This function should return the connection status to disconnected.  You need
        to use new members of this class to determine how the phone is connected to
        the other phone.

        You should also make sure to disconnect the other phone on the other end of the line.
        :return: True or False
        """
        if self.busy:
            self.busy.busy = None
            self.busy = None
            return True
        else:
            return False

