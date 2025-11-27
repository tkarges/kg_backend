import json
import os
import re
from rdflib import Graph, Namespace, Literal, XSD, URIRef
from typing import List, Dict

def parse_object_term(relation: str, obj: str):
    IN = Namespace('http://example.org/data/')
    base_url = 'http://example.org/data/'

    obj = obj.replace(' ', '[WS]')
    if relation == 'hasECTS':
        return Literal(int(obj), datatype=XSD.integer)
    
    if relation == 'taughtBy':
        obj = base_url + obj
        return URIRef(obj)
    
    if relation == 'hasLevel':
        return IN[obj]
    
    return Literal(obj)

def run_query(relation: str, obj: str):
    graph = Graph()
    TTL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'module_graph.ttl')
    graph.parse(TTL_PATH, format='turtle')
    query = f'''
        PREFIX ex: <http://example.org/schema/>

        SELECT ?module_name
        WHERE {{
            ?m a ex:Module ;
                ex:hasModuleName ?module_name ;
                ex:{relation} ?obj .

            FILTER(?obj = ?query_input)
        }}
    '''
    result = graph.query(query, initBindings={'query_input': parse_object_term(relation, obj)})
    cleaned_results = []
        
    cleaned_results: List[Dict[str, str]] = []
    for row in result:
        name = str(row["module_name"]).replace("[WS]", " ")
        cleaned_results.append({"module_name": name})

    return cleaned_results

def get_relation_range(relation: str):
    graph = Graph()
    TTL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'module_graph.ttl')
    graph.parse(TTL_PATH, format='turtle')
    query = f'''
        PREFIX ex: <http://example.org/schema/>

        SELECT DISTINCT ?range_item
        WHERE {{
            ?m a ex:Module ;
                ex:{relation} ?range_item .
        }}
    '''
    result = graph.query(query)
    cleaned_results = []
        
    cleaned_results: List[Dict[str, str]] = []
    for row in result:
        name = str(row["range_item"]).replace("[WS]", " ")
        if not re.match(r'http://', name) is None:
            name = name.lstrip('http://example.org/data/')
        cleaned_results.append({"module_name": name})

    return cleaned_results