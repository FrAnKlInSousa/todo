from todo.schemas import NivelAtividadeFisica
from todo.utils.decimal import arredonda_casas_decimais


def calcula_taxa_metabolica_basal(
    peso: float,
    altura: int,
    idade: int,
    sexo: float,
    nivel_atividade_fisica: NivelAtividadeFisica,
):
    tmb = taxa_metabolica(peso, altura, idade, sexo)
    tmb_final = aplica_fator_atividade_fisica(tmb, nivel_atividade_fisica)
    return tmb_final


def taxa_metabolica(
    peso: float, altura: int, idade: int, sexo: float
) -> float:
    taxa_peso = 10
    taxa_altura = 6.25
    taxa_idade = 5

    taxa_basal = (
        (taxa_peso * peso)
        + (taxa_altura * altura)
        - (taxa_idade * idade)
        + sexo
    )

    return arredonda_casas_decimais(taxa_basal)


def aplica_fator_atividade_fisica(
    taxa_metabolica_basal: float, nivel_atividade_fisica: NivelAtividadeFisica
) -> float:
    taxa_basal_com_fator_atividade = (
        taxa_metabolica_basal * nivel_atividade_fisica.fator
    )

    return arredonda_casas_decimais(taxa_basal_com_fator_atividade)
