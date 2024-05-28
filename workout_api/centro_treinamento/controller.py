from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import select

from workout_api.centro_treinamento.model import CentroTreinamentoModel
from workout_api.centro_treinamento.schema import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.depedencies import DataBaseDependency

router = APIRouter()


@router.post(
    path = "/",
    summary="Criar novo centro de treinamento",
    status_code = status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut
             )
async def post(
    db_session: DataBaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamentoModel = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    
    db_session.add(centro_treinamentoModel)

    await db_session.commit()
    
    return centro_treinamento_out

@router.get(
    path = "/",
    summary="Consultar todos os centros de treinamento",
    status_code = status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut]
             )
async def query( db_session: DataBaseDependency ) -> list[CentroTreinamentoOut]:
    centros: list[CentroTreinamentoOut] = (await(db_session.execute(select(CentroTreinamentoModel)))).scalars().all()
    
    return centros

@router.get(
    path = "/{id}",
    summary="Consultar um centro de treinamento por ID",
    status_code = status.HTTP_200_OK,
    response_model=CentroTreinamentoOut
             )
async def query( db_session: DataBaseDependency, id : UUID4) -> CentroTreinamentoOut:
    
    centro:CentroTreinamentoOut = (await(db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)))).scalars().first()
    
    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Centro de treinamento não encontrado com o id {id}")
    
    return centro
