from typing import List

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from fastapi_pagination import LimitOffsetPage, Page, add_pagination, paginate
from sqlalchemy.orm import Session

from ... import errors
from .. import dependencies, models, oauth2, schemas, token
from ..jwt_bearer import JWTBearer
from ..repository import list_todo

router = APIRouter(prefix="/lists", tags=["Lists"])

get_db = dependencies.get_db


@router.post("/", dependencies=[Depends(JWTBearer(Request))], response_model=schemas.CreateListResponse)
def create_new_list(request: Request, payload: schemas.CreateListBody, db: Session = Depends(get_db)):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        user_id = auth_info["user_id"]
        name = payload.name
        description = payload.description
        post_list = list_todo.create(name, description, user_id, db)
        return post_list
    except errors.Used:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error": "Information has been used!"})
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Not found user!"})


@router.get("/{id}", dependencies=[Depends(JWTBearer(Request))], response_model=schemas.GetListByIdResponse)
def get_list_by_id(id: int, request: Request, db: Session = Depends(get_db)):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        user_id = auth_info["user_id"]
        get_list = list_todo.get_list_id(user_id, id, db)
        return get_list
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "List Not Found!"})


@router.get("/", dependencies=[Depends(JWTBearer(Request))], response_model=Page[schemas.GetListByIdResponse])
def get_list(request: Request, db: Session = Depends(get_db)):
    key = (request.headers.get("authorization")).split(" ")[-1]
    auth_info = token.verify_token(key)
    user_id = auth_info["user_id"]
    get_list = list_todo.get_list(user_id, db)
    return get_list


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer(Request))])
def delete_list(id: int, request: Request, db: Session = Depends(get_db)):
    try:
        key = (request.headers.get("authorization")).split(" ")[-1]
        auth_info = token.verify_token(key)
        user_id = auth_info["user_id"]
        delete_list = list_todo.delete(user_id, id, db)
        return delete_list
    except errors.NotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "List Not Found!"})
