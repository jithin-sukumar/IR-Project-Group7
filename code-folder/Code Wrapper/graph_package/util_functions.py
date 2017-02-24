from global_variable_def import *
from util_classes import *
import json

def get_paper_nodes(  ):
    citation_file_handle = open(citation_network, 'r')
    paper_abstract_file_handle = open(paper_abstract, 'r')
    paper_author_file_handle = open(paper_authors, 'r')
    paper_field_file_handle = open(paper_fields, 'r')
    paper_title_file_handle = open(paper_title, 'r')
    paper_venue_file_handle = open(paper_venue, 'r')
    paper_year_file_handle = open(paper_year, 'r')
    
    citer_id = 15
    cited_node_array = []
    author_array = []
    keywords_array = []
    paper_node_array = []
    while True :  
        
        # for getting venue
        
        line1 = paper_title_file_handle.readline()
        line1 = line1[:-1]
        if( line1 == '' ):
            break
        line_contents = line1.split('\t')            
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        title = line_contents[1]
        
        #for getting field
        
        seek_pos1 = paper_venue_file_handle.tell()
        line2 = paper_field_file_handle.readline()
        line2 = line2[:-1]
        line_contents = line2.split('\t')
        try:
            temp_paper_id = int( line_contents[0] )
        except ValueError:
            continue
        if( temp_paper_id == paper_id ):
            field = line_contents[1]
        else:
            field = ''
            paper_field_file_handle.seek(seek_pos1)
        
        # for getting title
        
        seek_pos2 = paper_venue_file_handle.tell()
        line3 =  paper_venue_file_handle.readline()
        line3 = line3[:-1]
        line_contents = line3.split('\t')     
        try:
            temp_paper_id = int( line_contents[0] )
        except ValueError:
            continue
        if( temp_paper_id == paper_id ):
            venue = line_contents[1]
        else:
            venue = ''
            paper_venue_file_handle.seek(seek_pos2)
        
        # for getting year
        
        line4 = paper_year_file_handle.readline()
        line4 = line4[:-1]
        line_contents = line4.split('\t')
        year = line_contents[1]
             
        
        # for getting cited paper array
        
        while citer_id == paper_id:
            line5 = citation_file_handle.readline()
            line5 = line5[:-1]
            if(line5 == ''):
                break
            line_contents = line5.split('\t')
            try:
                citer_id =  int( line_contents[0] )
            except ValueError:
                continue
            try: 
                cited_paper_id =  int( line_contents[1] )
            except ValueError:
                continue
            if( citer_id == paper_id ):
                cited_node_array.append( cited_paper_id ) 
                
        # for getting author array
        
        
        
        
        # for getting keywords
        
        
        
        
        # object creation        
        paper_node_object = paper_node(venue, field, title, year, author_array, cited_node_array, keywords_array) 
        paper_node_array.append( paper_node_object.object_to_json() )
        cited_node_array = [ cited_paper_id ]
    return paper_node_array
    
    citation_file_handle.close()
    paper_abstract_file_handle.close()
    paper_author_file_handle.close()
    paper_field_file_handle.close()
    paper_title_file_handle.close()
    paper_venue_file_handle.close()
    paper_year_file_handle.close()
    