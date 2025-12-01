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
    
    if relation in ['taughtBy', 'offeredIn']:
        obj = base_url + obj
        return URIRef(obj)
    
    if relation == 'hasLevel':
        return IN[obj]
    
    return Literal(obj)

def parse_module_name(module: str):
    # base_url = 'http://example.org/data/'
    # module = module.replace(' ', '[WS]')
    # module = base_url + module
    # print(f'DEBUG: parsed module {module}')
    # return URIRef(module)
    name_in_graph = module.replace(" ", "[WS]")
    return Literal(name_in_graph, datatype=XSD.string)

def run_query(relation: str, module: str):
    print(f'DEBUG: function run_query in module_property_router entered with \n\tmodule: {module}\n\trelation: {relation}')
    graph = Graph()
    TTL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'module_graph.ttl')
    graph.parse(TTL_PATH, format='turtle')
    query = f'''
        PREFIX ex: <http://example.org/schema/>

        SELECT ?obj
        WHERE {{
            ?m a ex:Module ;
                ex:hasModuleName ?module_name ;
                ex:{relation} ?obj .

            FILTER(STR(?module_name) = ?query_input)
        }}
    '''
    print(f'DEBUG: query: {query}')
    result = graph.query(query, initBindings={'query_input': parse_module_name(module)})
    cleaned_results = []
        
    cleaned_results: List[Dict[str, str]] = []
    for row in result:
        print(f'DEBUG: module property result: {row}')
        name = str(row["obj"]).replace("[WS]", " ")
        if not re.match(r'http://', name) is None:
            name = name.lstrip('http://example.org/data/')
        cleaned_results.append({"module_property": name})

    return cleaned_results

def get_module_domain():
    graph = Graph()
    TTL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'module_graph.ttl')
    graph.parse(TTL_PATH, format='turtle')
    print('DEBUG: function get_module_domain entered')
    query = f'''
        PREFIX ex: <http://example.org/schema/>

        SELECT DISTINCT ?module_name
        WHERE {{
            ?m a ex:Module ;
                ex:hasModuleName ?module_name .
        }}
    '''
    result = graph.query(query)
    cleaned_results = []
        
    cleaned_results: List[Dict[str, str]] = []
    for row in result:
        name = str(row["module_name"]).replace("[WS]", " ")
        if not re.match(r'http://', name) is None:
            name = name.lstrip('http://example.org/data/')
        cleaned_results.append({"module_name": name})

    print(f'DEBUG: got {len(cleaned_results)} results')
    return cleaned_results