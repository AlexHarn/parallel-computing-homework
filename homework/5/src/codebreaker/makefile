CC=mpicc
LIBS=-lm

all: block_codebreaker.x cyclic_codebreaker.x sequential_codebreaker.x encrypter.x

block_codebreaker.x: codebreaker.c
	$(CC) $(LIBS) $< -o $@

cyclic_codebreaker.x: cyclic_codebreaker.c
	$(CC) $(LIBS) $< -o $@
	
sequential_codebreaker.x: sequential_codebreaker.c
	$(CC) $(LIBS) $< -o $@

encrypter.x: encrypter.c
	$(CC) $(LIBS) $< -o $@

clean:
		rm -f *.o
		rm -f *.x
