Feature: Autenticação de Usuário
    Como um usuário da API
    Quero gerar um token de acesso usando meu CPF
    Para que eu possa acessar recursos protegidos

    Scenario: Gerar token com CPF válido
        Given que possuo um CPF válido "21829365053"
        When eu solicito a criação de um token para este CPF
        Then o sistema deve retornar o código de status 200
        And a resposta deve conter um token de acesso