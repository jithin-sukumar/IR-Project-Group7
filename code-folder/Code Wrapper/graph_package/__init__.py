from util_classes import *
from global_variable_def import *
from util_functions import *
import json

paper_json_handle = open(paper_nodes_json, 'w')
paper_node_array = get_paper_nodes(  )

paper_nodes_object = {}
paper_nodes_object['Nodes'] = paper_node_array
paper_node_json_object = {}
paper_node_json_object['Paper'] = paper_nodes_object

#print paper_node_json_object
paper_json_handle.write( json.dumps( paper_node_json_object ) )  
paper_json_handle.close()