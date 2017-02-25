import json
from global_variable_def import*    

def avquery(a,v):
    with open(author_nodes_json) as df:
        adata=json.load(df)


    ad=adata["Authors"]
    #print ad.keys()

    ani={} #author name to id dictionary
    for i in ad.keys():
        ani[ad[i]["Name"]]=i

    ap=[] #papers of author
    for i in ad[ani[a]]["Papers"]:
        ap.append(i)


    with open(venue_nodes_json) as df:
        vdata=json.load(df)
    vd=vdata["Venues"]
    vp=vd[v]
    '''
    print "author papers are: "
    print ap
    print "venue papers are: "
    print vp
    '''

    result = []
    for i in ap:
        if(i in vp):
            result.append(i)
    return result


if __name__== "__main__":
    v="European Symposium on Algorithms - ESA[680], pp. 488-499"
    a="Michael T. Hallett" 
    print avquery(a,v)
