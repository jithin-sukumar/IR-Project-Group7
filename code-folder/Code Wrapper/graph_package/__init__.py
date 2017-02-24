from util_classes import *
from global_variable_def import *
from util_functions import *
import json

# PAPER NODES

paper_json_handle = open(paper_nodes_json, 'w')
paper_node_array = get_paper_nodes(  )
paper_nodes_json_object = {}
paper_nodes_json_object['Papers'] = paper_node_array
paper_json_handle.write( json.dumps( paper_nodes_json_object ) )  
paper_json_handle.close()

#VENUE NODES

venue_json_handle = open( venue_nodes_json, 'w' )
venue_nodes_json_object = {}
venue_nodes_json_object['Venues'] = get_venue_nodes()
venue_json_handle.write( json.dumps( venue_nodes_json_object ) )
venue_json_handle.close()

#AUTHOR NODES

author_json_handle = open( author_nodes_json, 'w' )
author_nodes_json_object = {}
author_nodes_json_object['Authors'] = get_author_nodes()
author_json_handle.write( json.dumps( author_nodes_json_object ) )
author_json_handle.close()

#FIELD NODES

field_json_handle = open( field_nodes_json, 'w' )
field_nodes_json_object = {}
field_nodes_json_object['Fields'] = get_field_nodes()
field_json_handle.write( json.dumps( field_nodes_json_object ) )
field_json_handle.close()

