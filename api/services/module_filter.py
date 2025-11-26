import json
import os
from rdflib import Graph, Namespace, Literal, XSD, URIRef
from typing import List, Dict

def run_query(module: str):
    graph = Graph()
    TTL_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'module_graph.ttl')
    graph.parse(TTL_PATH, format='turtle')
    query = '''
        PREFIX ex: <http://example.org/schema/>

        SELECT ?module_name
        WHERE {
            ?m a ex:Module ;
                ex:hasModuleName ?module_name ;
                ex:hasApplicationRange ?app_range .

            FILTER(strafter(str(?app_range), "/data/") = ?var)
        }
    '''
    result = graph.query(query, initBindings={'var': Literal(module)})
    cleaned_results = []
        
    cleaned_results: List[Dict[str, str]] = []
    for row in result:
        name = str(row["module_name"]).replace("[WS]", " ")
        cleaned_results.append({"module_name": name})

    return cleaned_results