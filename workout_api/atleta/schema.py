from typing import Annotated, Optional
from pydantic import Field, PositiveFloat

from workout_api.categorias.schema import CategoriaIn
from workout_api.centro_treinamento.schema import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', examples=["Kaka"], max_length=50)]    
    cpf: Annotated[str, Field(description='CPF do Atleta', examples=["12345678901"], max_length=11)]    
    idade: Annotated[int, Field(description='Idade do Atleta', examples=[21])]
    peso: Annotated[PositiveFloat, Field(description="Peso do Atleta", example=56.5)]   
    altura: Annotated[PositiveFloat, Field(description="Altura do Atleta", example=1.81)] 
    sexo: Annotated[str, Field(description='Sexo do Atleta', examples=["F"], max_length=1)]    
    categoria : Annotated[CategoriaIn, Field(description="Categoria do Atleta")]
    centro_treinamento : Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]
    
class AtletaIn(Atleta):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None,description='Nome do Atleta', examples=["Kaka"], max_length=50)]    
    idade: Annotated[Optional[int], Field(None,description='Idade do Atleta', examples=[21])]
  
    
class AtletaOut(AtletaIn, OutMixin):
    pass
