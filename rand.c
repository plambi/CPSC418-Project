#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // Seed the random number generator with the current time
    srand(time(NULL));

    // Open the file for writing
    FILE *file = fopen("random_bit_string.txt", "w");
    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }

    // Generate 1 million bits
    for (int i = 0; i < 1000000; i++) {
        // Get a random number and extract the least significant bit
        int bit = rand() & 1;  // rand() returns a number, & 1 gives the least significant bit

        // Write the bit to the file
        fprintf(file, "%d", bit);
    }

    // Close the file
    fclose(file);

    printf("1 million bits have been written to 'random_bit_string.txt'.\n");
    return 0;
}
