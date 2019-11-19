CC=mpicc
LIBS=-lm

trapezoid:
		$(CC) -fopenmp -o hybrid_trapezoid.x trapezoid.c $(LIBS)
		$(CC) -o mpi_only_trapezoid.x trapezoid.c $(LIBS)

.PHONY: clean

clean:
		rm -f *.o
		rm -f trapezoid
