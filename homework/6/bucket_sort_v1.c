#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
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

    double *input_array;   // the input array
    double *bucketlist;    //this array will contain input elements in order of the processors
                            //e.g elements of process 0 will be stored first, then elements of process 1, and so on
    double *local_array;    //This array will contain the elements in each process
    int local_count;

    int n, p, i, my_rank;

    int *scounts;           //This array will contain the counts of elements each processor will receive
    int *dspls;             //The relative offsets in bucketlist array where the elements of different processes
                            //will be stored
    int *bin_elements;       //it will keep track of how many elements have been included in the pth bin

    double t_total;
    double t_generate;
    double t_binning;
    double t_distribute;
    double t_local_sort;
    double t_gathering;

    MPI_Init(NULL, NULL);
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &p);

    scounts = malloc(p*sizeof(int));

    if ( my_rank == 0 )
    {
        t_total = MPI_Wtime();
        t_generate = MPI_Wtime();
        if ( argc > 1 )
            n = atoi(argv[1]);
        else
            n = 100000000;
        input_array = malloc(n*sizeof(double));

        bucketlist = malloc(n*sizeof(double));
        dspls = malloc(p*sizeof(int));
        bin_elements = malloc(p*sizeof(int));

        for ( i = 0; i < p; i++ )
            scounts[i] = 0 ;

        for ( i = 0; i < n; i++ )
        {
            input_array[i] = ((double) rand()/( RAND_MAX + 1.));
            scounts[(int)(input_array[i]/(1.0/p))]++;
        }

        t_binning = MPI_Wtime();
        t_generate = t_binning - t_generate;

        for ( i = 0; i < p; i++ )
            bin_elements[i] = scounts[i];

        dspls[0] = 0;
        for ( i = 0; i < p-1; i++ )
            dspls[i+1] = dspls[i] + scounts[i];

        int bin, pos;
        for ( i = 0; i < n; i++ )
        {
            bin = (int)(input_array[i]/(1.0/p));
            pos = dspls[bin] + scounts[bin] - bin_elements[bin];
            bucketlist[pos] = input_array[i];
            bin_elements[bin]--;
        }
        t_binning = MPI_Wtime() - t_binning;

        // The input array is not needed anymore so let's free it to save
        // memory. The output will be the bucketlist array.
        free(input_array);

        /*MPI_Request req;*/
        /*for ( i = 1; i < p; i++ )*/
        /*{*/
            /*MPI_Isend(&bucketlist[dspls[i]], scounts[i], MPI_DOUBLE, i,*/
                    /*ARRAY_TAG, MPI_COMM_WORLD, &req);*/
            /*MPI_Request_free(&req);*/
        /*}*/

        // no need to reallocate memory for the root process, we'll just use the
        // bucketlist array in-place to save some memory
        local_array = bucketlist;
    }

    /*if ( my_rank > 0 )*/
    /*{*/
        /*MPI_Status status;*/
        /*MPI_Probe(0, ARRAY_TAG, MPI_COMM_WORLD, &status);*/
        /*MPI_Get_elements(&status, MPI_DOUBLE, &local_count);*/
        /*local_array = malloc(local_count*sizeof(double));*/
        /*MPI_Recv(local_array, local_count, MPI_DOUBLE, 0, ARRAY_TAG, MPI_COMM_WORLD, &status);*/
    /*}*/

    // broadcast the bin sizes to prepare local arrays for the scattering
    // operation
    if ( my_rank == 0 )
        t_distribute = MPI_Wtime();
    MPI_Bcast(scounts, p, MPI_INT, 0, MPI_COMM_WORLD);
    local_count = scounts[my_rank];

    // no need to reallocate memory for the root process, we'll just use the
    // bucketlist array in-place to save some memory
    if ( my_rank > 0 )
        local_array = malloc(local_count*sizeof(double));
    MPI_Scatterv(bucketlist, scounts, dspls, MPI_DOUBLE, local_array,
            local_count, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    if ( my_rank == 0 )
        t_distribute = MPI_Wtime() - t_distribute;

    // do the local sorting
    t_local_sort = MPI_Wtime();
    qsort_dbls(local_array, local_count);
    t_local_sort = MPI_Wtime() - t_local_sort;

    // combine the results
    if ( my_rank == 0 )
        t_gathering = MPI_Wtime();
    MPI_Gatherv(local_array, local_count, MPI_DOUBLE, bucketlist,
            scounts, dspls, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    if ( my_rank == 0 )
        t_gathering = MPI_Wtime() - t_gathering;

    double *t_local_sort_array;
    if ( my_rank == 0 )
    {
        t_total = MPI_Wtime() - t_total;
        t_local_sort_array = malloc(p*sizeof(double));
    }
    MPI_Gather(&t_local_sort, 1, MPI_DOUBLE, t_local_sort_array, 1, MPI_DOUBLE,
            0, MPI_COMM_WORLD);
    MPI_Finalize();

    // Check result
    if ( my_rank == 0 )
    {
        /*{*/
            /*printf("Output is: [");*/
            /*for ( i = 0; i < n - 1; i++ )*/
                /*printf("%f, ", bucketlist[i]);*/
            /*printf("%f]\n", bucketlist[n-1]);*/
        /*}*/

        // Only print someting here if the output is incorrect, I don't want
        // spam in my output files
        for ( i = 0; i < n - 1; i++ )
            if ( bucketlist[i] > bucketlist[i+1] )
            {
                printf("OUTPUT IS INCORRECT!\n");
                return 1;
            }

        double local_sort_min, local_sort_avg, local_sort_max;
        get_min_avg_max(t_local_sort_array, p, &local_sort_min,
                &local_sort_avg, &local_sort_max);

        printf("Time Report:\n");
        printf("============\n");
        printf("Total:      %.6f\n", t_total);
        printf("Generate:   %.6f\n", t_generate);
        printf("Binning:    %.6f\n", t_binning);
        printf("Distribute: %.6f\n", t_distribute);
        printf("Local Sort:\n");
        printf("       Min: %.6f\n", local_sort_min);
        printf("       Avg: %.6f\n", local_sort_avg);
        printf("       Max: %.6f\n", local_sort_max);
        printf("Gathering:  %.6f\n", t_gathering);
    }
    return 0;
}
