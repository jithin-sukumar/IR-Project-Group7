from global_variable_def import *
from util_classes import *
import json

def string_cleaner(line):
    line = line[:-1]
    try:
        line = line.encode('ascii')
    except ValueError:
        line = line
    return line

def get_field_paper_dict():
    paper_field_file_handle = open(paper_fields, 'r')
    paper_field_dict = {}
    for line in paper_field_file_handle:
        line_contents = line.split('\t')
        line = string_cleaner( line )
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        if paper_id in paper_field_dict:
            paper_field_dict[ paper_id ].append( line_contents[1] )
        else:
            paper_field_dict[ paper_id ] = [ line_contents[1] ]
    paper_field_file_handle.close()
    return paper_field_dict

def is_pure_string( string ):
    for c in string:
        if( (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') ):
            continue
        else:
            return False
    return True

def create_paper_nodes(  ):
    citation_file_handle = open(citation_network, 'r')
    paper_abstract_file_handle = open(paper_abstract, 'r')
    paper_author_file_handle = open(paper_authors, 'r')
    paper_venue_file_handle = open(paper_venue, 'r')
    paper_title_file_handle = open(paper_title, 'r')
    paper_year_file_handle = open(paper_year, 'r')
    
    citer_id = 15
    cited_node_array = []
    author_array = []
    keywords_array = []
    
    field_paper_dict = get_field_paper_dict()
    paper_node_dict = {}
    while True :  
        
        # for getting title
        
        line1 = paper_title_file_handle.readline()
        line1 = string_cleaner(line1)
        if( line1 == '' ):
            break
        line_contents = line1.split('\t')            
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        title = line_contents[1]
        
        # for getting venue
        
        seek_pos2 = paper_venue_file_handle.tell()
        line3 =  paper_venue_file_handle.readline()
        line3 = string_cleaner(line3)
        line_contents = line3.split('\t')     
        try:
            temp_paper_id = int( line_contents[0] )
        except ValueError:
            continue
        if( temp_paper_id == paper_id ):
            venue = line_contents[1]
        else:
            
            paper_venue_file_handle.seek(seek_pos2)
        # for getting year
        
        seek_pos3 = paper_year_file_handle.tell()
        line4 =  paper_year_file_handle.readline()
        line4 = string_cleaner(line4)
        line_contents = line4.split('\t')     
        try:
            temp_paper_id = int( line_contents[0] )
        except ValueError:
            continue
        if( temp_paper_id == paper_id ):
            year = line_contents[1]
        else:
            paper_year_file_handle.seek(seek_pos3)
            continue
        
        # for getting cited paper array
        
        while citer_id == paper_id:
            line5 = citation_file_handle.readline()
            line5 = string_cleaner(line5)
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
        '''while temp_id == paper_id:
            line6 = paper_author_file_handle.readline()
            line6 = line6[:-1]
            if(line6 == ''):
                break
            line_contents = line6.split('\t')
            try:
                temp_id = int( line_contents[0] )
            except ValueError:
                continue
            try:
                open_bracket_pos = line_contents[1].index('[')
                close_bracket_pos = line_contents[1].index(']')
                author = line_contents[1][open_bracket_pos+1:close_bracket_pos]
                author = int(author)
            except ValueError:
                continue
            if( temp_id == paper_id):
                author_array.append( author )
        '''
                
        # for getting keywords
        '''line7 = paper_abstract_file_handle.readline()
        line7 = string_cleaner( line7 )
        line_contents = line7.split('\t')
        all_words = line_contents[1].split(' ')
        for i in all_words:
            if( len(i) > 3 and is_pure_string( i ) and i not in keywords_array ):
                keywords_array.append(i)
        '''
                
        # object creation  
        paper_node_object = paper_node(venue, field_paper_dict[paper_id], title, year, author_array, cited_node_array, keywords_array) 
        paper_node_dict[paper_id] = paper_node_object.object_to_json()
        cited_node_array = [ cited_paper_id ]
        #keywords_array = []
        #author_array = [ author ]
        #field_array = [ field ]
        print 'paper id completed : '+str(paper_id)
            
    citation_file_handle.close()
    paper_abstract_file_handle.close()
    paper_author_file_handle.close()
    paper_venue_file_handle.close()
    paper_title_file_handle.close()
    paper_year_file_handle.close()
    
    print 'files closed'
    paper_json_handle = open(paper_nodes_json, 'w')
    paper_nodes_json_object = {}
    paper_nodes_json_object['Papers'] = paper_node_dict
    json.dump( paper_nodes_json_object, paper_json_handle )  
    paper_json_handle.close()
  
    
def create_author_nodes():
    paper_author_file_handle = open(paper_authors, 'r')
    author_dict = {}
    curr_authors = []
    prev_id = 15
    paper_id = 15
    
    while prev_id == paper_id:
        line = paper_author_file_handle.readline()
        if(line == ''):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        prev_id = paper_id
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        try:
            open_bracket_pos = line_contents[1].index('[')
            close_bracket_pos = line_contents[1].index(']')
            author_id = line_contents[1][open_bracket_pos+1:close_bracket_pos]
            author_name = line_contents[1][:open_bracket_pos]
            author_id = int(author_id)
        except ValueError:
            author_id = -1
        if author_id in author_dict:
            author_dict[author_id]['Papers'].append( paper_id )
        elif( author_id != -1 ):
            author_dict[author_id] = {}
            author_dict[author_id]['Papers'] = [ paper_id ]
            author_dict[author_id]['Name'] = author_name
            author_dict[author_id]['Co Authors'] = {}
        if( paper_id == prev_id ):
            curr_authors.append( author_id )
        else:
            for i in range( 0, len( curr_authors ) ):
                if( curr_authors[i] == -1 ):
                    continue
                for j in range( 0, len( curr_authors ) ):
                    if( i == j or curr_authors[j] == -1 ):
                        continue
                    else:
                        if( curr_authors[j] in author_dict[curr_authors[i]]['Co Authors'] ):
                            author_dict[curr_authors[i]]['Co Authors'][curr_authors[j]] = author_dict[curr_authors[i]]['Co Authors'][curr_authors[j]] + 1
                        else:
                            author_dict[curr_authors[i]]['Co Authors'][curr_authors[j]] = 1   
            curr_authors = [ author_id ]
            prev_id = paper_id 
        print 'paper-author'+str( paper_id )
    paper_author_file_handle.close()
    
    author_json_handle = open( author_nodes_json, 'w' )
    author_nodes_json_object = {}
    author_nodes_json_object['Authors'] = author_dict
    json.dump( author_nodes_json_object , author_json_handle )
    author_json_handle.close()
        
  
def create_venue_nodes():
    paper_venue_file_handle = open(paper_venue, 'r')
    venue_dict = {}
    while True:
        line = paper_venue_file_handle.readline()
        if( line == '' ):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        try:
            paper_id = int(line_contents[0])
        except ValueError:
            continue
        venue = line_contents[1]
        if venue in venue_dict:
            venue_dict[ venue ].append( paper_id )
        else:
            venue_dict[ venue ] = [ paper_id ]
        print 'paper-venue'+str( paper_id )
    paper_venue_file_handle.close()    
    
    venue_json_handle = open( venue_nodes_json, 'w' )
    venue_nodes_json_object = {}
    venue_nodes_json_object['Venues'] = venue_dict
    json.dump( venue_nodes_json_object, venue_json_handle )
    venue_json_handle.close()


def create_field_nodes():       
    paper_field_file_handle = open(paper_fields, 'r')
    field_dict = {}
    while True:
        line = paper_field_file_handle.readline()
        if( line == '' ):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        field = line_contents[1]
        if field in field_dict:
            field_dict[ field ].append( paper_id )
        else:
            field_dict[ field ] = [ paper_id ]
        print 'paper-field'+str( paper_id )
    paper_field_file_handle.close()
        
    field_json_handle = open( field_nodes_json, 'w' )
    field_nodes_json_object = {}
    field_nodes_json_object['Fields'] = field_dict
    json.dump( field_nodes_json_object, field_json_handle )
    field_json_handle.close()

        
def create_year_nodes():
    paper_year_file_handle = open(paper_year, 'r')
    year_dict = {}
    while True:
        line = paper_year_file_handle.readline()
        if( line == '' ):
            break
        line = string_cleaner( line )
        line_contents = line.split('\t')
        try:
            paper_id = int( line_contents[0] )
        except ValueError:
            continue
        try:
            year = line_contents[1]
        except ValueError:
            continue
        if year in year_dict:
            year_dict[ year ].append( paper_id )
        else:
            year_dict[ year ] = [ paper_id ]
        print 'paper-year'+str( paper_id )
    paper_year_file_handle.close()
    
    year_json_handle = open( year_nodes_json, 'w' )
    year_nodes_json_object = {}
    year_nodes_json_object['Years'] = year_dict
    json.dump( year_nodes_json_object, year_json_handle )
    year_json_handle.close()
