#!/usr/bin/python
# coding=<utf-8>

from bratify_owl import run_bratify


"""
    Bratify is a program that produces Brat-formatted class hierarchy and labels from an OWL file.
    
    Usage: edit the template below and run the program.
    
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


def name_of_ontology():
    # Specify the paths to:
    # - the input OWL file
    # - the output file formatted for brat visual.conf
    # - the output file formatted for brat annotation.conf
    owl = "./path_to/owl_file.owl"
    visualization_path = "./for_configuration_files/labels_for_visualization.txt"
    annotation_path = "./for_configuration_files/hierarchy_for_annotation.txt"

    # Specify the output format of the labels for Brat's system and for visualization.conf
    # 1 = brat_syst_format | normal term format | ID
    # 2 = ID | normal term format
    output_style = "1"

    # Specify the SPARQL query to get the labels and the PURLs for each class in the OWL file
    query = """ SELECT DISTINCT ?child_label ?child_id ?parent_label ?parent_id
                WHERE {
                    ?child rdfs:subClassOf ?parent .
                    ?child a owl:Class .
                    ?parent a owl:Class .
                    ?child rdfs:label ?child_label .
                    ?parent rdfs:label ?parent_label .
                    ?child oboInOwl:id ?child_id .
                    ?parent oboInOwl:id ?parent_id .

                    FILTER ( ?parent != ?child )
                }
                #LIMIT 10
            """

    # Run bratify.py for the specified ontology
    run_bratify(owl, query, visualization_path, annotation_path, output_style)


if __name__ == '__main__':
    name_of_ontology()

