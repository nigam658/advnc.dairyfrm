from fastapi import APIRouter, HTTPException, BackgroundTasks
from passlib.context import CryptContext

from app.databases.mysqldb import SessionLocal
from app.schemas.user_schema import user_pass,LoginUser
from app.models.user_model import SignpUser
from app.service.auth_service import create_user, create_token_fnc
from app.service.jwt_handler import verify_refresh_token, create_access_token
from app.email.send_email import send_welcome_email

router = APIRouter()

@router.post("/signup")
def signup(user : user_pass,Background_tasks : BackgroundTasks):

    db = SessionLocal()

    # First try username or email exist or not 
    try :
        created_user = create_user(db,user)

        Background_tasks.add_task(send_welcome_email,created_user.email, created_user.username)

        return {
            "message" : "signup successfully done"
        }
    except HTTPException:
        raise

    # if try fail, error print  
    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        db.close()


#login router 
@router.post("/login")
def login(login_data: LoginUser):

    db = SessionLocal()

    try:
        tokens = create_token_fnc(db, login_data)

    finally:
        db.close()

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer"
    }

@router.post("/refresh-token")
def refresh_token(refresh_token: str):

    db = SessionLocal()

    try:

        payload = verify_refresh_token(refresh_token)

        if not payload:
            raise HTTPException(
                status_code=401,
                detail="invalid refresh token"
            )

        username = payload.get("sub")

        user = db.query(SignpUser).filter(
            SignpUser.username == username
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="user not found"
            )

        new_access_token = create_access_token({
            "sub": user.username,
            "role": user.role
        })

        return {
            "access_token": new_access_token
        }

    finally:
        db.close()