
# Flask-auth

Este projeto refere-se a criação de uma API para lidar com autenticação de usuários em alguma plataforma. Com essa API, um cliente pode gerenciar usuários a partir de um atributo que define o nível de acesso de um perfil. Esse projeto faz parte de um módulo do curso de Backend com Python da [Rocketseat](https://www.rocketseat.com.br/). Essas são as funcionalidades da API:

- CRUD de usuários
- Realizar login e logout de usuários
- Lidar com acesso de rotas com base no estado do usuário

## Tecnologias usadas

- **Linguagem:** Python
- **Framework:** Flask
- **Banco de dados:** MySQL
- **ORM:** SQLAlchemy
- **Testes:** Pytest
- **Utils**: Requests, BCrypt, Shortuuid

## Referência da API

### Criar usuário

```
  POST /user
```

Corpo da requisição
```json
{
    "username": "<string>",
    "password": "<string>"
}

```

Respostas
| Código    |  Descrição                       |
| :-------- |:-------------------------------- |
| 200    | Usuário criado com sucesso |
| 400    | Dados enviados incorretamente|

### Realizar Login

```
  POST /login   
```

Corpo da requisição
```json
{
    "username": "<string>",
    "password": "<string>"
}

```

Respostas
| Código    |  Descrição                       |
| :-------- |:-------------------------------- |
| 200    | Login realizado com sucesso |
| 400    | Credenciais inválidas|

### Realizar Logout

```
  GET /logout   
```

**O usuário precisa estar logado para realizar essa ação**


Respostas
| Código    |  Descrição                       |
| :-------- |:-------------------------------- |
| 200    | Logout realizado com sucesso |


### Obter usuário
**O usuário precisa estar logado para realizar essa ação**

```
  GET /user/<id>   
```

| Parâmetro | Tipo     | Descrição                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `Inteiro` | **Obrigatório**. ID do usuário a ser obtido|

Respostas
| Código    |  Descrição                       | Retorno
| :-------- |:-------------------------------- |:---------|
| 200    | Usuário encontrado com sucesso|{"username": "<string>"}
| 404    | Usuário não encontrado| {"message": "<string>"}

### Atualizar usuário
**O usuário precisa estar logado para realizar essa ação. Além disso, um usuário comum só pode atualizar a sua própria senha e um perfil administrador pode atualizar a senha de qualquer usuário.**

```
  PUT /user/<id>   
```

| Parâmetro | Tipo     | Descrição                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `Inteiro` | **Obrigatório**. ID do usuário a ser atualizado|

Corpo da requisição
```json
{
    "password": "<string>"
}

```

Respostas
| Código    |  Descrição                       | Retorno
| :-------- |:-------------------------------- |:---------|
| 200    | Usuário atualizado com sucesso|{"user_id": int, "message": "<string>"}
| 403    | Usuário normal tentou atualizar outro usuário| {"message": "<string>"}
| 404    | Usuário não encontrado| {"message": "<string>"}

### Remover usuário
**O usuário precisa estar logado para realizar essa ação. Além disso, somente perfis administradores podem remover um usuário, mas não podem remover eles mesmos.**

```
  DELETE /user/<id>   
```

| Parâmetro | Tipo     | Descrição                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `Inteiro` | **Obrigatório**. ID do usuário a ser removido|

Respostas
| Código    |  Descrição                       | Retorno
| :-------- |:-------------------------------- |:---------|
| 200    | Usuário deletado com sucesso|{"message": "<string>"}
| 403    | Usuário não seguiu os requisitos supracitados| {"message": "<string>"}
| 404    | Usuário não encontrado| {"message": "<string>"}
