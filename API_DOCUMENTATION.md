# 📚 Documentação da API Fortlar

## 🎯 **Visão Geral**

A API Fortlar é um sistema completo de gestão de empresas, produtos, pedidos e kits, desenvolvido com **FastAPI** e seguindo os princípios de **Clean Architecture**.

## 🚀 **Acesso à Documentação**

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **Base URL**: `http://localhost:8000/api`

## 📋 **Endpoints Disponíveis**

### 🔐 **Autenticação**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/login` | Login de usuário |
| `POST` | `/password` | Alterar senha |
| `POST` | `/token` | Validar token |

### 🏢 **Empresas**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/companies/` | Criar empresa |
| `GET` | `/companies/` | Listar empresas |
| `GET` | `/companies/{id}` | Buscar empresa por ID |
| `PUT` | `/companies/{id}` | Atualizar empresa |
| `DELETE` | `/companies/{id}` | Deletar empresa |

### 📦 **Produtos**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/produtos/` | Listar produtos |
| `GET` | `/produtos/categoria/{id}` | Produtos por categoria |
| `GET` | `/produtos/subcategoria/{id}` | Produtos por subcategoria |
| `GET` | `/produtos/search` | Buscar produtos |
| `GET` | `/produtos/price-range` | Produtos por faixa de preço |

### 📂 **Categorias**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/categorias/` | Listar categorias |
| `GET` | `/categorias/{id}` | Buscar categoria por ID |
| `GET` | `/categorias/{id}/produtos` | Produtos da categoria |
| `GET` | `/categorias/{id}/subcategorias` | Subcategorias da categoria |

### 🛒 **Pedidos**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/pedidos/` | Listar pedidos |
| `GET` | `/pedidos/{id}` | Buscar pedido por ID |
| `GET` | `/pedidos/cliente/{id}` | Pedidos do cliente |
| `GET` | `/pedidos/status/{status}` | Pedidos por status |
| `GET` | `/pedidos/recentes` | Pedidos recentes |

### 📦 **Kits**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/kits/` | Listar kits |
| `GET` | `/kits/{id}` | Buscar kit por ID |
| `GET` | `/kits/codigo/{codigo}` | Buscar kit por código |
| `GET` | `/kits/categoria/{categoria}` | Kits por categoria |
| `GET` | `/kits/search` | Buscar kits |

### 👥 **Contatos**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/contatos/` | Listar contatos |
| `GET` | `/contatos/{id}` | Buscar contato por ID |
| `GET` | `/contatos/empresa/{id}` | Contatos da empresa |
| `GET` | `/contatos/email/{email}` | Buscar por email |
| `GET` | `/contatos/empresa/{id}/principal` | Contato principal |

### 🏠 **Endereços**
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/enderecos/` | Listar endereços |
| `GET` | `/enderecos/{id}` | Buscar endereço por ID |
| `GET` | `/enderecos/empresa/{id}` | Endereços da empresa |
| `GET` | `/enderecos/empresa/{id}/principal` | Endereço principal |
| `GET` | `/enderecos/cep/{cep}` | Endereços por CEP |
| `GET` | `/enderecos/cidade/{cidade}` | Endereços por cidade |
| `GET` | `/enderecos/estado/{uf}` | Endereços por estado |

## 🔧 **Filtros e Parâmetros**

### **Parâmetros Comuns**
- `skip`: Número de registros para pular (paginação)
- `limit`: Número máximo de registros (padrão: 100)
- `active_only`: Filtrar apenas registros ativos

### **Filtros Específicos**

#### **Empresas**
- `vendedor_id`: Filtrar por vendedor
- `search_name`: Buscar por nome

#### **Produtos**
- `categoria_id`: Filtrar por categoria
- `subcategoria_id`: Filtrar por subcategoria
- `search_name`: Buscar por nome
- `min_price`: Preço mínimo
- `max_price`: Preço máximo

#### **Pedidos**
- `cliente_id`: Filtrar por cliente
- `status`: Filtrar por status
- `cupom_id`: Filtrar por cupom
- `start_date`: Data inicial
- `end_date`: Data final
- `min_value`: Valor mínimo
- `max_value`: Valor máximo

#### **Kits**
- `categoria`: Filtrar por categoria
- `search_name`: Buscar por nome
- `min_price`: Preço mínimo
- `max_price`: Preço máximo
- `with_products`: Incluir apenas kits com produtos
- `with_images`: Incluir apenas kits com imagens

## 📊 **Códigos de Status HTTP**

| Código | Descrição |
|--------|-----------|
| `200` | Sucesso |
| `201` | Criado com sucesso |
| `204` | Sucesso sem conteúdo |
| `400` | Requisição inválida |
| `401` | Não autorizado |
| `404` | Não encontrado |
| `422` | Dados inválidos |
| `500` | Erro interno do servidor |

## 🔐 **Autenticação**

A API utiliza **JWT (JSON Web Tokens)** para autenticação:

```bash
# Login
POST /api/login
{
    "email": "usuario@exemplo.com",
    "senha": "senha123"
}

