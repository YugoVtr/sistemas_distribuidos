import Knex from 'knex'; 

//Create
export async function up(knex: Knex) {
  return knex.schema.createTable('pedido_produto', table => {
    table.integer('quantidade').notNullable();

    table.integer('produto_id')
      .primary()
      .notNullable()
      .references('id')
      .inTable('produto'); 
      
    table.integer('pedido_id')
      .primary()
      .notNullable()
      .references('id')
      .inTable('pedido'); 
  });
}

//Reset
export async function down(knex: Knex) {
  return knex.schema.dropTable('pedido_produto'); 
}