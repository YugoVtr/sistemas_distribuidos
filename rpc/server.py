#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rpyc, threading
from rpyc.utils.server import ThreadedServer
from pymongo import MongoClient

"""
Instrucoes
O sistema deve permitir que um servidor receba dados de desempenho de varios 
hosts em uma rede:
 - % de utilização de CPU, 
 - Memoria: Qtde Utilizada / Qtde Disponivel,
 - Disco: Qtde Utilizada / Qtde Disponivel),
 - Gere um relatorio de desempenho.

PARTE I:

Cada cliente deve enviar essas informacoes ao servidor periodicamente (N segundos)
O servidor deve armazenar os dados de cada cliente em um banco de dados local.
 
PARTE II:

O servidor deve poder solicitar explicitamente que um cliente específico envie
suas informações (polling)

Mongo Pwd: 0BTgfcX0dYeiIrdX
Mongo URL: mongodb+srv://yugo:0BTgfcX0dYeiIrdX@default-qmfnx.mongodb.net/test?retryWrites=true&w=majority
"""

""" Classe para manipular o banco de dados """
class Model():
    def __init__(self):
        url = "mongodb+srv://yugo:0BTgfcX0dYeiIrdX@default-qmfnx.mongodb.net/test?retryWrites=true&w=majority"
        client = MongoClient(url)
        db = client.get_database('monitor_db')
        self.records = db.monitor_records

    def delete_all(self):
        self.records.delete_many({})     
        
    def insert(self, obj):
        try:    
            self.records.insert_one(obj)
        except: 
            # Ta dando erro ao inserir, mas ta inserindo, 
            # entao to ignorando por hora
            pass
        
    def list_all(self):
        return list( self.records.find({}) )          
 
""" Classe do RPyC que manipula as coneccoes """       
class Servidor(rpyc.Service):
    def __init__(self):
        self.model = Model()
        self.connections = []
    
    def on_connect(self, conn):
        self.connections.append(conn)      
        
    def on_disconnect(self, conn):
        self.connections.remove(conn)

    def exposed_save(self, obj): 
        self.model.insert(obj)
        
    def poll(self):
        for conn in self.connections:
            conn.root.callback()
    
def run_server():
    t = ThreadedServer(Servidor, port=18861)
    t.start()
                
if __name__ == "__main__":
    run_server()
    # t = threading.Thread(target=run_server)
    # t.start()
