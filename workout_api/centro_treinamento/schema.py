from typing import Annotated

from pydantic import UUID4, Field

from workout_api.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
    nome: Annotated[str,Field(description='Nome do Centro', examples=["SmartFit"], max_length=50)]  
    endereco: Annotated[str,Field(description='Endereco do Centro', examples=["Rua A Bairro B"], max_length=50)]  
    propietario: Annotated[str,Field(description='Nome do Centro', examples=["Carlos"], max_length=25)]    
    
class CentroTreinamentoIn(CentroTreinamento):
    pass

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str,Field(description='Nome do Centro', examples=["SmartFit"], max_length=50)]  
    
class CentroTreinamentoOut(CentroTreinamento):
    id : Annotated[UUID4,Field(description="Identificador de Centro de Treinamento")]