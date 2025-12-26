import textwrap
from fastapi import FastAPI, Query, Path, Depends, HTTPException
from pydantic import BaseModel, Field
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


class HealthCheckResponse(BaseModel):
    status: str = Field(..., example="ok", description=textwrap.dedent("""\
    The status of the backend service

    - `ok`: all systems nominal
    - `warn`: backend database sent a warning
    - `fatal`: backend service could not be reached"""))
    message: str = Field(..., example='', description="An additional message providing details on a potential error")
    ping: float = Field(None, example=0.47, description="The time used to query the backend database")


@app.get("/health", response_model=HealthCheckResponse)
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
