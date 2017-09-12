#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Junkai Huang"


import redis
import time
import configparser
from pprint import pprint


config = configparser.ConfigParser()
config.read('setting.ini')


POOL = redis.ConnectionPool(host=config['basic']['redis_bind_host'], 
                            port=config['basic']['redis_bind_port'], 
                            db=config['basic']['redis_bind_dp'])

VNEUES = list(config['basic']['badminton_vneues'].replace(' ','').split(','))


def initialize(pool):
    print("Initialize the database.....", end="")

    try:
        conn = redis.Redis(connection_pool=pool) 
        #Initialize the information of badminton venues
        if conn.exists('badminton_vneues'):
            conn.delete('badminton_vneues')

        for vneue in VNEUES:
            conn.rpush("badminton_vneues" ,vneue)

        time.sleep(1)
        print("Done")
    except Exception as e:
        print("Failed")
        print("ERROR INFO:", str(e))

    print("Initialize the system.....", end="")

    prices = {}
    try:
        groups = config['basic']['working_day_groups'].replace(' ','').split(',')
        for group in groups:
            working_days = list(map(int, config[group]['working_days'].replace(' ','').split(',')))
            if config[group].get('price'):
                temp = list(map(eval,config[group]['price'].replace(' ','').split(';')))
            else:
                temp = list(map(eval,config['basic']['price'].replace(' ','').split(';')))
            if config[group].get('working_hours_start'):
                working_hours_start = int(config[group]['working_hours_start'])
            else:
                working_hours_start = int(config['basic']['working_hours_start'])
            if config[group].get('working_hours_end'):
                working_hours_end = int(config[group]['working_hours_end'])
            else:
                working_hours_end = int(config['basic']['working_hours_end'])

            prices[group] = {"start": working_hours_start,
                             "end": working_hours_end,
                             "working_days": working_days,
                             "price":[0 for i in range(25)]}

            index = working_hours_start
            for (dur, gold) in temp:
                for i in range(dur+1):
                    prices[group]['price'][index+i] = gold
                index += dur
               
        time.sleep(1)
        print("Done")
    except Exception as e:
        print("Failed")
        print("ERROR INFO:", str(e))

        pprint(prices)
    return prices


