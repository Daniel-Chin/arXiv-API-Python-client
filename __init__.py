import typing as tp
from contextlib import contextmanager
import json

import requests
import atoma

from cache import Cache

ENDPOINT = 'http://export.arxiv.org/api/query'

@contextmanager
def ArxivAPI():
    with Cache() as (getCache, setCache):
        def query(
            search_query: str | None = None, 
            id_list: tp.List[str] | None = None,
            start: int | None = None, 
            max_results: int | None = None,
        ):
            id_list_str = ','.join(sorted(id_list)) if id_list is not None else None
            params = {}
            if search_query is not None:
                params['search_query'] = search_query
            if id_list_str is not None:
                params['id_list'] = id_list_str
            if start is not None:
                params['start'] = start
            if max_results is not None: 
                params['max_results'] = max_results
            cache_key = json.dumps(params)
            try:
                return getCache(cache_key)
            except KeyError:
                pass
            res = requests.get(
                ENDPOINT,
                params=params,
            )
            assert res.status_code == 200
            feed = atoma.parse_atom_bytes(res.content)
            setCache(cache_key, feed)
            return feed
        
        yield query
