#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <math.h>


double Trap(double l, double r, int count, double h)
{
    double estimate, x;
    int i;

    estimate = (exp(l) + exp(r))/2.0;

    for (i = 1; i <= count-1; i++) {
        x = l + i * h;
        estimate += exp(x);
    }

    estimate = estimate * h;

    return estimate;
}


double p2p_reduce(double a, double b, int n, int my_rank, int comm_sz)
{
    int local_n, source;
    double h, chunk_size, local_a, local_b;
    double local_int=0, total_int=0;

    // aggregate the partial results at the root (MPI rank = 0) process
    // using point-to-point communication primitives, i.e. MPI_Send and MPI_Recvs
    if ( my_rank == 0 )
    {
        for ( int chunk = 1; chunk < comm_sz; chunk++ )
        {
            MPI_Recv(&local_int, 1, MPI_DOUBLE, chunk, MPI_ANY_TAG,
                    MPI_COMM_WORLD, MPI_STATUS_IGNORE);

            total_int += local_int;
        }
        return total_int;
    }

    // h will be the same for all processes
    h = (b - a)/n;

    // determine local_a and local_b values for each MPI process
    // for simplicity, you can assume n to be a perfect multiple of comm_sz
    chunk_size = (b - a)/(comm_sz - 1);
    local_a = a + (my_rank - 1)*chunk_size;
    local_b = local_a + chunk_size;
    local_int = Trap(local_a, local_b, n/(comm_sz - 1), h);
    return MPI_Send(&local_int, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
}


double coll_reduce(double a, double b, int n, int my_rank, int comm_sz)
{
    int local_n, source;
    double h, chunk_size, local_a, local_b;
    double local_int=0, total_int=0;

    if ( my_rank > 0 )
    {
        // h will be the same for all processes
        h = (b - a)/n;

        // determine local_a and local_b values for each MPI process
        // for simplicity, you can assume n to be a perfect multiple of comm_sz
        chunk_size = (b - a)/(comm_sz - 1);
        local_a = a + (my_rank - 1)*chunk_size;
        local_b = local_a + chunk_size;
        local_int = Trap(local_a, local_b, n/(comm_sz - 1), h);
    }

    // aggregate the partial results at the root (MPI rank = 0) process
    // using MPI collective operation(s).
    MPI_Reduce(&local_int, &total_int, 1, MPI_DOUBLE, MPI_SUM, 0,
            MPI_COMM_WORLD);

    return total_int;
}


int main(int argc, char* argv[])
{
    int my_rank, comm_sz, n;
    int trial, ntrials = 10;
    double a=0, b=1;
    double p2p_integral, coll_integral, solution;
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
    for (trial = 0; trial < ntrials; ++trial)
        p2p_integral = p2p_reduce(a, b, n, my_rank, comm_sz);
    t_end = MPI_Wtime();

    if (my_rank == 0) {
        if (p2p_integral >= 0.99*solution && p2p_integral <= 1.01 * solution) {
            printf("\n\nRIGHT Point-to-Point SOLUTION!\n");
            printf("Integral = %.15e\n", p2p_integral);
            printf("Time = %.6f\n", (t_end - t_start)/ntrials);
        }
        else
            printf("\n\nWRONG Point-to-Point SOLUTION!\n");
            printf("Integral = %.15e\n", p2p_integral);
            printf("Time = %.6f\n", (t_end - t_start)/ntrials);
    }

    MPI_Barrier(MPI_COMM_WORLD);

    t_start = MPI_Wtime();
    for (trial = 0; trial < ntrials; ++trial)
        coll_integral = coll_reduce(a, b, n, my_rank, comm_sz);
    t_end = MPI_Wtime();

    if (my_rank == 0) {
        if (coll_integral >= 0.99*solution && coll_integral <= 1.01 * solution) {
            printf("\n\nRIGHT Collectives SOLUTION!\n");
            printf("Integral = %.15e\n", coll_integral);
            printf("Time = %.6f\n", (t_end - t_start)/ntrials);
        }
        else
            printf("\n\nWRONG Collectives SOLUTION!\n");
            printf("Integral = %.15e\n", coll_integral);
            printf("Time = %.6f\n", (t_end - t_start)/ntrials);
    }

    MPI_Finalize();
    return 0;
}
