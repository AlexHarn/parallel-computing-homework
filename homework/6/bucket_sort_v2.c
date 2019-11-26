#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>
#include <float.h>

#define ARRAY_TAG 1


// Comparison function used by qsort
int compare_dbls(const void* arg1, const void* arg2)
{
    double a1 = *(double *) arg1;
    double a2 = *(double *) arg2;
    if (a1 < a2) return -1;
    else if (a1 == a2) return 0;
    else return 1;
}

// Sort the array in place
void qsort_dbls(double *array, int array_len)
{
    qsort(array, (size_t)array_len, sizeof(double),
          compare_dbls);
}

// Get the maximum, minimum and average value in a array of floats
void get_min_avg_max(double *array, int n, double *min, double *avg, double *max)
{
    *max = 0.; *min = DBL_MAX; *avg = 0.;
    for (int i = 0; i < n; i++)
    {
        if ( array[i] > *max )
            *max = array[i];
        if ( array[i] < *min )
            *min = array[i];
        *avg += array[i];
    }
    *avg /= n;
}

int main(int argc, char* argv[])
{

    double *result;         // This array will contain the result gathered at the root process
    double *bucketlist;     //this array will contain input elements in order of the processors
                            //e.g elements of process 0 will be stored first, then elements of process 1, and so on
    double *local_array;    //This array will contain the elements in each process

    int n, p, i, my_rank;

    int *scounts;           //This array will contain the counts of elements each processor will receive
    int *dspls;             //The relative offsets in bucketlist array where the elements of different processes
                            //will be stored
    int *bin_elements;      //it will keep track of how many elements have been included in the pth bin

    double t_total;
    double t_generate;
    double t_binning;
    double t_distribute;
    double t_local_sort;
    double t_gathering;


    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &p);

    scounts = malloc(p*sizeof(int));

    t_generate = MPI_Wtime();
    if ( my_rank == 0 )
        t_total = t_generate;

    if ( argc > 1 )
        n = atoi(argv[1]);
    else
        n = 100000000;

    const int LOCAL_N = ceil(( (float) n )/p);
    const int CHUNK_SZ = ceil(1./p);

    n = p*LOCAL_N;
    bucketlist = malloc(n*sizeof(double));
    dspls = malloc(p*sizeof(int));
    bin_elements = malloc(p*sizeof(int));
    scounts = malloc(p*sizeof(int));
    local_array = malloc(LOCAL_N*sizeof(double));

    for ( i = 0; i < p; i++ )
        scounts[i] = 0;

    for ( i = 0 ; i < LOCAL_N ; i++ )
    {
        local_array[i] = ((double) rand()/( RAND_MAX + 1.));
        scounts[(int)(local_array[i]/(1.0/p))]++;
    }

    t_binning = MPI_Wtime();
    t_generate = t_binning - t_generate;

    for ( i = 0 ; i<p ; i++ )
        bin_elements[i] = scounts[i];

    dspls[0] = 0;
    for ( i = 0; i< p-1; i++ )
        dspls[i+1] = dspls[i] + scounts[i];

    int bin, pos;
    for ( i = 0; i < LOCAL_N; i++ )
    {
        bin = (int)(local_array[i]/(1.0/p));
        pos = dspls[bin] + scounts[bin] - bin_elements[bin];
        bucketlist[pos] = local_array[i];
        bin_elements[bin]--;
    }

    t_distribute = MPI_Wtime();
    t_binning = t_distribute - t_binning;

    free(local_array);

    int *rcounts, *rdspls;
    rcounts = malloc(p*sizeof(int));
    rdspls = malloc(p*sizeof(int));

    MPI_Alltoall(scounts, 1, MPI_INT, rcounts, 1, MPI_INT, MPI_COMM_WORLD);
    rdspls[0] = 0;
    for ( i = 1; i < p; i++ )
        rdspls[i] = rdspls[i - 1] + rcounts[i - 1];
    const int local_count = rdspls[p - 1] + rcounts[p -1];
    /*printf("\nHello from %d, my local count is %d!\n\n", my_rank, local_count);*/
    local_array = malloc(local_count*sizeof(double));
    MPI_Alltoallv(bucketlist, scounts, dspls, MPI_DOUBLE, local_array, rcounts,
            rdspls, MPI_DOUBLE, MPI_COMM_WORLD);

    t_local_sort = MPI_Wtime();
    t_distribute = t_local_sort - t_distribute;
    // do the local sorting
    qsort_dbls(local_array, local_count);

    t_gathering = MPI_Wtime();
    t_local_sort = t_gathering - t_local_sort;

    // combine the results
    MPI_Gather(&local_count, 1, MPI_INT, rcounts, 1, MPI_INT, 0,
            MPI_COMM_WORLD);

    if ( my_rank == 0 )
    {
        for ( i = 1; i < p; i++ )
            rdspls[i] = rdspls[i - 1] + rcounts[i - 1];
        result = malloc(n*sizeof(double));
    }
    MPI_Gatherv(local_array, local_count, MPI_DOUBLE, result,
            rcounts, rdspls, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    t_gathering = MPI_Wtime() - t_gathering;

    double *t_generate_array;
    double *t_binning_array;
    double *t_distribute_array;
    double *t_local_sort_array;
    double *t_gathering_array;

    if ( my_rank == 0 )
    {
        t_total = MPI_Wtime() - t_total;
        t_generate_array = malloc(p*sizeof(double));
        t_binning_array = malloc(p*sizeof(double));
        t_distribute_array = malloc(p*sizeof(double));
        t_local_sort_array = malloc(p*sizeof(double));
        t_gathering_array = malloc(p*sizeof(double));
    }

    MPI_Gather(&t_generate, 1, MPI_DOUBLE, t_generate_array, 1, MPI_DOUBLE,
            0, MPI_COMM_WORLD);
    MPI_Gather(&t_binning, 1, MPI_DOUBLE, t_binning_array, 1, MPI_DOUBLE,
            0, MPI_COMM_WORLD);
    MPI_Gather(&t_distribute, 1, MPI_DOUBLE, t_distribute_array, 1, MPI_DOUBLE,
            0, MPI_COMM_WORLD);
    MPI_Gather(&t_local_sort, 1, MPI_DOUBLE, t_local_sort_array, 1, MPI_DOUBLE,
            0, MPI_COMM_WORLD);
    MPI_Gather(&t_gathering, 1, MPI_DOUBLE, t_gathering_array, 1, MPI_DOUBLE,
            0, MPI_COMM_WORLD);

    MPI_Finalize();

    // Check result
    if ( my_rank == 0 )
    {
        /*printf("Result is: [");*/
        /*for ( i = 0; i < n - 1; i++ )*/
            /*printf("%f, ", result[i]);*/
        /*printf("%f]\n", result[n-1]);*/
        /*printf("Local is: [");*/
        /*for ( i = 0; i < local_count - 1; i++ )*/
            /*printf("%f, ", local_array[i]);*/
        /*printf("%f]\n", local_array[n-1]);*/

        // Only print someting here if the output is incorrect, I don't want
        // spam in my output files
        for ( i = 0; i < n - 1; i++ )
            if ( result[i] > result[i+1] )
            {
                printf("OUTPUT IS INCORRECT!\n");
                return 1;
            }

        double generate_min, generate_avg, generate_max;
        double binning_min, binning_avg, binning_max;
        double distribute_min, distribute_avg, distribute_max;
        double local_sort_min, local_sort_avg, local_sort_max;
        double gather_min, gather_avg, gather_max;

        get_min_avg_max(t_generate_array, p, &generate_min,
                &generate_avg, &generate_max);
        get_min_avg_max(t_binning_array, p, &binning_min,
                &binning_avg, &binning_max);
        get_min_avg_max(t_distribute_array, p, &distribute_min,
                &distribute_avg, &distribute_max);
        get_min_avg_max(t_local_sort_array, p, &local_sort_min,
                &local_sort_avg, &local_sort_max);
        get_min_avg_max(t_gathering_array, p, &gather_min,
                &gather_avg, &gather_max);

        printf("Time Report:\n");
        printf("============\n");
        printf("Total:      %.6f\n", t_total);
        printf("Generate:\n");
        printf("       Min: %.6f\n", generate_min);
        printf("       Avg: %.6f\n", generate_avg);
        printf("       Max: %.6f\n", generate_max);
        printf("Binning:\n");
        printf("       Min: %.6f\n", binning_min);
        printf("       Avg: %.6f\n", binning_avg);
        printf("       Max: %.6f\n", binning_max);
        printf("Distribute:\n");
        printf("       Min: %.6f\n", distribute_min);
        printf("       Avg: %.6f\n", distribute_avg);
        printf("       Max: %.6f\n", distribute_max);
        printf("Local Sort:\n");
        printf("       Min: %.6f\n", local_sort_min);
        printf("       Avg: %.6f\n", local_sort_avg);
        printf("       Max: %.6f\n", local_sort_max);
        printf("Gathering:\n");
        printf("       Min: %.6f\n", gather_min);
        printf("       Avg: %.6f\n", gather_avg);
        printf("       Max: %.6f\n", gather_max);
    }
    return 0;
}

