from . import ArxivAPI

def test():
    with ArxivAPI() as (query, getCacheStats, clearCache):
        feed = query(id_list=['2107.05677'])
        print(getCacheStats())
        print(f'{type(feed) = }')
        import pdb; pdb.set_trace()

test()
