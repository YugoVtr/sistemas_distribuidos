import { Request, Response } from 'express'; 
import knex from '../database/connection'; 

class ProdutoController {
  async index(request: Request, response: Response) {
    const produto = await knex('produto').select('*');
    return response.json(produto);
  }
}

export default ProdutoController