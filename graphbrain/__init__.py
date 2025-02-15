from contextlib import contextmanager

from graphbrain.hyperedge import hedge
import graphbrain.memory.sqlite

try:
    import graphbrain.memory.leveldb
    LEVELDB = True
except ImportError:
    LEVELDB = False


def hgraph(locator_string):
    """Returns an instance of Hypergraph identified by the locator_string.
    The hypergraph will be created if it does not exist.

    The location_string can be the path to an SQLite3 file or LevelDB folder.
    """
    filename_parts = locator_string.split('.')
    if len(filename_parts) > 1:
        extension = filename_parts[-1]
        if extension in {'sqlite', 'sqlite3', 'db'}:
            return graphbrain.memory.sqlite.SQLite(locator_string)
        elif extension in {'leveldb', 'hg'}:
            if LEVELDB:
                return graphbrain.memory.leveldb.LevelDB(locator_string)
            else:
                raise RuntimeError(
                    'LevelDB not supported. Custom build required.')
    raise RuntimeError('Unknown hypergraph database type.')


@contextmanager
def hopen(*args, **kwds):
    hg = hgraph(*args, **kwds)
    hg.begin_transaction()
    hg.batch_mode = True
    try:
        yield hg
    finally:
        hg.batch_mode = False
        hg.end_transaction()
