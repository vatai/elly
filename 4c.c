#include <stdio.h>
#include <stdlib.h>
int f2t(int n, int *a, int *b){
  int i;
  int rv=0;
  for(i=0; i<n; i++){
    rv+=a[i]*b[i];
  }
  return rv;
}

int main(){
  int a[20];
  int b[20];
  int i,j,n;
  for(i=0; i<10; i++){
    n=rand()%20+1;
    for(j=0;j<n;j++){
      a[j]=rand()%10;
      b[j]=rand()%10;
    }
    
    int stud = f2(n, a, b);
    int teac = f2t(n, a, b);
    if( stud != teac ){
      printf("a[0]=%d, b[0]=%d\n", a[0], b[0]);
      printf("Hiba: stud=%d, teac=%d\n",stud,teac);
    }else{
      printf("OK\n");
    }
  }
}
