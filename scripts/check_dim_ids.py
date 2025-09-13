"""Script temporal para comprobar gaps/saltos en ids de dimensiones OLAP.
Uso: & .venv\Scripts\python.exe scripts/check_dim_ids.py
Requiere que .env tenga la conexión OLAP (OLAP_HOST, OLAP_USER, OLAP_PASSWORD, OLAP_DBNAME, OLAP_PORT)
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

OLAP = {
    'host': os.getenv('OLAP_HOST', 'localhost'),
    'user': os.getenv('OLAP_USER', 'postgres'),
    'password': os.getenv('OLAP_PASSWORD', ''),
    'dbname': os.getenv('OLAP_DBNAME', 'railway'),
    'port': int(os.getenv('OLAP_PORT', 5432)),
}

conn = psycopg2.connect(**OLAP)
cur = conn.cursor()

dimensions = [
    ('dim_producto', 'id_producto'),
    ('dim_envio', 'id_envio'),
    ('dim_metodo_pago', 'id_metodo_pago'),
]

for table, pk in dimensions:
    print('='*80)
    print(f"Checking {table}.{pk}")
    cur.execute(f"SELECT MIN({pk}) as min_id, MAX({pk}) as max_id, COUNT(*) as cnt FROM {table};")
    row = cur.fetchone()
    if not row:
        print('No data or table missing')
        continue
    min_id, max_id, cnt = row
    print(f"min={min_id} max={max_id} count={cnt}")
    if min_id is None:
        print('Table empty')
        continue
    # buscar gaps: ids que no están entre min..max
    cur.execute(f"SELECT {pk} FROM {table} ORDER BY {pk};")
    ids = [r[0] for r in cur.fetchall()]
    gaps = []
    prev = ids[0]
    for i in ids[1:]:
        if i != prev + 1:
            gaps.append((prev, i))
        prev = i
    if not gaps:
        print('No gaps detected')
    else:
        print('Gaps detected (prev -> next):')
        for g in gaps:
            print(g)
    # intentar identificar sequence asociada usando pg_get_serial_sequence
    try:
        cur.execute("SELECT pg_get_serial_sequence(%s, %s);", (table, pk))
        seq = cur.fetchone()[0]
        print('associated sequence:', seq)
        if seq:
            cur.execute(f"SELECT last_value, is_called FROM {seq};")
            srow = cur.fetchone()
            print('sequence state:', srow)
    except Exception as e:
        print('sequence check failed:', e)

conn.close()
print('\nDone.')
