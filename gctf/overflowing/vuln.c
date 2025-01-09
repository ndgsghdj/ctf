#include <stdio.h>
#include <stdlib.h>

void win() {
    printf("Oh No");
    system("cat flag.txt");
}
void main() {
    char flag[150];
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    printf("Enter the flag: ");
    fgets(flag, 1000, stdin);
}

