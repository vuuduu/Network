"""
File:          switchboard.py
Author         Vu Nguyen
Date:          12/4/2020
Section:       31
Description:   This is a Switch Board file that contain a
               Switch Board class
"""

"""
    Switchboard class

"""


class Switchboard:
    def __init__(self, area_code):
        """
        :param area_code: the area code to which the switchboard will be associated.
        """
        self.area_code = area_code
        self.phone_list = []  # string of number (no area code)
        self.trunk_connect = []  # object of other switchboard

    def add_phone(self, phone_number):
        """
        This function simply add the string of phone number to a list
        :param phone_number: phone number without area code
        :return: update the self.phone_list
        """
        self.phone_list.append(phone_number)

    def add_trunk_connection(self, switchboard):
        """
        This function add the object of other switchboard to
        self.trunk_connect. This indicate that there's a trunk
        line connecting between the two area code

        :param switchboard: should be either the area code or switchboard object to connect.
        :return: success/failure, None, or it's up to you
        """
        self.trunk_connect.append(switchboard)

    def connect_call(self, current_area_code, dest_number, previous_codes):
        """
        This must be a recursive function.

        :param current_area_code: the area code to which the destination phone belongs
        :param dest_number: the phone number of the destination phone without area code.
        :param previous_codes: list of already checked areas_code
        :return: True or False
        """
        if dest_number in current_area_code.phone_list:
            return True
        else:
            previous_codes.append(current_area_code.area_code)

            # This loop through all the possible trunk line connection
            # with the switch board
            for possible_a_code in current_area_code.trunk_connect:
                if possible_a_code.area_code not in previous_codes:
                    if possible_a_code.connect_call(possible_a_code, dest_number, previous_codes):
                        return True

            return False

    def jsonify(self):
        """
        Format style for each switch board
        {'area_code': {'Phone': [], 'Trunk_Connect': []}}
        """
        other_switch = []
        for trunk in self.trunk_connect:
            other_switch.append(trunk.area_code)

        return {self.area_code: {'Phone': self.phone_list, 'Trunk_Connect': other_switch}}


