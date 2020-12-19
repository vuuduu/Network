"""
File:          network.py
Author         Vu Nguyen
Date:          12/7/2020
Section:       31
Description:   This is a file contain a main program and network class
               that'll execute all the basic function of both Phone and
               Switchboard
"""

"""
network.py is both the definition file for the Network class as well as the driver for the program.

In network you need to implement the functions which the driver will call for the all the different commands.
"""

from phone import Phone
from switchboard import Switchboard
import json
"""
import json
import csv (you can do either if you choose, or just use the regular file io)

Some constants below are for the driver, don't remove them unless you mean to.  
"""

HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'
TRUNK_CONNECT = 'Trunk_Connect'
PHONE = 'Phone'


class Network:
    def __init__(self):
        """
            Construct a network by creating the switchboard container object

            You are free to create any additional data/members necessary to maintain this class.
        """

        # extra
        self.switch_board = []  # object switchboard
        self.network_info = {}  # This is where I'll dump everything into a json file
        self.connectable = False

    def load_network(self, filename):
        """
        :param filename: the name of the file to be loaded.  Assume it exists and is in the right format.
                If not, it's ok if your program fails.
        :return: updated the new self.network_info and self.switch_board
        """
        with open(filename, 'r') as json_file:
            json_reader = json.load(json_file)

            area_code_info = {}
            the_entire_file = {}

            # This reset and re-append the switch_board from file and add the info the the phone and trunk_line.
            self.switch_board = []
            for a_c in json_reader:
                switch_board = Switchboard(a_c)
                self.switch_board.append(switch_board)

                # The sub info of the self.network (includes Phone and Trunk Connect)
                area_code_info[PHONE] = [Phone(phone_num, switch_board) for phone_num in json_reader[a_c][PHONE]]
                area_code_info[TRUNK_CONNECT] = [trunk_line for trunk_line in json_reader[a_c][TRUNK_CONNECT]]

                the_entire_file[a_c] = area_code_info

                area_code_info = {}

            # Go through each one of the area_code from a new dictionary
            for area_c in the_entire_file:

                # This set up the switch_board for checking.
                checking_area_code = None
                for sw_bo in self.switch_board:
                    if sw_bo.area_code == area_c:
                        checking_area_code = sw_bo

                # Checking through other connect area_code and adding it to the checking_area_code.
                for trunk_code in the_entire_file[area_c][TRUNK_CONNECT]:
                    for sw_bo in self.switch_board:
                        if sw_bo.area_code == trunk_code:
                            checking_area_code.add_trunk_connection(sw_bo)

                for phone_num in the_entire_file[area_c][PHONE]:
                    checking_area_code.add_phone(phone_num.number)

            self.network_info = the_entire_file

    def save_network(self, filename):
        """
        the format: {'area_code': {'Phone': [strings of phone number w/o area_code], 'Trunk Connect':
                                   [strings of other area_code that connect through a trunk line]}}

        :param filename: the name of your file to save the network.  Remember that you need to save all the
            connections, but not the active phone calls (they can be forgotten between save and load).
            You must invent the format of the file, but if you wish you can use either json or csv libraries.
        :return: put all of the infomation from the_entire_info into a json file.
        """
        with open(filename, 'w') as json_file:

            the_entire_info = {}
            for switch_board in self.switch_board:
                the_entire_info.update(switch_board.jsonify())

            json.dump(the_entire_info, json_file)

    def add_switchboard(self, area_code):
        """
        add switchboard should create a switchboard and add it to your network.

        By default it is not connected to any other boards and has no phone lines attached.
        :param area_code: the area code for the new switchboard
        :return: updated the self.network_info and self.switch_board
        """
        self.switch_board.append(Switchboard(area_code))
        self.network_info[area_code] = {PHONE: [], TRUNK_CONNECT: []}

    def adding_phone(self, a_code, phone_num):
        """
        :param a_code: The area code of the phone number that user want to add
        :param phone_num: the number w/o the area code
        :return: print the info and update the self.network_info
        """

        # This condition checks to see if the area code exist
        if a_code not in self.network_info:
            print(a_code, "doesn't exist")
        else:
            sw_bo = None

            # This condition find the switch board in the list.
            for switch_board in self.switch_board:
                if switch_board.area_code == a_code:
                    sw_bo = switch_board

            # This condition checks for duplication of phone number in same local switchboard
            if phone_num in sw_bo.phone_list:
                print("\tCan't add duplicated phone number in the same area code")
            else:
                self.network_info[a_code][PHONE].append(Phone(phone_num, sw_bo))  # Change
                sw_bo.add_phone(phone_num)
                print('\t', a_code + '-' + phone_num, 'successfully added')

    def connect_switchboards(self, area_1, area_2):
        """
            Connect switchboards should connect the two switchboards (creates a trunk line between them)
            so that long distance calls can be made.

        :param area_1: area-code 1
        :param area_2: area-code 2
        :return: success/failure
        """
        if area_1 not in self.network_info:
            print("\tCan't connect because", area_1, "doesn't exist")
        elif area_2 not in self.network_info:
            print("\tCan't connect because", area_2, "doesn't exist")
        else:

            # This loops through all the sb stores in the network to retrieve the two sb that needed to be connect.
            sw_bo_one = None
            sw_bo_two = None
            for switch_board in self.switch_board:
                if switch_board.area_code == area_1:
                    sw_bo_one = switch_board

                elif switch_board.area_code == area_2:
                    sw_bo_two = switch_board

            # This add the switchboard to the others trunk_connect list as an object.
            sw_bo_one.add_trunk_connection(sw_bo_two)
            sw_bo_two.add_trunk_connection(sw_bo_one)
            self.network_info[area_1][TRUNK_CONNECT].append(area_2)
            self.network_info[area_2][TRUNK_CONNECT].append(area_1)

            print("\tSuccessfully connected", area_1, 'with', area_2)

    def connecting_call(self, src_a_code, src_phone_num, dest_a_code, dest_phone_num):
        """
        This is a conditional helper function that checks whether if it's possible to connect
        two phone number to each other.

        :param src_a_code: the caller phone number's area code
        :param src_phone_num: the caller phone number w/o area code
        :param dest_a_code: the receiver phone number's area code
        :param dest_phone_num: the receiver phone number w/o area code
        :return: True or False
        """
        # Checks for the right start switch_board.
        for switch_board in self.switch_board:
            if switch_board.area_code == src_a_code:
                if switch_board.connect_call(switch_board, dest_phone_num, []):
                    self.connectable = True

        # This updated the phone busy attribute
        if self.connectable:
            first_phone = None
            second_phone = None
            # Assign phone object to two phone number.
            for a_c in self.network_info:
                if a_c in [src_a_code, dest_a_code]:

                    # This loop through all of the phone number a correct area_code
                    for phone_num in self.network_info[a_c][PHONE]:
                        if phone_num.number == src_phone_num:
                            first_phone = phone_num
                        elif phone_num.number == dest_phone_num:
                            second_phone = phone_num

            first_phone.connect(second_phone)
            second_phone.connect(first_phone)

        return self.connectable

    def disconnecting_call(self, area_code, phone):
        """
        :param area_code: the area_code of the phone that that want to disconnect
        :param phone: the phone number without area code
        :return: True or False
        """
        for a_c in self.network_info:
            if a_c == area_code:
                for phone_num in self.network_info[a_c][PHONE]:
                    if phone_num.number == phone:
                        return phone_num.disconnect()

    def display(self):
        """
            Display should output the status of the phone network as described in the project.
        """
        for a_code in self.network_info:
            print('Switchboard with area code: ', a_code)

            print('\tTrunk lines are: ')
            for trunk_line in self.network_info[a_code][TRUNK_CONNECT]:
                print('\t\tTrunk line connection to: ', trunk_line)

            print('\tLocal phone numbers are: ')
            for phone_num in self.network_info[a_code][PHONE]:
                print('\t\tPhone with number:', phone_num.number, end=' ')
                if not phone_num.busy:
                    print('is not in use')
                else:
                    print('is connected to', HYPHEN.join([phone_num.busy.switchboard.area_code, phone_num.busy.number]))


