from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models, token
from ..hashing import Hash
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login')
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credenciais inválidas"
        )
    try:
        if Hash.verify(user.password, request.password):
            pass
            
    except VerifyMismatchError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Senha inválida"
        )
    except (InvalidHash, VerificationError) as e:
        print("Erro de verificação de senha:", e)
        return False
    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token":access_token, "token_type":"bearer"}