# Resposta
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### **Usando o Token**
```bash
# Incluir no header Authorization
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 📝 **Exemplos de Uso**

### **1. Criar Empresa**
```bash
curl -X POST "http://localhost:8000/api/companies/" \
  -H "Content-Type: application/json" \
  -d '{
    "cnpj": "12345678000195",
    "razao_social": "Empresa Exemplo LTDA",
    "nome_fantasia": "Exemplo",
    "senha": "MinhaSenh@123",
    "endereco": {
      "cep": "01234567",
      "numero": "123",
      "complemento": "Sala 1",
      "bairro": "Centro",
      "cidade": "São Paulo",
      "uf": "SP",
      "ibge": "3550308"
    },
    "contato": {
      "nome": "João Silva",
      "telefone": "1133334444",
      "celular": "11999998888",
      "email": "joao@exemplo.com"
    }
  }'
```

### **2. Listar Produtos com Filtros**
```bash
curl -X GET "http://localhost:8000/api/produtos/?categoria_id=1&active_only=true&min_price=10&max_price=100"
```

### **3. Buscar Pedidos por Status**
```bash
curl -X GET "http://localhost:8000/api/pedidos/status/PENDENTE"
```

### **4. Listar Kits com Produtos**
```bash
curl -X GET "http://localhost:8000/api/kits/?with_products=true&active_only=true"
```

## 🏗️ **Arquitetura**

### **Padrões Utilizados**
- **Clean Architecture**: Separação clara de responsabilidades
- **Repository Pattern**: Isolamento do acesso a dados
- **Use Case Pattern**: Lógica de negócio isolada
- **Dependency Injection**: Baixo acoplamento
- **DTO Pattern**: Transferência de dados estruturada

### **Estrutura de Pastas**
```
app/
├── domain/           # Entidades e regras de negócio
├── application/      # Casos de uso e serviços
├── infrastructure/   # Repositórios e configurações
└── presentation/     # Routers e DTOs
```

## 🚀 **Como Executar**

### **1. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **2. Configurar Banco de Dados**
```bash
# Configurar variáveis de ambiente
export DATABASE_URL="mysql://usuario:senha@localhost:3306/fortlar"
```

### **3. Executar Aplicação**
```bash
python -m uvicorn app.run:application --host 0.0.0.0 --port 8000 --reload
```

### **4. Acessar Documentação**
- Swagger: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📈 **Monitoramento**

### **Health Check**
```bash
curl -X GET "http://localhost:8000/api/health"
```

### **Métricas**
- Logs estruturados
- Tratamento de exceções
- Validação de dados
- Documentação automática

## 🔧 **Desenvolvimento**

### **Adicionando Novos Endpoints**
1. Criar router em `app/presentation/routers/`
2. Implementar use case em `app/application/usecases/`
3. Adicionar repository se necessário
4. Registrar router em `fastapi_config.py`

### **Testes**
```bash
# Executar testes
pytest tests/

# Com cobertura
pytest --cov=app tests/
```

## 📞 **Suporte**

- **Email**: contato@fortlar.com
- **Documentação**: http://localhost:8000/api/docs
- **Issues**: GitHub Issues

---

**Versão**: 1.0.0  
**Última Atualização**: $(date)  
**Desenvolvido com**: FastAPI, SQLAlchemy, MySQL, Python 3.13
