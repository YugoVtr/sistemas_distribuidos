import Knex from 'knex'; 

//Create
export async function up(knex: Knex) {
  return knex.schema.createTable('produto', table => {
    table.increments('id').primary(); 
    table.string('descricao').notNullable();
    table.decimal('preco').notNullable();
    table.integer('quantidade_estoque').notNullable();
  });
}

//Reset
export async function down(knex: Knex) {
  return knex.schema.dropTable('produto'); 
}