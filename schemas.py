# schemas.py (수정 완료)

from pydantic import BaseModel, HttpUrl

class AvatarCreateRequest(BaseModel):
    tryOnImgUrl: HttpUrl
    userId: int
    taskId: str
    callbackUrl: HttpUrl

class AvatarTryOnRequest(BaseModel):
    baseImgUrl: HttpUrl
    garmentImgUrl: HttpUrl
    maskImgUrl: HttpUrl
    poseImgUrl: HttpUrl
    userId: int
    # [수정] 아래 두 필드 추가
    productId: int
    garmentType: str
    taskId: str
    callbackUrl: HttpUrl

class TaskResponse(BaseModel):
    task_id: str
    status: str