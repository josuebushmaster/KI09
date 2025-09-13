"""Comprueba min/max/count, gaps y secuencia asociada para dimensiones OLAP.
Uso: & .venv\Scripts\python.exe scripts/check_sequences_and_gaps.py
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
    min_id, max_id, cnt = row
    print(f"min={min_id} max={max_id} count={cnt}")
    if min_id is None:
        print('Table empty')
    else:
        # gaps
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
    # attempt to get sequence via pg_get_serial_sequence
    try:
        cur.execute("SELECT pg_get_serial_sequence(%s, %s);", (table, pk))
        seq = cur.fetchone()[0]
    except Exception:
        seq = None
    if seq:
        print('associated sequence (pg_get_serial_sequence):', seq)
        try:
            cur.execute(f"SELECT last_value, is_called FROM {seq};")
            srow = cur.fetchone()
            print('sequence state:', srow)
        except Exception as e:
            print('failed to read sequence state:', e)
    else:
        # fallback: search sequences that depend on the table
        print('pg_get_serial_sequence returned NULL; searching pg_depend for sequences...')
        cur.execute("""
            SELECT n.nspname as schema, s.relname as seqname
            FROM pg_class s
            JOIN pg_namespace n ON s.relnamespace = n.oid
            JOIN pg_depend d ON d.objid = s.oid
            JOIN pg_class t ON d.refobjid = t.oid
            WHERE s.relkind = 'S' AND t.relname = %s;
        """, (table,))
        rows = cur.fetchall()
        if not rows:
            print('No dependent sequences found.')
        else:
            for schema, seqname in rows:
                full = f"{schema}.{seqname}"
                print('found sequence:', full)
                try:
                    cur.execute(f"SELECT last_value, is_called FROM {full};")
                    print('sequence state:', cur.fetchone())
                except Exception as e:
                    print('failed to read', full, e)

conn.close()
print('\nDone.')
