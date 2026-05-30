from fastapi import HTTPException
from passlib.context import CryptContext
from app.models.user_model import SignpUser
from app.schemas.user_schema import user_pass
from sqlalchemy import or_
from app.service.jwt_handler import create_access_token, create_refresh_token

 
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#create user for signup
def create_user(db ,user):
    existing_user = db.query(SignpUser).filter(
                or_(
                    SignpUser.email == user.email,
                    SignpUser.username  == user.username
                )
            ).first()

    if existing_user :
        raise HTTPException(
            status_code=400,
            detail="user already exist, try new username"
        )
    
    hassed_password = pwd_context.hash(user.password)

    new_user = SignpUser(
            email=user.email,
            username=user.username,
            password=hassed_password,
            role="customer"
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
                
def create_token_fnc(db, login_data):

    user_exist = db.query(SignpUser).filter(
        or_(
            SignpUser.username == login_data.username,
            SignpUser.email == login_data.username
        )
    ).first()

    if not user_exist:
        raise HTTPException(
            status_code=404,
            detail="user not found!"
        )

    is_password_correct = pwd_context.verify(
        login_data.password,
        user_exist.password
    )

    if not is_password_correct:
        raise HTTPException(
            status_code=401,
            detail="invalid password"
        )

    access_token = create_access_token({
        "sub": user_exist.username,
        "role": user_exist.role
    })

    refresh_token = create_refresh_token({
        "sub": user_exist.username
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


         
