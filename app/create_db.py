try:
    import yaml as y
    from psycopg2 import connect as pgcnx, ProgrammingError
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:
    raise ImportError('Exteral Modules not installed.')

try:
    from model import cfg
except Exception as err:
    sys.exit(err)

urx = 'postgresql://' +cfg['datastore']['uid']+ ':' +cfg['datastore']['pwd']+ '@' +cfg['datastore']['host']+ ':' +str(cfg['datastore']['port'])+ '/' +cfg['datastore']['db']
dbn = cfg['datastore']['db']

def dbOps(urx,q,write=False,iso_level=False):
    pgx=pgcnx(urx)
    try:
        if iso_level:
            pgx.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        pgcur=pgx.cursor()
        x=pgcur.execute(q)
    except DuplicateObj as err:
            print(err)
    try:
        x=pgcur.fetchall()
    except ProgrammingError as err:
            x=False
    if write:
        pgx.commit()
    pgcur.close()
    pgx.close()
    return x

d = dbOps(uri,"SELECT datname FROM pg_database WHERE datname='" +dbn+ "'")
if len(d)>0:
    dbb=d[0][0]
    if dbb==dbn:
        print('Database ' +dbn+ ' already exits.')
else:
    nuDB=dbOps(uri,'CREATE DATABASE ' +dbn,iso_level=True)
    print('New Database created')
