# Bratify
Bratify is a program that produces Brat-formatted class hierarchy and labels from an OWL file.


## Running the program

#### Edit the following information in the `run_bratify.py` file (see example below).

#### Specify the paths to:
   * the input OWL file
   * the output file formatted for brat visual.conf
   * the output file formatted for brat annotation.conf
    
#### Specify the output format (`1` or `2`) of the labels for Brat's system and for visualization.conf.

`1` = `brat_syst_format | normal term format | ID`

For example:

    Matthew-Wood_syndrome | Matthew-Wood syndrome | DOID_0050819

`2` = `ID | normal term format` 

For example:

    DOID_0050819 | Matthew-Wood syndrome

#### Specify the SPARQL query to get the labels and the PURLs for each class in the OWL file.

#### Run bratify.py for the specified ontology by adding a call to the function.

## Example

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
        
## Output examples
    
#### Hierarchy

    DOID_4
        DOID_630
            DOID_0050177
                DOID_14793
                DOID_0050738
                DOID_0050739
                    DOID_0050736
                        DOID_14213
                        DOID_9467
                        DOID_14702

#### Labels
    
    DOID_0001816 | angiosarcoma
    DOID_0002116 | pterygium
    DOID_0014667 | disease of metabolism
    DOID_0050004 | seminal vesicle acute gonorrhea
    DOID_0050012 | chikungunya
    DOID_0050013 | carbohydrate metabolism disease
    DOID_0050025 | human granulocytic anaplasmosis
    DOID_0050026 | human monocytic ehrlichiosis
    DOID_0050032 | mineral metabolism disease
    DOID_0050035 | African tick-bite fever    