# application.py

import uvicorn
from fastapi import FastAPI
from celery.result import AsyncResult
from pydantic import HttpUrl

# 수정된 스키마를 임포트합니다.
from schemas import AvatarCreateRequest, AvatarTryOnRequest, TaskResponse
from tasks import celery_app

app = FastAPI(
    title="FitDiT API Server (Publisher)",
    description="사용자 요청을 받아 Celery 워커에게 작업을 위임하고, 완료 시 콜백을 보냅니다.",
    version="3.0.0"
)

def convert_http_url_to_string(data: dict) -> dict:
    """Pydantic 모델의 HttpUrl 필드를 문자열로 변환합니다."""
    for key, value in data.items():
        if isinstance(value, HttpUrl):
            data[key] = str(value)
    return data

@app.post("/generate", response_model=TaskResponse, status_code=202, summary="마스크/포즈 생성 작업 요청 (콜백 방식)")
async def request_generate(request: AvatarCreateRequest):
    """
    마스크/포즈 생성 작업을 Celery 큐에 넣고, 즉시 Celery의 작업 ID를 반환합니다.
    작업 완료 시 Spring 서버의 callbackUrl로 결과가 전송됩니다.
    """
    print(f"API: /generate 요청 수신. Spring Task ID: {request.taskId}")
    # Pydantic 모델을 dict로 변환하고 HttpUrl을 문자열로 변환
    task_args = convert_http_url_to_string(request.dict())
    task = celery_app.send_task("process_generate_request", args=[task_args])
    return {"task_id": task.id, "status": "작업이 대기열에 추가되었습니다."}


@app.post("/tryon", response_model=TaskResponse, status_code=202, summary="Try-On 이미지 생성 작업 요청 (콜백 방식)")
async def request_tryon(request: AvatarTryOnRequest):
    """
    Try-On 이미지 생성 작업을 Celery 큐에 넣고, 즉시 Celery의 작업 ID를 반환합니다.
    작업 완료 시 Spring 서버의 callbackUrl로 결과가 전송됩니다.
    """
    print(f"API: /tryon 요청 수신. Spring Task ID: {request.taskId}")
    # Pydantic 모델을 dict로 변환하고 HttpUrl을 문자열로 변환
    task_args = convert_http_url_to_string(request.dict())
    task = celery_app.send_task("process_tryon_request", args=[task_args])
    return {"task_id": task.id, "status": "작업이 대기열에 추가되었습니다."}


# 이 엔드포인트는 디버깅 및 상태 확인 용도로 유지할 수 있습니다.
@app.get("/result/{celery_task_id}", summary="작업 결과 확인 (디버깅용)")
async def get_task_result(celery_task_id: str):
    """Celery의 작업 ID를 사용하여 작업의 상태와 최종 결과를 확인합니다."""
    task = AsyncResult(celery_task_id, app=celery_app)

    if task.failed():
        return {"status": "FAILURE", "result": str(task.result)}

    if not task.ready():
        return {"status": "PENDING"}
    
    return {"status": "SUCCESS", "result": task.result}

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
import logging

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"❌ Validation error at {request.url}: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )


# 로컬 테스트를 위한 실행 구문
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)