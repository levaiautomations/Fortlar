"""Template HTML para email de pedido"""


def pedido_html(itens: list, valor_total: float, forma_pagamento: str) -> str:
    """
    Gera HTML formatado para email de pedido
    
    Args:
        itens: Lista de itens com informações do produto (nome, quantidade, preco_unitario, subtotal)
        valor_total: Valor total do pedido
        forma_pagamento: Forma de pagamento escolhida
    
    Returns:
        HTML formatado do pedido
    """
    
    # Constrói a tabela de itens
    itens_html = ""
    for item in itens:
        nome_produto = item.get('nome', 'Produto')
        quantidade = item.get('quantidade', 0)
        preco_unitario = item.get('preco_unitario', 0.0)
        subtotal = item.get('subtotal', 0.0)
        
        itens_html += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">{nome_produto}</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: center;">{quantidade}</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: right;">R$ {preco_unitario:.2f}</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd; text-align: right;">R$ {subtotal:.2f}</td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pedido - Fortlar</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .header {{
                background-color: #2c3e50;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                padding: 30px;
            }}
            .section {{
                margin-bottom: 30px;
            }}
            .section-title {{
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th {{
                background-color: #3498db;
                color: #ffffff;
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }}
            th.text-center {{
                text-align: center;
            }}
            th.text-right {{
                text-align: right;
            }}
            td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}
            .total-section {{
                background-color: #ecf0f1;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .total-row {{
                display: flex;
                justify-content: space-between;
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
            }}
            .payment-info {{
                background-color: #e8f5e9;
                padding: 15px;
                border-radius: 5px;
                border-left: 4px solid #4caf50;
            }}
            .payment-info strong {{
                color: #2c3e50;
            }}
            .footer {{
                background-color: #34495e;
                color: #ffffff;
                padding: 15px;
                text-align: center;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛒 Novo Pedido - Fortlar</h1>
            </div>
            
            <div class="content">
                <div class="section">
                    <div class="section-title">Itens do Pedido</div>
                    <table>
                        <thead>
                            <tr>
                                <th>Produto</th>
                                <th class="text-center">Quantidade</th>
                                <th class="text-right">Preço Unitário</th>
                                <th class="text-right">Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            {itens_html}
                        </tbody>
                    </table>
                </div>
                
                <div class="total-section">
                    <div class="total-row">
                        <span>Total do Pedido:</span>
                        <span>R$ {valor_total:.2f}</span>
                    </div>
                </div>
                
                <div class="section">
                    <div class="payment-info">
                        <strong>Forma de Pagamento:</strong> {forma_pagamento}
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>Este é um email automático. Por favor, não responda.</p>
                <p>&copy; 2024 Fortlar. Todos os direitos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

