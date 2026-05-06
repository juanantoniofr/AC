#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define N 4096*4

unsigned int A[N][N];

int main(){
    register int i,j;
    for (i=0; i<N; i++) {
        for (j=0; j<N; j++) {
            A[i][j]= i*j%(i+j+1);
        }
    }
    return 0;	
}
    
    
