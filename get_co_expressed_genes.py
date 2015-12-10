#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A script designed to find all clusters that contain any gene of interest.

    Inputs:     [1] Path leading to file containing clusters and genes within.
                [2] Path leading to a new-line delimited file containing the genes of interest.
                [3] Path leading to output file, which mirrors the structure of the cluster file.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


from CommandLineParser import *
import os


def find_co_expression_clusters(cluster_file, genes, output_file):
    """
    Method to find all clusters and their genes that contain certain genes of interest contained
    within a list. Found clusters are written to a tab and new-line delimited output file.

    :param cluster_file: A string specifying the file name containing the clusters and their genes.
    :param genes: A list of strings containing the names of the genes of interest.
    :param output_file: A string specifying the name of the output file to be written.
    """
    with open(output_file, 'w') as output_file:
        with open(cluster_file, 'r') as input_file:
            for line in input_file:
                line = line.strip().split('\t')
                cluster, gene_list = line[0], line[1]
                if check_gene_presence(gene_list, genes):
                    output_file.write('%s\t%s\n' % (cluster, gene_list))


def check_gene_presence(gene_list, genes):
    """
    Function to check whether any gene of interest is contained within a given list of genes.

    :param gene_list: A list of strings containing the genes of interest.
    :param genes: A list of strings containing the genes of a cluster.
    :return: [True/False] depending on whether a gene was found or not.
    """
    for gene in gene_list.split(','):
        if gene[0] == ' ':
            gene = gene[1:]
        if gene in genes:
            return True
    return False


def get_genes_from_file(gene_file, column):
    """
    Function to create a list of strings containing the contents of a new-line delimited file
    containing the genes of interest.

    :param gene_file: A string specifying the name of the new-line delimited file containing the
    genes of interest
    :param column: The column containing the gene codes/names of interest.
    :return: A list of strings containing the genes of the input file.
    """
    genes = []
    with open(gene_file, 'r') as input_file:
        for line in input_file:
            genes.append(line.strip().split('\t')[column])
    return genes


def main():
    """
    Method to find all co-expressed clusters and their genes.
    """
    cluster_file, gene_file, column, output_file = get_command_line_arguments(
        ['testing_cluster.txt', 'testing_genes.txt', '0', 'testing_output.txt'])
    assert os.path.exists(cluster_file), 'Cluster file %s does not exist.' % cluster_file
    assert os.path.exists(gene_file), 'Gene file %s does not exist.' % gene_file
    column = int(column)
    genes = get_genes_from_file(gene_file, column)
    find_co_expression_clusters(cluster_file, genes, output_file)


if __name__ == '__main__':
    main()
