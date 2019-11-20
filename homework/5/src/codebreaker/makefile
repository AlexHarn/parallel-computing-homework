CC=mpicc
LIBS=-lm

all: codebreaker.x cyclic_codebreaker.x sequential_codebreaker.x encrypter.x

codebreaker.x: codebreaker.c
	$(CC) $(LIBS) $< -o $@

cyclic_codebreaker.x: codebreaker.c
	$(CC) $(LIBS) $< -o $@
	
sequential_codebreaker.x: codebreaker.c
	$(CC) $(LIBS) $< -o $@

encrypter.x: encrypter.c
	$(CC) $(LIBS) $< -o $@

clean:
		rm -f *.o
		rm -f *.x
