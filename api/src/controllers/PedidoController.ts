import { Request, Response } from 'express'; 
import knex from '../database/connection'; 
import PedidoModel, { Pedido, PedidoProduto, Cliente } from '../models/pedido'; 

class PedidoController {
  async index(request: Request, response: Response) {
    const model = new PedidoModel();
    const pedidos = await model.listar(); 
    return response.json(pedidos);
  }

  async store(request: Request, response: Response) {
    const {cliente_id, produtos} = request.body; 
    const model = new PedidoModel();     
    try {

      //Pedido pra inserir
      const pedido: Pedido = {
        status: 0,
        cliente: {
          id: Number(cliente_id)
        } 
      }

      //Produtos pra inserir
      const produtosPedido = produtos.map((produto: any) => {
        return {
          quantidade: produto.quantidade,
          produto: {
            id: produto.produto_id
          }
        };
      });

      //Calcular o preco
      const pedido_id = await model.persistir(pedido, produtosPedido);  
      if(pedido_id > 0) {
        const preco = await model.preco(pedido_id); 
        return response.json({preco: preco}); 
      }

    } catch (error) {
      console.error(error); 
      return response.json({error: true}); 
    }
  }

  async show(request: Request, response: Response) {
    const { id } = request.params
    const model = new PedidoModel();
    const pedidos = await model.listar(Number(id)); 
    return response.json(pedidos);
  }

  async update(request: Request, response: Response) {
    const { id } = request.params
    const {cliente_id, status, produtos} = request.body; 
    const model = new PedidoModel();     
    try {

      //Pedido pra inserir
      const pedido: Pedido = {
        id: Number(id),
        status: Number(status),
        cliente: {
          id: Number(cliente_id)
        } 
      }

      //Produtos pra inserir
      const produtosPedido = produtos.map((produto: any) => {
        return {
          quantidade: produto.quantidade,
          produto: {
            id: produto.produto_id
          }
        };
      });

      //Calcular o preco
      const pedido_id = await model.persistir(pedido, produtosPedido);  
      if(pedido_id > 0) {
        const preco = await model.preco(pedido_id); 
        return response.json({preco: preco}); 
      }

    } catch (error) {
      console.error(error); 
      return response.json({error: true}); 
    }
  }

  async destroy(request: Request, response: Response) {
    const { id } = request.params
    const trx = await knex.transaction(); 
    try {
      await trx('pedido_produto')
        .where('pedido_id', id)
        .del()
      await trx('pedido')
        .where('id', id)
        .del()
      
      await trx.commit();
      return response.json({error: false}); 
    } catch (error) {
      await trx.rollback()
      return response.json({error: true});

    }
  }

} //#END PEDIDOCONTROLLER

export default PedidoController