import knex from '../database/connection'; 

interface Cliente { 
  id: Number; 
  nome?: String; 
  contato?: String; 
  endereco?: String; 
}

interface Pedido {
  id?: Number;
  data_pedido?: String;
  data_entrega?: String;
  status: Number;
  cliente: Cliente;
}

interface Produto { 
  id: Number;
  descricao?: String; 
  preco?: Number;
  quantidade_estoque?: Number; 
}

interface PedidoProduto {
  produto: Produto; 
  pedido: Pedido;
  quantidade: Number; 
}


class PedidoModel {
  async listar(id: Number = 0) {
    let pedidos:any[]; 
    if(id > 0) {
      pedidos = await knex('pedido').select('*').where('id', id);
    } else {
      pedidos = await knex('pedido').select('*');
    }

    const listaDePromisses = pedidos.map( async (pedido: any) => {
      const cliente = await knex('cliente')
        .where('id', pedido.cliente_id)
        .select('*');

      const produto = await knex('pedido_produto')
        .join('produto', 'pedido_produto.produto_id', '=', 'produto.id')
        .where('pedido_produto.pedido_id', pedido.id)
        .select('produto.id', 'produto.descricao', 'produto.preco', 'pedido_produto.quantidade');

      return {
        id: pedido.id,
        data_pedido: pedido.data_pedido, 
        data_entrega: pedido.data_entrega,
        status: pedido.status,
        cliente: cliente[0], 
        produto: produto
      }
    })
    
    const pedidoCompleto = await Promise.all(listaDePromisses);
    return pedidoCompleto; 
  }

  async preco(id: Number) { 
    const produtos = await this.listar(id); 
    return produtos[0].produto.reduce((preco, eachProduto) => {
      return preco + eachProduto.quantidade * eachProduto.preco; 
    }, 0)
  }

  async persistir(pedido:Pedido, produtos:PedidoProduto[]) {
    const trx = await knex.transaction(); 
    
    try {

      const pedidoToInsert: any = {
        cliente_id: pedido.cliente.id, 
        status: pedido.status
      };

      if (pedido.id) {
        //Atualizar o pedido
        await trx('pedido')
          .where('id', '=', pedido.id)
          .update(pedidoToInsert);
          
        let item: any = produtos.pop(); 
        while (item) {
          await trx('pedido_produto')
            .where('pedido_id', '=', pedido.id)
            .update({
              quantidade: item.quantidade, 
            });  
          item = produtos.pop()
        }

        await trx.commit();
        return pedido.id;

      } else {
        //Criar Pedidos novos
        const ids = await trx('pedido').insert(pedidoToInsert);
        const pedido_id = Number( ids.pop() ); 
        const pedidoProduto = produtos.map((items) => {
          return {
            pedido_id,
            quantidade: items.quantidade, 
            produto_id: items.produto.id
          };
        });
        await trx('pedido_produto').insert(pedidoProduto);      
        await trx.commit();
        return pedido_id; 
      }
    } catch (error) {
      await trx.rollback()
      return 0;
    }
  }
}

export { Cliente, Pedido, Produto, PedidoProduto }
export default PedidoModel