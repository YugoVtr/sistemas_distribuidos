#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rpyc 
import shutil, psutil
from datetime import datetime

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
    def exposed_callback(self):
        run_client()

def send_to_server(connection):
    m = Monitor()   
    connection.root.save(m.get_all_status())

def run_client():
    connection = rpyc.connect("127.0.0.1", 18861, service=Cliente)
    send_to_server(connection)
    connection.root.poll()
    
if __name__ == "__main__":
    run_client()   