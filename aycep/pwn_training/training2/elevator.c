#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

// gcc elevator.c -fno-stack-protector -no-pie -o elevator 

// Ignore
void callme() {
  asm volatile ("pop %%rdi\n\t"
      "ret"
      :
      :
      : "rdi");
}

int main(void) {
    char command[100];
    
    // Setup -- ignore this
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    memset(command, 0x0, sizeof(command)); 
    
    printf("Maverick Inc. Inter-Section Elevator\n"); 
    printf("Enter desired floor >> "); 
    
    fgets(command, 1000, stdin); // Oh no! I totally didn't key in an extra zero! -- Maverick Inc. intern
    
    printf("Ding! May your ride be an uplifting experience!\n");
    
    return 0; 
}
