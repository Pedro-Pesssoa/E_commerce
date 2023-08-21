def formata_preco(val):
    return f'{val:.2f}'.replace(',','.')

def cart_total_qtd(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])
