from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import database

from time import time

app = FastAPI()


def fetch_connection():
    with database.connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                yield cursor
                connection.commit()
            except Exception:
                connection.rollback()
                raise


@app.get("/health")
def check_health(db=Depends(fetch_connection)):
    try:
        tic = time()
        db.execute("WITH t_health (base) AS (SELECT DATABASE() = 'hbz-registrations') SELECT IF(base, 'ok', 'warn') AS status, IF(base, '', 'wrong database selected') AS message FROM t_health")
        toc = time()
        result = db.fetchone()
        result['ping'] = 1000 * (toc - tic)
        return result
    except Exception:
        return { status: 'fatal', message: 'backend service unreachable' }
