import Knex from 'knex'
import faker from 'faker'

export async function seed(knex: Knex) {
  let seeds = [];
  for (let i = 0; i < 10; i++) {
    seeds.push({
      descricao: faker.commerce.productName(),
      preco: faker.commerce.price(),
      quantidade_estoque: faker.random.number({
        'min': 1,
        'max': 50
      })
    });
  }
  await knex('produto').insert(seeds);
}