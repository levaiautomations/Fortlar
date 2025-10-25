#!/usr/bin/env python3
"""
Script para criar um arquivo Excel de exemplo para teste da funcionalidade de upload
"""

import pandas as pd
import os

def create_example_excel():
    """Cria um arquivo Excel de exemplo com dados de produtos"""
    
    # Dados de exemplo
    produtos_data = {
        'codigo': [
            'PROD001', 'PROD002', 'PROD003', 'PROD004', 'PROD005',
            'PROD006', 'PROD007', 'PROD008', 'PROD009', 'PROD010'
        ],
        'nome': [
            'Smartphone Samsung Galaxy S24',
            'Notebook Dell Inspiron 15',
            'Fone de Ouvido Bluetooth Sony',
            'Smartwatch Apple Watch Series 9',
            'Tablet iPad Air 5',
            'Câmera Canon EOS R6',
            'Monitor LG UltraWide 34"',
            'Teclado Mecânico Logitech',
            'Mouse Gamer Razer DeathAdder',
            'Webcam Logitech C920'
        ],
        'descricao': [
            'Smartphone Android com tela de 6.2" e câmera de 50MP',
            'Notebook com processador Intel i7 e 16GB RAM',
            'Fone sem fio com cancelamento de ruído',
            'Relógio inteligente com GPS e monitor cardíaco',
            'Tablet com tela Retina de 10.9" e chip M1',
            'Câmera mirrorless full-frame com 24MP',
            'Monitor ultrawide 4K com taxa de 144Hz',
            'Teclado mecânico com switches Cherry MX',
            'Mouse gamer com sensor óptico de 16.000 DPI',
            'Webcam Full HD com microfone integrado'
        ],
        'id_categoria': [1, 2, 3, 4, 2, 5, 2, 6, 6, 6],
        'id_subcategoria': [1, 1, 2, 1, 2, 1, 2, 1, 2, 3],
        'valor_base': [2999.99, 4599.00, 299.90, 3999.00, 5999.00, 
                      8999.00, 2499.00, 399.90, 199.90, 299.90],
        'ativo': [True, True, True, True, True, True, True, True, True, True]
    }
    
    # Cria DataFrame
    df = pd.DataFrame(produtos_data)
    
    # Cria arquivo Excel com múltiplas abas
    with pd.ExcelWriter('exemplo_produtos.xlsx', engine='openpyxl') as writer:
        # Aba com dados dos produtos
        df.to_excel(writer, sheet_name='Produtos', index=False)
        
        # Aba com instruções
        instrucoes = pd.DataFrame({
            'Coluna': ['codigo', 'nome', 'descricao', 'id_categoria', 'id_subcategoria', 'valor_base', 'ativo'],
            'Obrigatório': ['Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Sim', 'Sim'],
            'Tipo': ['Texto', 'Texto', 'Texto', 'Número', 'Número', 'Número', 'Boolean'],
            'Descrição': [
                'Código único do produto (máximo 50 caracteres)',
                'Nome do produto (máximo 150 caracteres)',
                'Descrição detalhada (opcional)',
                'ID da categoria (deve existir no banco de dados)',
                'ID da subcategoria (deve existir no banco de dados)',
                'Valor base do produto (formato: 999.99)',
                'Status ativo (true/false, 1/0, sim/não)'
            ],
            'Exemplo': [
                'PROD001',
                'Smartphone Samsung Galaxy S24',
                'Smartphone Android com tela de 6.2"',
                '1',
                '1',
                '2999.99',
                'true'
            ]
        })
        instrucoes.to_excel(writer, sheet_name='Instruções', index=False)
        
        # Aba com categorias disponíveis (exemplo)
        categorias = pd.DataFrame({
            'id_categoria': [1, 2, 3, 4, 5, 6],
            'nome_categoria': [
                'Smartphones', 'Computadores', 'Áudio', 'Wearables', 
                'Fotografia', 'Periféricos'
            ]
        })
        categorias.to_excel(writer, sheet_name='Categorias', index=False)
        
        # Aba com subcategorias disponíveis (exemplo)
        subcategorias = pd.DataFrame({
            'id_subcategoria': [1, 2, 3],
            'nome_subcategoria': ['Eletrônicos', 'Acessórios', 'Periféricos'],
            'id_categoria': [1, 1, 6]
        })
        subcategorias.to_excel(writer, sheet_name='Subcategorias', index=False)
    
    print("Arquivo 'exemplo_produtos.xlsx' criado com sucesso!")
    print("\nConteúdo do arquivo:")
    print("- Aba 'Produtos': 10 produtos de exemplo")
    print("- Aba 'Instruções': Como preencher a planilha")
    print("- Aba 'Categorias': Categorias disponíveis")
    print("- Aba 'Subcategorias': Subcategorias disponíveis")
    print("\nPara testar:")
    print("1. Execute o servidor: uvicorn app.run:app --reload")
    print("2. Acesse: http://localhost:8000/docs")
    print("3. Teste o upload: POST /produtos/upload-excel")

if __name__ == "__main__":
    create_example_excel()
