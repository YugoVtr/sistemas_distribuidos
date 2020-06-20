import { Request, Response } from 'express'; 
import knex from '../database/connection'; 

class ClienteController {
  async index(request: Request, response: Response) {
    const clientes = await knex('cliente').select('*');
    return response.json(clientes);
  }
}

export default ClienteController