CC=mpicc
LIBS=-lm

all: bucket_sort_v1.x bucket_sort_v2.x bucket_sort_v2_square.x bucket_sort_v3.x

bucket_sort_v1.x: bucket_sort_v1.c
	$(CC) $(LIBS) $< -o $@

bucket_sort_v2.x: bucket_sort_v2.c
	$(CC) $(LIBS) $< -o $@
	
bucket_sort_v2_square.x: bucket_sort_v2_square.c
	$(CC) $(LIBS) $< -o $@
	
bucket_sort_v3.x: bucket_sort_v3.c
	$(CC) $(LIBS) $< -o $@

clean:
		rm -f *.o
		rm -f *.x
