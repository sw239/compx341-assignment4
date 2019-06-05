import time
import math
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def stored_primes():
	return str(cache.lrange('primes',0,-1))+"\n"

def detect_num(n):
        if n==2:
                cache.lpush('primes',n)
                return True
        x=n%2
        if x==0:
                return False
        else:
                x=3
                while(x<=math.sqrt(n)):
                        a=n%x
                        if a==0:
                                return False
                        else:
                                x=x+1
                                a=x%2
                                if a==0:
                                        x=x+1             
                
                return True
                        



@app.route('/Prime/<int:number>')
def detect(number):
    status=detect_num(number)
    if status:
        cache.lpush('primes',number)
        return '{} is prime\n'.format(number)
    else:
        return '{} is not prime\n'.format(number)

@app.route('/primeStored')

def display():
	return stored_primes()
