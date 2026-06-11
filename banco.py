from neo4j import GraphDatabase

URI = "neo4j+s://d8ee697f.databases.neo4j.io"
AUTH = ("d8ee697f", "yAD_gDVo7Qq0MTKXiwYKkOjPOzUHBodaxpsH7tWah8Y")

driver = GraphDatabase.driver(URI, auth=AUTH)

driver.verify_connectivity()
print("Conectado ao Neo4j com sucesso!")


def create_usuario():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")

    print("\n=== ENDEREÇO ===")
    rua = input("Rua: ")
    num = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP: ")

    query = """
    MERGE (u:Usuario {cpf: $cpf})
    SET
        u.nome = $nome,
        u.sobrenome = $sobrenome,
        u.rua = $rua,
        u.num = $num,
        u.bairro = $bairro,
        u.cidade = $cidade,
        u.estado = $estado,
        u.cep = $cep
    """

    with driver.session() as session:
        session.run(
            query,
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            rua=rua,
            num=num,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep
        )

    print("Usuário cadastrado com sucesso!")


def create_vendedor():
    nome = input("Nome: ")
    sobrenome = input("Sobrenome: ")
    cpf = input("CPF: ")

    print("\n=== ENDEREÇO ===")
    rua = input("Rua: ")
    num = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado: ")
    cep = input("CEP: ")

    query = """
    MERGE (v:Vendedor {cpf: $cpf})
    SET
        v.nome = $nome,
        v.sobrenome = $sobrenome,
        v.rua = $rua,
        v.num = $num,
        v.bairro = $bairro,
        v.cidade = $cidade,
        v.estado = $estado,
        v.cep = $cep
    """

    with driver.session() as session:
        session.run(
            query,
            nome=nome,
            sobrenome=sobrenome,
            cpf=cpf,
            rua=rua,
            num=num,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep
        )

    print("Vendedor cadastrado com sucesso!")


def create_produto():
    id_produto = int(input("ID do produto: "))
    nome = input("Nome do produto: ")
    descricao = input("Descrição: ")
    preco = float(input("Preço: "))
    cpf_vendedor = input("CPF do vendedor: ")

    with driver.session() as session:

        vendedor = session.run(
            """
            MATCH (v:Vendedor {cpf:$cpf})
            RETURN v
            """,
            cpf=cpf_vendedor
        ).single()

        if vendedor is None:
            print("Vendedor não encontrado!")
            return

        query = """
        MATCH (v:Vendedor {cpf:$cpf_vendedor})

        MERGE (p:Produto {id: $id_produto})

        SET
            p.nome = $nome,
            p.descricao = $descricao,
            p.preco = $preco

        MERGE (v)-[:VENDE]->(p)
        """

        session.run(
            query,
            id_produto=id_produto,
            nome=nome,
            descricao=descricao,
            preco=preco,
            cpf_vendedor=cpf_vendedor
        )

    print("Produto cadastrado com sucesso!")


def create_compra():
    cpf_usuario = input("CPF do usuário: ")
    id_produto = int(input("ID do produto: "))

    with driver.session() as session:

        usuario = session.run(
            """
            MATCH (u:Usuario {cpf:$cpf})
            RETURN u
            """,
            cpf=cpf_usuario
        ).single()

        if usuario is None:
            print("Usuário não encontrado!")
            return

        produto = session.run(
            """
            MATCH (p:Produto {id:$id})
            RETURN p
            """,
            id=id_produto
        ).single()

        if produto is None:
            print("Produto não encontrado!")
            return

        query = """
        MATCH (u:Usuario {cpf:$cpf_usuario})
        MATCH (p:Produto {id:$id_produto})

        CREATE (c:Compra {
            id: randomUUID(),
            data: date()
        })

        CREATE (u)-[:REALIZOU]->(c)
        CREATE (c)-[:CONTEM]->(p)
        """

        session.run(
            query,
            cpf_usuario=cpf_usuario,
            id_produto=id_produto
        )

    print("Compra cadastrada com sucesso!")

def read_usuarios():
    query = """
    MATCH (u:Usuario)
    RETURN u
    """

    with driver.session() as session:
        result = session.run(query)

        for record in result:
            u = record["u"]

            print(f"""
            Nome: {u['nome']} {u['sobrenome']}
            CPF: {u['cpf']}
            Cidade: {u['cidade']}
            Estado: {u['estado']}
            -------------------------
            """)

def read_vendedores():
    query = """
    MATCH (v:Vendedor)
    RETURN v
    """

    with driver.session() as session:
        result = session.run(query)

        for record in result:
            v = record["v"]

            print(f"""
            Nome: {v['nome']} {v['sobrenome']}
            CPF: {v['cpf']}
            Cidade: {v['cidade']}
            Estado: {v['estado']}
            -------------------------
            """)

def read_produtos():
    query = """
    MATCH (v:Vendedor)-[:VENDE]->(p:Produto)

    RETURN
        p.nome AS nome,
        p.id AS id,
        p.preco AS preco,
        p.descricao AS descricao,
        v.nome AS vendedor
    """

    with driver.session() as session:
        result = session.run(query)

        print("\n=== PRODUTOS ===")

        for record in result:
            print(f"""
            ID: {record['id']}
            Produto: {record['nome']}
            Descrição: {record['descricao']}
            Preço: R$ {record['preco']}
            Vendedor: {record['vendedor']}
            -------------------------
            """)

def read_compras():
    query = """
    MATCH (u:Usuario)-[:REALIZOU]->(c:Compra)
          -[:CONTEM]->(p:Produto)

    RETURN
        c.id AS compra,
        c.data AS data,
        u.nome AS usuario,
        p.nome AS produto
    """

    with driver.session() as session:
        result = session.run(query)

        print("\n=== COMPRAS ===")

        for record in result:
            print(f"""
        Compra: {record['compra']}
        Data: {record['data']}
        Usuário: {record['usuario']}
        Produto: {record['produto']}
        -------------------------
        """)

def menu():
    while True:
        print("1 - Cadastrar usuário")
        print("2 - Cadastrar vendedor")
        print("3 - Cadastrar produto")
        print("4 - Realizar compra")
        print("5 - Listar usuários")
        print("6 - Listar vendedores")
        print("7 - Listar produtos")
        print("8 - Listar compras")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            create_usuario()
        elif opcao == "2":
            create_vendedor()
        elif opcao == "3":
            create_produto()
        elif opcao == "4":
            create_compra()
        elif opcao == "5":
            read_usuarios()
        elif opcao == "6":
            read_vendedores()
        elif opcao == "7":
            read_produtos()
        elif opcao == "8":
            read_compras()
        elif opcao == "0":
            print("Tchau professor...")
            break
        else:
            print("Opção inválida!")
menu()

driver.close()