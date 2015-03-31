#include <stdio.h>
#include <stdlib.h>
int f1t(int x1, int x2, int x3, int x4, int x5, int x6){
     return 3*x1+4*((x2-x3)*x5+5)*x6-4*x4;
  // return 3*x1+4*((x2-x3)/x5+5)*x6-4*x4;
}

int main(){
  int x1, x2, x3, x4, x5, x6;
  int result;
  int i;
  for(i=0; i<10; i++){
    x1=rand()%1000;
    x2=rand()%1000;
    x3=rand()%1000;
    x4=rand()%1000;
    x5=rand()%1000;
    x6=rand()%1000;
    int stud = f1(x1, x2, x3, x4, x5, x6);
    int teac = f1t(x1, x2, x3, x4, x5, x6);
    if( stud != teac ){
      printf("Hiba: x1=%3d, x2=%3d, x3=%3d, x4=%3d, x5=%3d, x6=%3d, "
	     "stud=%d, teac=%d\n", 
	     x1, x2, x3, x4, x5, x6, stud, teac);
    }else{printf("OK\n");}
  }
}
