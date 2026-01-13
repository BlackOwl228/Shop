from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from core.utils import templates
from core import get_db
from core.security import get_current_user_cookie
from models import User

router = APIRouter(tags=["FOR WEBSITE"])

@router.get("/front/profile")
def profile(request: Request,
            user: User = Depends(get_current_user_cookie),
            db: Session = Depends(get_db)):
    found_user = db.query(User).get(user.id)
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": found_user,
        }
    )