# arXiv API Python client
- A python client over export.arxiv.org  
- Provides a local cache store, invalidated at midnight Eastern Time.  
- Thread-safe.  

## todo
- catch API errors
  - rate limited
    - auto retry
  - http status codes
  - others

## Related repo
- https://github.com/lukasschwab/arxiv.py
  - Doesn't provide caching yet. 
- https://github.com/BalconyJH/aioarxiv/
  - Doesn't seem to provide caching yet. 

## References
- https://info.arxiv.org/help/api/user-manual.html
- https://info.arxiv.org/help/api/tou.html
