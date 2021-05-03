#define PY_SSIZE_T_CLEAN  /* For all # variants of unit formats (s#, y#, etc.) use Py_ssize_t rather than int. */
#include <Python.h>       /* MUST include <Python.h>, this implies inclusion of the following standard headers:
                             <stdio.h>, <string.h>, <errno.h>, <limits.h>, <assert.h> and <stdlib.h> (if available). */
#include <math.h>         /* include <Python.h> has to be before any standard headers are included */



static int array_equal(int d,int K,double *x,double *y);
static void copy_Arrays(int d,int K,double *x,double *y);
static double Min_check(int d ,int rX,int rY,double *x,double *y);
static void zero_double_Array(int N,int d,double *x);
static void update_centroid(int d,int N,int *clusters_sit,int *clusters,double *centroids,int K,double *observations);


static int* kmeans_c(int K,int N,int d,int MAX_ITER,PyObject *_centroids,PyObject *_observations){


    double observation_min,m;
    double *centroids;
    double *centroids_prev;
    double *observations;
    int *clusters;
    int *clusters_sit;
    int i = 0, j = 0, x = 0, c = 0, count_iter = 0,nearest_c = 0;
    Py_ssize_t q;
    PyObject *item;


    clusters_sit=(int *) calloc (K,sizeof(int));
    if(clusters_sit == NULL){
        puts("Memory Allocation has failed!");
        return NULL;
    }
    clusters= (int *) malloc (N*K*sizeof(int));
     if(clusters == NULL){
        puts("Memory Allocation has failed!");
        return NULL;
    }
    centroids_prev=(double *) calloc (d*K,sizeof(double));
     if(centroids_prev == NULL){
        puts("Memory Allocation has failed!");
        return NULL;
    }
    observations = (double *) malloc (d*N*sizeof(double));
    if(observations == NULL){
        puts("Memory Allocation has failed!");
        return NULL;
    }
    centroids = (double *) malloc (d*K*sizeof(double));
    if(centroids == NULL){
        puts("Memory Allocation has failed!");
        return NULL;
    }




// initializing observations //
    for (q = 0; q < d*N; q++) {
        item = PyList_GetItem(_observations, q);
        if (PyFloat_Check(item))
            observations[q] = PyFloat_AsDouble(item);
        else{
            puts("not a double");
            continue;
        }
         }

// initializing centroids //
    for (q = 0; q < K*d; q++) {
        item = PyList_GetItem(_centroids, q);
        if (PyFloat_Check(item))
            centroids[q] = PyFloat_AsDouble(item);
        else{
            puts("not a double");
            continue;
        }
         }

    while (array_equal(d,K,centroids_prev,centroids)==0 && (count_iter <= MAX_ITER)) {
        for(i=0;i<K;i++){
            clusters_sit[i]=0;
        }

        copy_Arrays(d, K, centroids_prev, centroids);

        for (x=0; x < N; x++) {

            observation_min=-1;
            for (c = 0; c < K; c++) {

                m = Min_check(d, x, c, observations, centroids);

                if ((m < observation_min )||(observation_min==-1)) {
                    nearest_c = c;
                    observation_min = m;
                }
            }
            clusters[nearest_c*N+clusters_sit[nearest_c]] = x;
            clusters_sit[nearest_c]=clusters_sit[nearest_c]+1;
        }

        update_centroid(d,N,clusters_sit,clusters,centroids,K,observations);
        count_iter = count_iter + 1;

    }

    for(i=0;i<K;i++){
        for(j=0;j<N;j++){
            if(j>=clusters_sit[i])
                clusters[i*N + j] = 0;
        }
    }
    free(observations);
    free(centroids);
    free(clusters_sit);
    free(centroids_prev);
    return clusters;

}

static PyObject* kmeans_capi(PyObject *self, PyObject *args)
{
    int  k;
    int n;
    int d;
    int MAX_ITER;
    size_t i;
    PyObject *_centroids, *_observations;
    if(!PyArg_ParseTuple(args, "iiiiOO:print_int_lists", &k, &n, &d, &MAX_ITER,&_centroids,&_observations)) {
        puts("Failed parsing k,n or d");
        PyErr_SetString(PyExc_TypeError, "Failed parsing k,n or d");
        return NULL;
}
    if (!PyList_Check(_centroids)){
        puts("Failed parsing centroids");
        PyErr_SetString(PyExc_TypeError, "Failed parsing centroids");
        return NULL;
        }
    if (!PyList_Check(_observations)){
        puts("Failed parsing observations");
        PyErr_SetString(PyExc_TypeError, "Failed parsing observations");
        return NULL;
        }

    int* x = kmeans_c(k,n,d,MAX_ITER,_centroids,_observations);
    if(x == NULL){
        PyErr_SetString(PyExc_AssertionError, "Failed clustering");
        return NULL;
    }
    PyObject *l = PyList_New(n*k);
    for (i = 0; (int)i != n*k; ++i) {
        PyList_SET_ITEM(l, i, PyLong_FromLong(x[i]));
    }
    free(x);
    return l;

    }


static PyMethodDef capiMethods[] = {
    {"k_means",                   /* the Python method name that will be used */
      (PyCFunction) kmeans_capi, /* the C-function that implements the Python function and returns static PyObject*  */
      METH_VARARGS,           /* flags indicating parametersaccepted for this function */
      PyDoc_STR("compute k-means algorithm")}, /*  The docstring for the function */
    {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    capiMethods /* the PyMethodDef array from before containing the methods of the extension */
};


/*
 * The PyModuleDef structure, in turn, must be passed to the interpreter in the module’s initialization function.
 * The initialization function must be named PyInit_name(), where name is the name of the module and should match
 * what we wrote in struct PyModuleDef.
 * This should be the only non-static item defined in the module file
 */
PyMODINIT_FUNC
PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}





static void copy_Arrays(int d,int K,double *x,double *y) {
    int i,j;
    for (i = 0; i < K; i++) {
        for (j = 0; j < d; j++) {
            x[j+i*d] = y[j+i*d];
        }

    }
}
static int array_equal(int d,int K,double *x,double *y){
    int i,j;
    for(i=0;i<K;i++){
        for(j=0;j<d;j++){
            if(x[j+i*d]!=y[j+i*d]) {
                return 0;
            }
        }

    }
    return 1;
}

static double Min_check(int d ,int rX,int rY,double *x,double *y){
    double sum = 0;
    int i=0;
    for(i=0;i<d;i++){
        sum =sum + (x[rX*d+i]-y[rY*d+i])*(x[rX*d+i]-y[rY*d+i]);
    }

    return sum;
}
static void update_centroid(int d,int N,int *clusters_sit,int *clusters,double *centroids,int K,double *observations) {
    int i,c,j,l;
    zero_double_Array(K,d,centroids);
    for (c = 0 ;c< K; c++) {
        for (i = 0; i < d; i++) {
            for (l = 0; l < clusters_sit[c]; l++) {
                centroids[c * d + i] = centroids[c * d + i] + observations[clusters[c * N + l] * d + i];
            }
        }

        for (j = 0; j < d; j++) {
            centroids[c * d + j] = centroids[c * d + j] / clusters_sit[c];
        }

    }
}



static void zero_double_Array(int N,int d,double *x){
    int i,j;
    for(i=0;i<N;i++){
        for(j=0;j<d;j++){
            x[j+i*d]=0;
        }
    }
}






