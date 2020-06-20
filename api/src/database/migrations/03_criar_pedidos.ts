import Knex from 'knex';

//Create
export async function up(knex: Knex) {
  return knex.schema.createTable('pedido', table => {
    table.increments('id').primary();
    table.timestamp('data_pedido').defaultTo(knex.fn.now());
    table.timestamp('data_entrega');
    table.integer('status').notNullable();

    table.integer('cliente_id')
      .notNullable()
      .references('id')
      .inTable('cliente');
  });
}

//Reset
export async function down(knex: Knex) {
  return knex.schema.dropTable('pedido');
}