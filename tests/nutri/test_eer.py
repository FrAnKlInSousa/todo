import pytest

from todo.schemas import NivelAtividadeFisica, Sexo
from todo.services.taxa_metabolica import (
    aplica_fator_atividade_fisica,
    taxa_metabolica,
)


@pytest.mark.parametrize(
    ('peso', 'altura', 'idade', 'sexo', 'esperado'),
    [
        (60, 150, 20, Sexo.HOMEM, 1442.5),
        (70, 160, 32, Sexo.HOMEM, 1545),
        (60, 150, 20, Sexo.MULHER, 1276.5),
        (70, 160, 32, Sexo.MULHER, 1379),
        (35, 150, 12, Sexo.HOMEM, 1232.5),
        (50, 168, 20, Sexo.HOMEM, 1455),
        (55, 175, 24, Sexo.HOMEM, 1528.75),
        (60, 180, 56, Sexo.HOMEM, 1450),
        (87, 185, 31, Sexo.HOMEM, 1876.25),
        (91, 165, 35, Sexo.HOMEM, 1771.25),
        (89, 159, 42, Sexo.HOMEM, 1678.75),
        (84, 179, 19, Sexo.HOMEM, 1868.75),
        (65, 154, 27, Sexo.HOMEM, 1482.5),
        (123, 196, 44, Sexo.HOMEM, 2240),
        (68, 156, 12, Sexo.MULHER, 1434),
        (55, 160, 20, Sexo.MULHER, 1289),
        (62, 172, 24, Sexo.MULHER, 1414),
        (58, 148, 56, Sexo.MULHER, 1064),
        (71, 152, 31, Sexo.MULHER, 1344),
        (66, 160, 35, Sexo.MULHER, 1324),
        (54, 161, 42, Sexo.MULHER, 1175.25),
        (63, 180, 19, Sexo.MULHER, 1499),
        (49, 145, 27, Sexo.MULHER, 1100.25),
        (122, 177, 44, Sexo.MULHER, 1945.25),
    ],
)
def test_taxa_metabolica_basal(
    peso: float, altura: int, idade: int, sexo: Sexo, esperado: float
):
    resultado = taxa_metabolica(peso, altura, idade, sexo.sexo)
    assert resultado == esperado


@pytest.mark.parametrize(
    ('taxa_metabolica_basal', 'nivel_atividade_fisica', 'esperado'),
    [
        (1442.5, NivelAtividadeFisica.MODERADO, 2163.75),
        (1545, NivelAtividadeFisica.LEVE, 2124.38),
        (1232.50, NivelAtividadeFisica.SEDENTARIO, 1479),
        (1455, NivelAtividadeFisica.ATLETA, 2764.50),
        (1528.75, NivelAtividadeFisica.SEDENTARIO, 1834.50),
        (1450, NivelAtividadeFisica.MODERADO, 2175),
        (1876.25, NivelAtividadeFisica.LEVE, 2579.84),
        (1771.25, NivelAtividadeFisica.SEDENTARIO, 2125.5),
        (1678.75, NivelAtividadeFisica.LEVE, 2308.28),
        (1868.75, NivelAtividadeFisica.INTENSO, 3223.59),
        (1482.5, NivelAtividadeFisica.ATLETA, 2816.75),
        (2240, NivelAtividadeFisica.INTENSO, 3864),
        (1434, NivelAtividadeFisica.LEVE, 1971.75),
        (1289, NivelAtividadeFisica.SEDENTARIO, 1546.8),
        (1414, NivelAtividadeFisica.LEVE, 1944.25),
        (1064, NivelAtividadeFisica.MODERADO, 1596),
        (1344, NivelAtividadeFisica.LEVE, 1848),
        (1324, NivelAtividadeFisica.ATLETA, 2515.6),
        (1175.25, NivelAtividadeFisica.LEVE, 1615.97),
        (1499, NivelAtividadeFisica.INTENSO, 2585.78),
        (1100.25, NivelAtividadeFisica.ATLETA, 2090.48),
        (1945.25, NivelAtividadeFisica.MODERADO, 2917.88),
    ],
)
def test_taxa_metabolica_final(
    taxa_metabolica_basal, nivel_atividade_fisica, esperado
):
    resultado = aplica_fator_atividade_fisica(
        taxa_metabolica_basal, nivel_atividade_fisica
    )
    assert resultado == esperado
