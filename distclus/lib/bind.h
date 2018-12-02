#ifndef __BIND_H_
#define __BIND_H_

#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef enum {I_RANDOM, I_GIVEN, I_KMEANSPP} initializer;
typedef enum {S_REAL, S_COMPLEX, S_SERIES} space;
typedef enum {O_KMEANS, O_MCMC, O_KNN, O_STREAMING} oc;

#endif
