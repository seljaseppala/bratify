#!/usr/bin/python
# coding=<utf-8>

"""
    Bratify is a program that produces Brat-formatted class hierarchy and labels from an OWL file.

    Copyright (C) 2017  Selja Seppälä
    Email: selja.seppala.unige@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import rdflib, codecs, re
from rdflib.namespace import RDF
from collections import defaultdict
from construct_tree import construct_trees_by_TingYu


def pretty_to_file(d, f, indent=0):
    """ (dictionary of { str : str} dictionaries) -> NoneType

        Prints a class hierarchy in an open file f
        given the nested dictionary of dictionaries d.
        Each subclass level is indented with an extra tab.

        :param d: nested dictionary of dictionaries of { str : str}
        :param f: file open for writing
        :param indent: number of tabs for indenting subclass strings
        :return: NoneType
    """

    for key, value in d.iteritems():
        # print type(key), key

        f.write('\t' * indent + key.decode('utf-8') + '\n')

        if isinstance(value, dict):
            pretty_to_file(value, f, indent+1)
        else:
            if value is not None:
                f.write('\t' * (indent+1) + value.decode('utf-8') + '\n')


def format_label_for_brat_config(label):
    """ (str) -> str

        Replaces any character in the given label that does not comply with
        the brat annotation type format,
        which can only include alphanumeric characters ("a"-"z", "A"-"Z", "0"-"9"),
        the hyphen ("-") and the underscore ("_") character.
        Returns a new brat-compliant label to be used in the brat annotation.conf file.

        :param label: str that is the original label of a class
        :return: str that is the label formatted for brat's internal system
    """

    brat_label = ''
    for char in label:
        if re.match(r'[a-zA-Z0-9_-]', char):#.encode('utf-8')):
            brat_label = brat_label + char
        else:
            brat_label = brat_label + '_'

    return brat_label


def print_labels_for_brat_visualization(label_list, path):
    """ (list or str) -> NoneType

        Prints in an output file with each element of the given label_list,
        where each element contains strings separated by a space, a pipe,
        and another space.
        For example: 'brat_label | class label | class_id'.
        The output is to be used in the brat visual.conf file
        to configure the labels shown to the annotators.

        :param label_list: list of labels
        :param path: path to output file
        :return: NoneType
    """

    f = codecs.open(path, 'w', encoding='utf-8')
    sorted_list = sorted(label_list, key=lambda s: s.lower())
    for label in sorted_list:
        # print label, type(label)
        f.write(label.decode('utf-8') + '\n')
    f.close()


def print_hierarchy_for_brat_config(child_parent_list, path):
    """ (list of str) -> NoneType

        From the classes in the given child_parent_list,
        creates a nested dictionary containing a class hierarchy
        and prints the hierarchy in a file.

        :param child_parent_list: list of child-parent pair strings
        :param path: path to output file
        :return: NoneType
    """

    #hierarchy_dict = defaultdict(lambda: defaultdict(dict))
    # hierarchy_dict = construct_trees_by_TingYu(child_parent_list)

    # Adapted from https://gist.github.com/aethanyc/8313640
    hierarchy_dict = defaultdict(dict)

    for child, parent in child_parent_list:
        # print child, parent
        hierarchy_dict[parent][child] = hierarchy_dict[child]

    # for k, v in hierarchy_dict.iteritems():
    #     print k, v

    # Find roots
    children, parents = zip(*child_parent_list)
    roots = set(parents).difference(children)
    # print roots

    hierarchy_out = {root: hierarchy_dict[root] for root in roots}

    f = codecs.open(path, 'w', encoding='utf-8')
    pretty_to_file(hierarchy_out, f, indent=0)
    f.close()


def sparql_for_child_parent_pairs(owl_path, query):
    """ (str) -> class
        Creates an RDF graph from the OWL file at the given owl_path and
        returns the result of a SPARQL query that gets
        the labels and IDs of classes in each child-parent pair.

        :param owl_path: str specifying path to owl file
        :return: list of labels and IDs of classes in child-parent pairs
    """

    graph = rdflib.Graph()
    graph = graph.parse(owl_path)

    child_parent_pairs = graph.query(query)
    print len(child_parent_pairs)
    return child_parent_pairs


def format_id_term(child_parent_pairs, output_style):
    """ <class 'rdflib.plugins.sparql.processor.SPARQLResult'> -> list of str, list of str

        Formats each label and id for each class in the given child_parent_pairs list
        in the SPARQLResult.
        Returns a list of labels formatted for the brat annotation.conf file and
        a list of labels formatted for the brat visual.conf file.

    :param child_parent_pairs: list of child-parent pairs in rdflib.plugins.sparql.processor.SPARQLResult
    :param output_style: a number specifying the selected brat output style
    :return: a list of formatted labels and a list of formatted child-parent pairs
    """
    print type(child_parent_pairs)

    label_list = []
    child_parent_list = []

    for row in child_parent_pairs:

        # Process children
        print row
        # print 'Class C:', row[0], type(row[0])
        child = row[0].encode('utf-8')
        # print '\t> Child:', type(child)
        child_brat = row[0].encode('utf-8')
        child_brat = format_label_for_brat_config(child_brat).encode('utf-8')
        # print '\t\t> Replaced C:', type(child_brat)
        # child_id = row[1].encode('utf-8').split('/')[-1]
        child_id = row[1].replace(':', '_').replace('#', '/').encode('utf-8').split('/')[-1]
        # print '\t\t\t> ID C:', type(child_id), child_id

        # Specify the output format of the child labels for brat's visualization.conf
        # 1 = brat_term_format | normal term format | ID
        # 2 = ID | normal term format
        if output_style == '1':
            child_output = (child_brat + ' | ' + child + ' | ' + child_id)#.encode('utf-8')
        elif output_style == '2':
            child_output = (child_id + ' | ' + child)#.encode('utf-8')
        # print 'C:', child_output, type(child_output)
        if child_output not in label_list:
            label_list.append(child_output)

        # Process parents
        # print 'Class P:', type(row[2])
        parent = row[2].encode('utf-8')
        # print '\t> Parent:', type(parent)
        parent_brat = row[2].encode('utf-8')
        parent_brat = format_label_for_brat_config(parent_brat).encode('utf-8')
        # print '\t\t> Replaced P:', type(parent_brat)
        # parent_id = row[3].encode('utf-8').split('/')[-1]
        parent_id = row[3].replace(':', '_').replace('#', '/').encode('utf-8').split('/')[-1]
        # print '\t\t\t> ID P:', type(parent_id), parent_id

        # Specify the output format of the parent labels for brat's visualization.conf
        # 1 = brat_term_format | normal term format | ID
        # 2 = ID | normal term format
        if output_style == '1':
            parent_output = (parent_brat + ' | ' + parent + ' | ' + parent_id)#.encode('utf-8')
        elif output_style == '2':
            parent_output = (parent_id + ' | ' + parent)#.encode('utf-8')
        # print 'P:', parent_output, type(parent_output)
        if parent_output not in label_list:
            label_list.append(parent_output)

        # Specify the output format of the labels for brat's system
        if output_style == '1':
            child_parent_list.append([child_brat, parent_brat])
        elif output_style == '2':
            child_parent_list.append([child_id, parent_id])

    return label_list, child_parent_list


def run_bratify(owl, query, visualization_path, annotation_path, output_style):
    """ Calls functions to extract child-parent class pairs from a given OWL file
        using the given SPARQL query,
        format their labels and IDs according to brat configuration specifications, and
        output the formatted labels in two separate files, which location is given by
        visualization_path and annotation_path.

        :param owl: path to owl file
        :param visualization_path: path to output file for brat visualization labels
        :param annotation_path: path to output file for brat annotation labels
        :return: NoneType
    """
    # 1. Get child-parent class pairs from a given owl file using the given SPARQL query
    print "Running step 1"
    child_parent_pairs = sparql_for_child_parent_pairs(owl, query)

    # 2. Format their labels and IDs according to brat configuration specifications
    print "Running step 2"
    label_list, child_parent_list = format_id_term(child_parent_pairs, output_style)

    # 3. Output the formatted labels in two separate files,
    #    which location is given by visualization_path and annotation_path
    print "Running step 3"
    print_labels_for_brat_visualization(label_list, visualization_path)
    print '----------------\n'

    print_hierarchy_for_brat_config(child_parent_list, annotation_path)
    print '----------------\n'


