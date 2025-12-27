import textwrap
from fastapi import FastAPI, Query, Path, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import database
import logging

import os
from time import time
import mysql.connector


class Message(BaseModel):
    status: int = Field(..., example=503, description="Response Status Code")
    message: str = Field(..., example="Service Unavailable", description="Response Status Message")


class OptionalPingMessage(Message):
    status: int = Field(..., example=500, description="Response Status Code")
    message: str = Field(..., example="Internal Server Error", description="Response Status Message")
    ping: float = Field(None, example=0.47, description="Response Query Time (if available)")


class PingMessage(Message):
    status: int = Field(..., example=200, description="Response Status Code")
    message: str = Field(..., example="OK", description="Response Status Message")
    ping: float = Field(..., example=0.47, description="Response Query Time")


logger = logging.getLogger('app')
app = FastAPI(
        docs_url=None,
        redoc_url="/docs",
    )
default_responses = {
        503: { 'model': Message, 'description': "Backend is unreachable." },
    }


def fetch_connection():
    with database.connection() as connection:
        with connection.cursor(dictionary=True) as cursor:
            try:
                yield cursor
                connection.commit()
            except Exception:
                connection.rollback()
                raise


@app.exception_handler(mysql.connector.errors.InterfaceError)
def handle_database_exception(request: Request, e: mysql.connector.errors.InterfaceError):
    return JSONResponse(
            status_code = 503,
            content = {
                'status': 503,
                'message': 'Service Unavailable: Backend Unreachable',
            },
        )


@app.get(
        "/health",
        response_model = PingMessage,
        response_description = "Health check was successful.",
        responses = {
            500: { 'model': OptionalPingMessage, 'description': "- The backend service failed its healthcheck.\n- The healthcheck query failed." },
            **default_responses,
        },
    )
def check_health(db=Depends(fetch_connection)):
    try:
        tic = time()
        db.execute("WITH t_health (base) AS (SELECT DATABASE() = 'hbz-registrations') SELECT IF(base, 200, 500) AS status, IF(base, 'OK', 'Internal Server Error: Bad Database') AS message FROM t_health")
        toc = time()
        result = db.fetchone()
        result['ping'] = 1000 * (toc - tic)
        return JSONResponse(
                status_code = result['status'],
                content = result,
            )
    except Exception:
        return JSONResponse(
                status_code = 500,
                content = {
                    'status': 500,
                    'message': 'Internal Server Error: Unknown Error',
                },
            )
