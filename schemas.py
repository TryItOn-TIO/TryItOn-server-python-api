from pydantic import BaseModel, HttpUrl
from typing import Optional # Optional 임포트

class AvatarCreateRequest(BaseModel):
    userId: str
    tryOnImgUrl: HttpUrl
    # [수정] 아래 두 필드를 선택적으로 변경
    taskId: Optional[str] = None
    callbackUrl: Optional[HttpUrl] = None

class AvatarTryOnRequest(BaseModel):
    baseImgUrl: HttpUrl
    garmentImgUrl: HttpUrl
    maskImgUrl: HttpUrl
    poseImgUrl: HttpUrl
    userId: int
    productId: int
    garmentType: str
    cacheKey: str
    # [수정] 아래 두 필드를 선택적으로 변경
    taskId: Optional[str] = None
    callbackUrl: Optional[HttpUrl] = None

# TaskResponse 스키마는 그대로 유지
class TaskResponse(BaseModel):
    task_id: str
    status: str