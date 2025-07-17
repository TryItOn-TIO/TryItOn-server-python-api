from celery import Celery
from config import settings

# Celery 애플리케이션 생성
# 이 앱을 통해 API 서버는 작업 요청을 Redis로 보낼 수 있습니다.
celery_app = Celery(
    "worker_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# 실제 작업 내용은 워커 서버에만 구현되므로 여기서는 비워둡니다.
# API 서버는 이 객체를 통해 작업 이름과 인자를 알고, .delay()를 호출하는 역할만 합니다.