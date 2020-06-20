import Knex from 'knex'
import faker from 'faker'

export async function seed(knex: Knex) {
  let seeds = [];
  for (let i = 0; i < 10; i++) {
    seeds.push({
      nome: faker.name.findName(),
      contato: faker.internet.email(),
      endereco: faker.address.streetAddress()
    });
  }
  await knex('cliente').insert(seeds);
}