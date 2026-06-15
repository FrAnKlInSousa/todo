- # Observações
- Uma forma de subir o servidor na rede local, é passando o host 0.0.0.0:
  - ex.: 
  ```shell
      poetry run fastapi dev todo/app.py --host 0.0.0.0
  ```
- Para revisar e entender melhor a Session e a Engine, assitir a aula 04 a partir de 31:19
  - Caso queira ver de forma rápida o arquivo local de banco de dados, dá pra usar o pipx pra executar o harlequin:
  ```shell
      pipx run harlequin database.db
  ```
- `secrets` é uma biblioteca nativa do python que pode ser usada para gerar senhas.
  ```shell
      import secrets
      secrets.token_hex(32)
  ```
- Ao usar o sqlite, quando precisar deixar ele assíncrono, basta alterar o valor dela no .env:
  - `DATABASE_URL='sqlite:///database.db'` para:
  - `DATABASE_URL='sqlite+aiosqlite:///database.db'`
- O pytest tem um comando para listar todos os testes do projeto:
```shell
    task test --collect-only
```

# Tasks:
  - ver lives:
    - #151 -> #154 [Playlist de corrotinas](https://www.youtube.com/watch?v=ZjwZ9nfhsk4&list=PLOQgLBuj2-3J4IRxalwXhRMU6UPoaigf9)
    - #168: [Pytest Fixtures](https://www.youtube.com/watch?v=sidi9Z_IkLU)
    - #189: [Documentado projetos com MkDocs](https://www.youtube.com/watch?v=GW6nAJ1NHUQ)
    - #207: [Variáveis de ambiente, dotenv, constantes e configurações](https://www.youtube.com/watch?v=DiiKff1z2Yw)
    - #211: [Migrações, bancos de dados evolutivos (Alembic e SQLAlchemy) ](https://www.youtube.com/watch?v=yQtqkq9UkDA)
    - #224: [Rich: fazendo prints incríveis](https://www.youtube.com/watch?v=gadMAObZ_1Y)
    - #234: [Requests assíncronos com HTTPX](https://www.youtube.com/watch?v=V4hSLZRCGoE)
    - #242: [Trio: Concorrência estruturada](https://www.youtube.com/watch?v=pejxUqrT7yo)
    - #258: [SQLAlchemy: conceitos básicos, uma introdução a versão 2](https://www.youtube.com/watch?v=t4C1c62Z4Ag)
    - #281: [Randomização de dados em testes unitários com Faker e Factory-boy](https://www.youtube.com/watch?v=q_P-2h5L1cE)
    - #305: [Boas práticas para clientes HTTP](https://www.youtube.com/watch?v=U_qmGH34sgc)

# Livros
- [Cosmic Python](http://www.cosmicpython.com/book/preface.html)
- [Python Fluente 2e](https://github.com/pythonfluente/pythonfluente2e/releases/tag/trilogia-2026-03-23)