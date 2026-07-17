from fastapi import APIRouter

from todo.schemas import Nutri
from todo.services.taxa_metabolica import calcula_taxa_metabolica_basal

router = APIRouter(prefix='/nutri', tags=['Nutri'])


@router.post('/')
def eer(data: Nutri):
    """

    :param data:
    :return:
    """
    data_nutri = data.model_dump()
    tmb = calcula_taxa_metabolica_basal(**data_nutri)
    return {'resultado': tmb}


"""
{
  "peso": 60,
  "altura": 150,
  "idade": 20,
  "sexo": "homem",
  "nivel_atividade_fisica": "4 a 5"
}
"""
