#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

// gcc floor1_lock.c -o floor1_lock -std=c11 -no-pie -z execstack -fno-stack-protector

int emergency_override() {
	printf("Maverick Inc.\n"); 
	printf("Emergency Door Release\n");
	
	execve("/bin/sh", NULL, NULL); 
	
	return 0;
}

int main(void) {
    char password[0x100];
    
    // Setup -- ignore this 
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
	printf("Welcome to Maverick Inc.\n"); 
	printf("Enter the password to unlock the door: \n");
	
	gets(password); 
	
	printf("ACCESS DENIED\n"); 
	
	return 0; 
}
