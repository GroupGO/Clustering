#!/usr/bin/env python


"""
Author: Henry Ehlers
A class responsible for parsing strings to and from the command line.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation:
    https://www.python.org/dev/peps/pep-0008/
This allows for longer, more descriptive variable and function names, as well as more extensive
doc-strings.

"""


import subprocess
import sys


def get_variable_command_line_arguments(start_index):
    """
    Function to return a variable number of input arguments from the command line as of a
    certain index.

    :param start_index: The index of the first variable input argument on the command line.
    :return: A list of the parsed command line arguments.
    """
    variable_inputs = ['']*(len(sys.argv[:]) - start_index)
    for index, argument in enumerate(sys.argv[start_index:len(sys.argv)]):
        variable_inputs[index] = argument
    return variable_inputs


def get_command_line_arguments(default_variable_values):
    """
    Function to get a variable number of input arguments from the command line, but use default
    values if none were given.

    :param default_variable_values: A list of default values given in order of their appearance in
    the command line.
    :return: A list of input variables.
    """
    assert isinstance(default_variable_values, list), \
        'The given default input variables values must be a list.'
    input_variables = [0]*len(default_variable_values)
    for index, default_value in enumerate(default_variable_values):
        try:
            input_variables[index] = sys.argv[index + 1]
        except IndexError:
            if default_value != '':
                input_variables[index] = default_value
            else:
                exit('Not enough command line input arguments. Critical Input Missing.')
    return input_variables


def execute_on_command_line(cmd_string):
    """
    Method to parse a formatted string to the command line and execute it.

    :param cmd_string: The formatted string to be executed.
    """
    assert isinstance(cmd_string, str), 'Command Line String must be of type string.'
    subprocess.check_call(cmd_string, shell=True)
