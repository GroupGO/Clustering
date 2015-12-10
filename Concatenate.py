#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A script designed to concatenate two tab-delimited, header and row-name -containing, expression
files, if their gene names/codes match.

    Inputs:     [1] A string specifying the path leading to the first expression file to be
                    concatenated.
                [2] A string specifying the path leading to the second expression file to be
                    concatenated.
                [3] A string specifying the path leading to the output file.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


from CommandLineParser import *
import datetime
import re
import os


def get_file_contents(file_path):
    """
    Function to extract the contents of a file to a list of lists of strings.

    :param file_path: A string specifying
    :return:
    """
    headers = []
    with open(file_path, 'r') as input_file:
        file_contents = []
        for index, line in enumerate(input_file):
            if index == 0:
                headers = line.split('\t')[1:]
                continue
            file_contents.append(line.strip().split('\t'))
    return file_contents, headers


def sort_file_contents(file_contents):
    file_contents.sort(key=lambda x: x[0])
    return file_contents


def remove_pattern(file_contents, pattern):
    """
    Function to replace a given pattern with 'CRO_' in the first column of each row of the
    second's file-contents and return it.

    :param file_contents: A list of lists containing the line-by-line contents of the second file.
    :param pattern: A string specifying the substring to be replaced with 'CRO_'.
    :return: The file_contents' list of lists.
    """
    sub_pattern, replacement = re.compile(pattern), 'CRO_'
    for index, row in enumerate(file_contents):
        file_contents[index][0] = sub_pattern.sub(replacement, row[0])
    return file_contents


def concatenate_files(file_one, file_contents, file_headers, output_file):
    """
    Method to concatenate two files and write it line by line to an output file.

    :param file_one: A string specifying the path to one of the two files to be combined.
    :param file_contents: A list of lists containing the contents of the second of the two files
    to be combined.
    :param file_headers: A list of strings containing the headers/conditions of the second file.
    :param output_file: A string specifying the path to the output file to be written.
    """
    with open(file_one, 'r') as input_file:
        with open(output_file, 'w') as output_file:
            for index, line in enumerate(input_file):
                line = line.strip()
                if index == 0:
                    write_header(output_file, line, file_headers)
                else:
                    if not write_gene_line(output_file, line, file_contents):
                        write_zero_expression(output_file, file_contents, line)


def write_header(output_file, line, file_headers):
    """
    Method to write to concatenate the headers of both files and write them to an output file.

    :param output_file: An open output file.
    :param line: A single line of the file to be appended to, containing its gene names and
    expression values, tab delimited.
    :param file_headers: A list of strings containing the conditions of the file to be appended.
    """
    output_file.write('%s\t' % line)
    for index, header in enumerate(file_headers):
        output_file.write(header.strip())
        if index < (len(file_headers) - 1):
            output_file.write('\t')
    output_file.write('\n')


def write_gene_line(output_file, line, file_contents):
    """
    Method to write a single line of concatenated expression provided the header exists in both
    files.

    :param output_file: An open output file.
    :param file_contents: A list of lists containing the contents of the file to be appended,
    in the form of a gene name and its expression values under different conditions.
    :param line: A single line of the file to be appended to, containing its gene names and
    expression values, tab delimited.
    :return: [True/False] depending on whether the function found a matching gene name between
    files or not.
    """
    current_gene = line.split('\t')[0]

    for row in file_contents:
        if row[0] == current_gene:
            output_file.write('%s\t' % line)
            for index, column in enumerate(row[1:]):
                output_file.write(column)
                if index < (len(row[1:]) - 1):
                    output_file.write('\t')
            output_file.write('\n')
            return True
    return False


def write_zero_expression(output_file, file_contents, line):
    """
    Method for appending zero expression to the first set of expressions.

    :param output_file: An open output file.
    :param file_contents: A list of lists containing the contents of the file to be appended,
    in the form of a gene name and its expression values under different conditions.
    :param line: A single line of the file to be appended to, containing its gene names and
    expression values, tab delimited.
    """
    output_file.write('%s\t' % line)
    for index, column in enumerate(['0'] * len(file_contents[0][1:])):
        output_file.write(column)
        if index < (len(file_contents[0][1:]) - 1):
            output_file.write('\t')
    output_file.write('\n')


def main():
    """
    Method to concatenate two tab-delimited expression files.
    :return:
    """
    file_one_path, file_two_path, output_path =\
        get_command_line_arguments(
            ['/home/ehler002/project/groups/go/Data/Cluster_Data/Dataset.txt',
             '/home/ehler002/project/groups/go/Data/Cluster_Data/translated_genes.fpkm_table',
             '/home/ehler002/project/groups/go/Data/Cluster_Data/Full_fpkm_Table.txt'])
    pattern = 'CRO_T'
    for file_path in [file_one_path, file_two_path]:
        assert os.path.exists(file_path), 'File %s does not exist.' % file_path
    start_time = datetime.datetime.now()
    print('Started concatenation at %s' % start_time)
    file_contents, headers = get_file_contents(file_two_path)
    file_contents = sort_file_contents(file_contents)
    file_contents = remove_pattern(file_contents, pattern)
    concatenate_files(file_one_path, file_contents, headers, output_path)
    print('Finished concatenation in %s' % (datetime.datetime.now() - start_time))


if __name__ == '__main__':
    main()
