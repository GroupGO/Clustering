#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A script designed to ...
    -input:
    -output:

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


import scipy.cluster.hierarchy as hier
import numpy


def main():
    array = numpy.array([[1, 1], [2, 1], [3, 3]])
    linkage_array = hier.linkage(array, method='single', metric='correlation')
    cluster = hier.fcluster(linkage_array, 1)
    hier.dendrogram(cluster)

if __name__ == '__main__':
    main()
