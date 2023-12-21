CC=gcc

all: libsimple.a

simple.o: simple.cpp simple.h
	$(CC) -O -c simple.cpp

libsimple.a: simple.o
	ar rcs libsimple.a simple.o

libs: libsimple.a