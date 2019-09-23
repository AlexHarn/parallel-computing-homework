#include "naiveMultiplication.h"

void naiveMultiplication(double* output, double* input_matrix, double* input_vector,int N,int M){
    
    for ( int i = 0; i < N; ++i ) {
        for ( int j = 0; j < M; ++j ) {
            output[i] += input_matrix[i*M+j]*input_vector[j];
        }
    }
    
}