if __name__ == '__main__':
    the_network = Network()
    s = input('Enter command: ')

    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = split_command[1]
            area_2 = split_command[2]
            the_network.connect_switchboards(area_1, area_2)

        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            the_network.add_switchboard(split_command[1])

        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split(HYPHEN)
            a_code = number_parts[0]
            phone_number = ''.join(number_parts[1:])
            the_network.adding_phone(a_code, phone_number)

        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            the_network.save_network(split_command[1])
            print('\tNetwork saved to {}.'.format(split_command[1]))

        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            the_network.load_network(split_command[1])
            print('\tNetwork loaded from {}.'.format(split_command[1]))

        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = src_number_parts[0]
            src_number = ''.join(src_number_parts[1:])

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = dest_number_parts[0]
            dest_number = ''.join(dest_number_parts[1:])

            if the_network.connecting_call(src_area_code, src_number, dest_area_code, dest_number):
                print('\t', HYPHEN.join(src_number_parts), 'and', HYPHEN.join(dest_number_parts),
                      'are now connected.')
            else:
                print('\t', HYPHEN.join(src_number_parts), 'and', HYPHEN.join(dest_number_parts),
                      'were not connected.')

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split('-')
            area_code = number_parts[0]
            number = ''.join(number_parts[1:])

            if the_network.disconnecting_call(area_code, number):
                print('\tHanging up...\n\tConnection Terminated.')
            else:
                print("\tUnable to disconnect")

        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            the_network.display()

        s = input('Enter command: ')
