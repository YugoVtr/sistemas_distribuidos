import express from 'express';
import ProdutoController from './controllers/ProdutoController'; 
import PedidoController from './controllers/PedidoController'; 
import ClienteController from './controllers/ClienteController'; 

const routes = express.Router(); 
const produtoController = new ProdutoController(); 
const pedidoController = new PedidoController(); 
const clienteController = new ClienteController(); 

routes.get('/cliente', clienteController.index);
routes.get('/produto', produtoController.index);
routes.get('/pedido', pedidoController.index);
routes.post('/pedido', pedidoController.store);
routes.get('/pedido/:id', pedidoController.show);
routes.put('/pedido/:id', pedidoController.update);
routes.delete('/pedido/:id', pedidoController.destroy);

export default routes; 