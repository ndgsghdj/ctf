#!/usr/bin/python3

from pwn import *
from queue import Queue
from threading import Thread

elf = context.binary = ELF('./vuln')

class Guesser:
	def __init__(self,max_threads):
		self.max_threads = max_threads
		self.guess_queue = Queue()
		for guess in range(-4095,4097):
			self.guess_queue.put(guess)
		self.current_threads = 0
		self.isFound = False
		self.found = 0
		
	def start(self):
		while not self.isFound:
			if self.current_threads <= self.max_threads:
				thread = Thread(target=self.thread_func)
				thread.start()
				self.current_threads += 1
		return self.found
	
	def thread_func(self):
		if self.isFound:
			return
		proc = process('./vuln')
		proc.recvlines(4)
		guess = self.guess_queue.get(block=True)
		info("Guessing {}...".format(guess))
		proc.sendline(str(guess))
		resp = proc.recvline().decode().strip()
		proc.recvline()
		proc.close()
		if "Congrats" in resp:			
			self.isFound = True
			self.found = guess
		self.current_threads -= 1
		return



# DRIVER
max_threads = 20
info("Using {} max threads".format(max_threads))
guesser = Guesser(max_threads)
guess = guesser.start()
info("CORRECTLY GUESSED VALUE -> {}".format(guess))
