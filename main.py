#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Junkai Huang"


import redis
import time
import readline

from init import POOL, VNEUES, initialize
from datetime import datetime

from pprint import pprint

class BVM(object):
    def __init__(self):
        super(BVM, self).__init__()

        self.pool = POOL

        self.conn = redis.Redis(connection_pool=self.pool)
        
        try:
            self.prices = initialize(self.pool)
        except Exception as e:
            print("ERROR 11: failed to initialize.")

    def _check_time(self, args):
        
       try:
           user = args[0]
           date = args[1]
           time = args[2].split('~')
           start_time = datetime.strptime(date+" "+time[0], "%Y-%m-%d %H:%M") 
           end_time = datetime.strptime(date+" "+time[1], "%Y-%m-%d %H:%M")
           if start_time.minute or end_time.minute:
               raise 
       except Exception as e:
           print(str(e))
           print("ERROR: the booking is invalid!")
           raise
       return user, start_time, start_time.hour, end_time.hour, start_time.weekday()+1



    def book(self, args):
       try:
           user, start_time, start, end, weekday = self._check_time(args)
           unix_ts = 1439111214.0
           timestamp = time.mktime(start_time.timetuple())
  
           if not self.conn.exists(args[1]):
               self.conn.set(args[1], str([0 for i in range(25)]))

           busy = eval(self.conn.get(args[1]))
           for i in range(start, end):
               if busy[i] == 1:
                   raise ValueError("Error: the booking conflicts with existing bookings!")
           income = 0

           price = self.prices['GroupOne']['price']
           if weekday in self.prices['GroupOne']['working_days']:
               price = self.prices['GroupTwo']['price']
               
           for i in range(start, end):
               income += price[i]           

           record = "%s %s %s %d" %(args[0], args[1], args[2], income)
           #print("record", record)
           self.conn.zadd(args[-1], record, timestamp)

           for i in range(start, end):
               busy[i] = 1
               self.conn.set(args[1], str(busy))
           print("Success: the booking is accepted!")
       except Exception as e:
           print(e)
           pass

        
    def cancel(self, args):
       try:
           user, start_time, start, end, weekday = self._check_time(args)
           unix_ts = 1439111214.0
           timestamp = time.mktime(start_time.timetuple())
 
     
           income = 0

           price = self.prices['GroupOne']['price']
           if weekday in self.prices['GroupOne']['working_days']:
               price = self.prices['GroupTwo']['price']
               
           for i in range(start, end):
               income += price[i]           
         
           record = "%s %s %s %d" %(args[0], args[1], args[2], income)
           if self.conn.zscore(args[-1], record):
               self.conn.zrem(args[-1], record)
          
                
               radio = 0.5
               if weekday in self.prices['GroupOne']['working_days']:
                   radio = 0.25
               new = list(record.split(' '))
               new[-1] = float(new[-1])*radio
               new_record = "%s %s %s %s" %(new[0], new[1], new[2], new[3])

               self.conn.zadd(args[-1], new_record, timestamp)
           else:
               raise ValueError("Error: the booking being cancelled does not exist!")

           busy = eval(self.conn.get(args[1]))
           for i in range(start, end):
               busy[i] = 0
           self.conn.set(args[1], str(busy))
           print("Success: the booking is accepted!")
       except Exception as e:
           print(e)
           pass


    def print_income(self):
        print("收⼊汇总:\n---")

        all_income = 0.0
        for vneue in VNEUES:
            print("场地:%s" %vneue)
            income = 0.0
            for record in self.conn.zscan_iter(vneue):
                show = record[0].decode().split(' ')
                income += float(show[3])
                if '.' in show[-1]:
                    print("%s %s 违约⾦ %s元" %(show[1], show[2], show[3]))
                else:
                    print("%s %s %s元" %(show[1], show[2], show[3]))
            print("⼩计: %s元\n" %str(income))


            all_income += income
        print("---\n总计: %s元" %str(all_income))


    def delete_all(self):
        print("Deleting....",end="")
        for vneue in VNEUES:
            for record in self.conn.zscan_iter(vneue):
                show = record[0].decode()
                try:
                    self.conn.zrem(vneue, show)
                except Exception as e:
                    pass
                show = show.split(' ')
                busy = eval(self.conn.get(show[1]))
                for i in range(len(busy)):
                    busy[i] = 0
                self.conn.set(show[1], str(busy))
             
        print("Done")



if __name__ == "__main__":
    print("Hello! Welcome to Badminton Vneues Management System(BVMS).")
    handler = BVM()
    print("Input 'quit' to exit. ")
    while(True):
        the_input = input("(BVMS)> ")

        # quit
        if the_input == "quit":
            print("Bye")
            break
        # the_input = "U123 2017-09-12 20:00~22:00 A"
        words = [i for i in the_input.split(' ') if i]
        operate = ""
        if the_input:
            operate = words[-1]
        try:
            if operate == "":
                handler.print_income()
            elif operate == "clear":
                the_input = input("Are you sure? (Y/N)\nConfirm:")
                if the_input != 'Y':
                    raise
                handler.delete_all()
            elif len(words) == 4 and operate in VNEUES:
                handler.book(words)
            elif len(words) == 5 and operate == 'C':
                handler.cancel(words[:-1])
            else:
                print("ERROR: the booking is invalid!")
        except Exception as e:
            pass
