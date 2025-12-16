import re
import json
import requests
from typing import Any, Dict, List
import re
import json
import requests
from typing import Any, Dict, List, Union

WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"
USER_AGENT = "WikidataClient/1.0 (https://github.com/ukaea/fuel)"


def wikidata_fetch(params: Dict[str, str]) -> Union[Dict[str, Any], str]:
    """Fetch data from the Wikidata API with error handling."""
    try:
        resp: requests.Response = requests.get(WIKIDATA_API_URL, params=params, headers={"User-Agent":USER_AGENT}, timeout=10)
        
        if resp.status_code == requests.codes.ok:
            return resp.json()
        else:
            return f"HTTP {resp.status_code}: {resp.content}"
    except requests.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


def wikidata_search(query: str) -> List[Dict[str, Any]]:
    """Search Wikidata for a query string and return entities with their types."""
    if not query:
        return []


    # Build set of search terms: original + split tokens
    query_strings = {query, *re.split(r"[ _\-\+\*\(\)\[\]]", query)} - {''}

    # Collect raw search results
    search_results: set[str] = set()
    for qs in query_strings:
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'search': qs,
            'language': 'en'
        }
        res = wikidata_fetch(params)        
                
        if isinstance(res, dict) and res.get('success'):
            for r in res.get('search', []):
                entry = {
                    'id': r['id'],
                    'url': r['url'],
                    'label': r.get('label', ''),
                    'aliases': r.get('aliases', []),
                    'description': r.get('description', ''),
                    'type': ''  # Will be filled later
                }
                search_results.add(json.dumps(entry))  # deduplicate

    if not search_results:
        return []

    # Deduplicate and map by ID
    results_list = [json.loads(r) for r in search_results]
    for r in results_list:
        r.setdefault("type", "")

    search_results_map = {r['id']: r for r in results_list}

    # Fetch entity details in one batch
    ids = '|'.join(search_results_map.keys())
    params = {
        'action': 'wbgetentities',
        'ids': ids,
        'format': 'json',
        'languages': 'en'
    }
    entities = wikidata_fetch(params)

    if isinstance(entities, dict) and 'entities' in entities:
    #if isinstance(entities, dict) and entities.get('success') and 'entities' in entities:
        type_ids: set[str] = set()
        ent_map = entities['entities']

        # Extract type IDs (P31) for each entity
        for eid, ent in ent_map.items():
            etype_id = (
                ent.get('claims', {})
                   .get('P31', [{}])[0]
                   .get('mainsnak', {})
                   .get('datavalue', {})
                   .get('value', {})
                   .get('id', '')
            )
            if etype_id:
                type_ids.add(etype_id)
                search_results_map[eid]['_type_id'] = etype_id  # temp

        # Batch fetch type labels
        if type_ids:
            type_params = {
                'action': 'wbgetentities',
                'ids': '|'.join(type_ids),
                'format': 'json',
                'languages': 'en'
            }
            type_entities = wikidata_fetch(type_params)
            if isinstance(type_entities, dict) and 'entities' in type_entities:
                for tid, tdata in type_entities['entities'].items():
                    etype_label = tdata.get('labels', {}).get('en', {}).get('value', '')
                    # Assign labels back to results
                    for ent in search_results_map.values():
                        if ent.get('_type_id') == tid:
                            ent['type'] = etype_label
                            del ent['_type_id']

    return list(search_results_map.values())


# -----------------
# Test harness
# -----------------
if __name__ == "__main__":
    test_queries = ["tokamak", "stellarator", "nuclear reactor"]

    for q in test_queries:
        print(f"\n=== Results for: {q} ===")
        results = wikidata_search(q)
        for r in results[:5]:  # show first 5 results for brevity        
            print(f"- {r['label']} ({r['id']})")
            print(f"  Type: {r['type']}")
            print(f"  Desc: {r['description']}")
            print(f"  URL : {r['url']}\n")

