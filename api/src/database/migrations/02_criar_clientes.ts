import Knex from 'knex'; 

//Create
export async function up(knex: Knex) {
  return knex.schema.createTable('cliente', table => {
    table.increments('id').primary(); 
    table.string('nome').notNullable(); 
    table.string('contato').notNullable();
    table.string('endereco').notNullable();
  });
}

//Reset
export async function down(knex: Knex) {
  return knex.schema.dropTable('cliente'); 
}