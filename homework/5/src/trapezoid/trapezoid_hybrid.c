#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <math.h>


double Trap(double l, double r, int count, double h)
{
    double estimate, x;
    int i;

    estimate = (exp(l) + exp(r))/2.0;

    #pragma omp parallel for reduction(+:estimate)
    for (i = 1; i <= count-1; i++)
    {
        x = l + i * h;
        estimate += exp(x);
    }

    estimate = estimate * h;

    return estimate;
}


double reduce(double a, double b, int n, int my_rank, int comm_sz)
{
    int local_n, source;
    double h, chunk_size, local_a, local_b;
    double local_int=0, total_int=0;

    // h will be the same for all processes
    h = (b - a)/n;

    // determine local_a and local_b values for each MPI process
    // for simplicity, you can assume n to be a perfect multiple of comm_sz
    chunk_size = (b - a)/comm_sz;
    local_a = a + my_rank*chunk_size;
    local_b = local_a + chunk_size;
    local_int = Trap(local_a, local_b, n/comm_sz, h);

    // aggregate the partial results at the root (MPI rank = 0) process
    // using MPI collective operation(s).
    MPI_Reduce(&local_int, &total_int, 1, MPI_DOUBLE, MPI_SUM, 0,
            MPI_COMM_WORLD);

    return total_int;
}


int main(int argc, char* argv[])
{
    int my_rank, comm_sz, n;
    double a=0, b=1;
    double integral, solution;
    double t_start, t_end;

    MPI_Init(NULL, NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);

    if (argc == 2) {
        // get the command line arguments
        n = strtol(argv[1], NULL, 10);
    }
    else {
        fprintf(stderr, "\nERROR: This program requires 1 command-line input:\n");
        fprintf(stderr, "         n: number of sample points\n");
        exit(1);
    }

    if (my_rank == 0) {
        printf("#procs = %d\n", comm_sz);
        printf("#trapezoids = %d\n", n);
        printf("Interval %f to %f\n", a, b);
        solution = exp(b) - exp(a);
        printf("Analytic solution = %.15e\n", solution);
    }

    MPI_Barrier(MPI_COMM_WORLD);

    t_start = MPI_Wtime();
    integral = reduce(a, b, n, my_rank, comm_sz);
    t_end = MPI_Wtime();

    if (my_rank == 0)
    {
        if (integral >= 0.99*solution && integral <= 1.01 * solution)
        {
            printf("\n\nRIGHT SOLUTION!\n");
            printf("Integral = %.15e\n", integral);
            printf("Time = %.6f\n", (t_end - t_start));
        }
        else
        {
            printf("\n\nWRONG SOLUTION!\n");
            printf("Integral = %.15e\n", integral);
            printf("Time = %.6f\n", (t_end - t_start));
        }
    }

    MPI_Finalize();
    return 0;
}
