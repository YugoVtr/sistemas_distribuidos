#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rpyc, time
import shutil, psutil
import logging, signal
from datetime import datetime
from threading import Thread

""" Classe que implementa o monitoramento do SO """
class Monitor():
    """
        Descricao: Monitora o disco principal em Gb
        Return: (Total, Usado, Livre)
    """
    def disk_monitor(self):
        total, used, free = shutil.disk_usage("/"); 
        return {
            "total": total/(10**9),
            "used": used/(10**9),
            "free": free/(10**9)
        }
    
    """
        Descricao: Monitora a quantidade de memoria em Mb
        Return: (Total, Usado, Livre)
    """
    def memory_monitor(self):
        memory = psutil.virtual_memory()
        total, used, free = memory.total, memory.used, memory.free
        return {
            "total": total/10**6,
            "used": used/10**6,
            "free": free/10**6
        }
    
    """
        Descricao: Monitora a quantidade de memoria em Mb
        Return: % de cpu utilizada
    """
    def cpu_monitor(self):
        return psutil.cpu_percent()
    
    def get_all_status(self):
        return {
            "disk": self.disk_monitor(), 
            "memory": self.memory_monitor(), 
            "cpu": self.cpu_monitor(),
            "date": datetime.today().strftime('%Y-%m-%d %H:%M')
        } 

""" Classe Cliente """
class Cliente(rpyc.Service):    
    current = None 
    
    class Daemon(object):
        def __init__(self, callback, interval=60):
            self.interval = interval
            self.callback = callback
            self.active = True
            self.thread = Thread(target = self.work)
            self.thread.start()
                    
        def stop(self):
            logging.info("Encerrando cliente")
            self.active = False
            self.thread.join()
        
        def work(self):
            logging.info("Monitoramento iniciado - Precione 'Ctrl+C' para encerrar.")
            while self.active:
                if callable( self.callback ):    
                    m = Monitor()
                    logging.info("Enviando ao servidor...")
                    self.callback( m.get_all_status() )
                time.sleep(self.interval)
        
        def update(self):
            m = Monitor()
            self.callback( m.get_all_status() )
    
    def on_connect(self, conn):
        self.current = self.Daemon(conn.root.save)
    
    def on_disconnect(self, conn):
        self.current.stop()


conn = None

def handler(signal, frame):
    global conn
    conn.close()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s|%(levelname)s --> %(message)s",
        datefmt="%d/%m/%Y %H:%M"
    )
    signal.signal(signal.SIGINT, handler)
    conn = rpyc.connect("127.0.0.1", 18861, service=Cliente)
