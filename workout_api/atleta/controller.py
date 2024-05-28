from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy import DateTime, select
from datetime import datetime, timezone

from workout_api.atleta.model import AtletaModel
from workout_api.atleta.schema import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.model import CategoriaModel
from workout_api.centro_treinamento.model import CentroTreinamentoModel
from workout_api.contrib.depedencies import DataBaseDependency

router = APIRouter()


@router.post(
    path="/",
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DataBaseDependency, atleta_in: AtletaIn = Body(...)
) -> AtletaOut:

    # Verificar existencia de categoria e centro de treinamento

    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    #Verificando categoria 
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {categoria_nome} não foi encontrada",
        )
        
    #Verificando centro de treinamento    
    centro_treinamento = (
            (
                await db_session.execute(
                    select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
                )
            )
            .scalars()
            .first()
        )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro_treinamento {centro_treinamento_nome} não foi encontrado",
        )
        
    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump()
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )
        
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamenento_id = centro_treinamento.pk_id
        
    
        db_session.add(atleta_model)

        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Atleta com esse CPF já criado!'
        )

    return atleta_out

@router.get(
    '/',
    summary="Consultar todos os atletas",
    status_code= status.HTTP_201_CREATED,
    response_model= list[AtletaOut],
)
async def query(db_session:DataBaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (
        await db_session.execute(   select(AtletaModel))
        ).scalars().all()
 
        
    
    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@router.patch(
        '/{id}',
    summary="Alterar um atleta por ID", 
    status_code= status.HTTP_201_CREATED,
    response_model= AtletaOut,
)

async def patch(id:UUID4, db_session: DataBaseDependency, atleta_update:AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta com id {id} não encontrado'
        )  
    atleta_aux= atleta_update.model_dump(exclude_unset=True)
    
    for key, value in atleta_aux.items():
        setattr(atleta,key,value)
        
    await db_session.commit()
    await db_session.refresh(atleta)
    
    return atleta

@router.delete(
    '/{id}',
    summary= "Deletando um atleta por ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def get(id:UUID4, db_session:DataBaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
        
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta com id {id} não encontrado'
        )  
    await db_session.delete(atleta)
    await db_session.commit()
