#include "optMultiplication.h"

void optMultiplication(double* output, double* input_matrix,
        double* input_vector, int N, int M, int B)
{
    int i, j, k, i_block, j_block;

    // Block matrix multiplication
    for ( i_block = 0; i_block < N; i_block += B )
        for ( j_block = 0; j_block < M; j_block += B )
            for ( i = i_block; i < MIN(i_block + B, N); i++ )
                for ( j = j_block; j < MIN(j_block + B, M); j++ )
                    for ( k = 0; k < 16; ++k )
                        output[i*16+k] += input_matrix[i*M+j]*input_vector[j*16+k];
}
