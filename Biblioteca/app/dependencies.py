from typing import Annotated
from fastapi import Header, HTTPException

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token!='upiix-token-secreto':
        raise HTTPException(status_code=400, detail="Token invalido")
    
async def get_query_token(token:str): 
    if token!="burrito":
        raise HTTPException(status_code=400, detail="Token inválido")