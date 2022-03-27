import sys
import psycopg2
from init import config
from src import lost_update, phantom_read, nonrepeatable_read, Read_Skew, Write_Skew
import random

TransactionClassMap = {
    'LU': [lost_update.transaction1, lost_update.transaction2],
    'PR': [phantom_read.transaction1, phantom_read.transaction2],
    'NR': [nonrepeatable_read.transaction1, nonrepeatable_read.transaction2],
    'RS': [Read_Skew.transaction1, Read_Skew.transaction2],
    'WS': [Write_Skew.transaction1, Write_Skew.transaction2],
}

isolationMap = {
    'RC': 'READ COMMITTED',
    'RR': 'REPEATABLE READ',
    'S': 'Serializable'
}

"""
@:param1: Anomaly Type
    Lost-Update
    Non-Repeatable-Read
    Phantom-Read
    Read-Skew
    Write-Skew
@:param2: Isolation Level
    RC: read committed
    RR: repeatable read
    S:  serializable
"""
if __name__ == '__main__':

    TYPE = sys.argv[1]          # anomaly type
    IL = sys.argv[2]            # isolation level

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)

        isolationLevel = isolationMap[IL]

        conn.set_session(isolation_level=isolationLevel, autocommit=True)
        with conn.cursor() as cur:
            cur.execute(open("sql/schema.sql", "r").read())

        TransactionClasses = TransactionClassMap[TYPE]

        index = random.randint(0, len(TransactionClasses) - 1)
        print(index)
        TransactionClass = TransactionClasses[index]

        conn.set_session(isolation_level=isolationLevel, autocommit=False)

        transaction = TransactionClass(conn)
        result = transaction.exec()
        print(result)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



