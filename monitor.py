from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Value, Array
from multiprocessing import current_process
import threading


class Table():
    def __init__(self,NPHIL,manager):
        self.current_phil = None 
        self.phil = manager.list([False]*NPHIL)
        self.neating = Value('i',0)
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)


    def no_comen_lados(self):
        return(not(self.phil[(self.current_phil+1)%len(self.phil)]) and not(self.phil[(self.current_phil-1)%len(self.phil)]))
     
        
    def set_current_phil(self,i):
        self.current_phil = i
    
    
    def wants_eat(self,i):
        self.mutex.acquire()
        self.freefork.wait_for(self.no_comen_lados)
        self.phil[i] = True
        self.neating.value+=1
        self.mutex.release()
      
        
    def wants_think(self,i):
        self.mutex.acquire()
        self.freefork.notify()
        self.phil[i] = False
        self.neating.value-=1
        self.freefork.notify_all()
        self.mutex.release()
  
    

class CheatMonitor():
    
    def __init__(self):
        self.forks = [threading.Semaphore(1) for i in range(2)]
        self.neating = Value('i',0)
          
    def is_eating(self, N):      
        if N==0:
            self.forks[0].release() #signal tenedor 0
            self.forks[1].acquire() #wait tenedor 1
        if N==2:
            self.forks[1].release()
            self.forks[0].acquire()
            
        self.neating.value+=1

       
    def wants_think(self,N):
        if N==0:
            self.forks[0].acquire() #wait tenedor 0
            self.forks[1].release() #signal tenedor 1
        if N==2:
            self.forks[1].acquire()
            self.forks[0].release()
           
        self.neating.value-=1

        
        