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
    paper_node_dict = {}
    while True :  
        
        # for getting title
        
        line1 = paper_title_file_handle.readline()
        line1 = line1[:-1]
        line1 = line1.encode('ascii')
        if( line1 == '' ):
            break
        line_contents = line1.split('\t')            
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        title = line_contents[1]
        
        #for getting field
        
        seek_pos1 = paper_field_file_handle.tell()
        line2 = paper_field_file_handle.readline()
        line2 = line2[:-1]
        line2 = line2.encode('ascii')
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
        
        # for getting venue
        
        seek_pos2 = paper_venue_file_handle.tell()
        line3 =  paper_venue_file_handle.readline()
        line3 = line3[:-1]
        line3 = line3.encode('ascii')
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
        line4 = line4.encode('ascii')
        line_contents = line4.split('\t')
        year = line_contents[1]
             
        
        # for getting cited paper array
        
        while citer_id == paper_id:
            line5 = citation_file_handle.readline()
            line5 = line5[:-1]
            line5 = line5.encode('ascii')
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
        paper_node_dict[paper_id] = paper_node_object.object_to_json()
        cited_node_array = [ cited_paper_id ]
    return paper_node_dict
    
    citation_file_handle.close()
    paper_abstract_file_handle.close()
    paper_author_file_handle.close()
    paper_field_file_handle.close()
    paper_title_file_handle.close()
    paper_venue_file_handle.close()
    paper_year_file_handle.close()
    
    
    
    
def get_author_nodes():
    paper_author_file_handle = open(paper_authors, 'r')
    author_dict = {}
    for line in paper_author_file_handle:
        line_contents = line.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        open_bracket_pos = line_contents[1].index('[')
        close_bracket_pos = line_contents[1].index(']')
        author_id = line_contents[1][open_bracket_pos+1:close_bracket_pos]
        author_name = line_contents[1][:open_bracket_pos]
        try:
            author_id = int(author_id)
        except ValueError:
            continue
        if author_id in author_dict:
            author_dict[author_id]['Papers'].append( paper_id )
        else:
            author_dict[author_id] = {}
            author_dict[author_id]['Papers'] = [ paper_id ]
            author_dict[author_id]['Name'] = author_name
    return author_dict       
        
  
def get_venue_nodes():
    paper_venue_file_handle = open(paper_venue, 'r')
    venue_dict = {}
    for line in paper_venue_file_handle:
        line = line[:-1]
        line_contents = line.split('\t')
        try:
            paper_id = line_contents[0]
        except ValueError:
            continue
        venue = line_contents[1]
        if venue in venue_dict:
            venue_dict[ venue ].append( paper_id )
        else:
            venue_dict[ venue ] = [ paper_id ]
        
    return venue_dict

def get_field_nodes():       
    paper_field_file_handle = open(paper_fields, 'r')
    field_dict = {}
    for line in paper_field_file_handle:
        line = line[:-1]
        line_contents = line.split('\t')
        try:
            paper_id = line_contents[0]
        except ValueError:
            continue
        field = line_contents[1]
        if field in field_dict:
            field_dict[ field ].append( paper_id )
        else:
            field_dict[ field ] = [ paper_id ]
        
    return field_dict
        
        
        
    
    
    