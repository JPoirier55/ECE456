
#include <stdio.h>
#include <stddef.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>
#include <byteswap.h>
#include <stdlib.h>


uint16_t ip_checksum2(char* data, int length) {
    // Cast the data pointer to one that can be indexed.

    // Initialise the accumulator.
    uint32_t acc=0x0000;

    // Handle complete 16-bit blocks.
    int i;
    for (i=0;i+1<length;i+=2) {
        uint16_t word;
        memcpy(&word,data+i,2);
        // printf("WORD:   %x  \n", word);
        // printf("ACC:    %x   \n", acc);
        acc+=word;
        // printf("BEFORE word: %x \n", acc);
        if (acc>0xffff) {
            acc-=0xffff;
            // printf("AFTER word: %x \n", acc);
        }
    }

    // Handle any partial block at the end of the data.
    if (length&1) {
        uint16_t word=0;
        memcpy(&word,data+length-1,1);
        acc+=word;
        if (acc>0xffff) {
            acc-=0xffff;
        }
    }

    // Return the checksum in network byte order.
    return ~acc;
}

int main(int argc, char *argv[] )
{
  FILE* fp2 = fopen("tempfile", "w");
  FILE* fp1 = fopen(argv[1], "r");
  FILE* fp = fopen(argv[6], "w");

  // printf("%s %s %s %s\n", argv[0], argv[1], argv[6], argv[4]);

  char *source_ip = argv[2];
  printf("Source IP: %s \n", source_ip);
  char *dest_ip = argv[3];
  printf("Dest. IP: %s \n", dest_ip);


  char *source_port = argv[4];
  printf("Source port: %s \n", source_port);
  char *dest_port = argv[5];
  printf("Dest port: %s \n", dest_port);

  char line[80];

  int i = fscanf(fp1, "%s", line);
  strcat(line, "\n");
  // printf("%x \n", ip_checksum(line, strlen(line)));

  uint16_t file_size = strlen(line)+8;

  printf("File size: %i\n", file_size);

  uint32_t source_ip_int = inet_addr(source_ip);
  uint32_t dest_ip_int = inet_addr(dest_ip);

  source_ip_int = __bswap_constant_32 (source_ip_int);
  dest_ip_int = __bswap_constant_32 (dest_ip_int);


  fwrite(&source_ip_int, 4, 1, fp2);
  fwrite(&dest_ip_int, 4, 1, fp2);

  int protocol = 17;
  fwrite(&protocol, 2, 1, fp2);
  fwrite(&file_size, 2, 1, fp2);

  int sourceport = atoi(source_port);
  int destport = atoi(dest_port);
  int checksum = 0;
  fwrite(&sourceport, 2, 1, fp2);
  fwrite(&destport, 2, 1, fp2);
  fwrite(&file_size, 2, 1, fp2);
  fwrite(&checksum, 2, 1, fp2);
  fwrite(line, strlen(line), 1, fp2);


  fclose(fp2);

  char *file_contents;
  long input_file_size;
  FILE *input_file = fopen("tempfile", "rb");
  fseek(input_file, 0, SEEK_END);
  input_file_size = ftell(input_file);
  rewind(input_file);
  file_contents = malloc((input_file_size + 1) * (sizeof(char)));
  fread(file_contents, sizeof(char), input_file_size, input_file);
  fclose(input_file);
  file_contents[input_file_size] = 0;
  checksum = ip_checksum2(file_contents, input_file_size);
  printf("Checksum:  %x \n", checksum);

  FILE* fp3 = fopen("tempfile", "w");

  // fclose(fp3);

  fwrite(&sourceport, 2, 1, fp3);
  fwrite(&destport, 2, 1, fp3);
  fwrite(&file_size, 2, 1, fp3);
  fwrite(&checksum, 2, 1, fp3);
  fwrite(line, strlen(line), 1, fp3);
  fclose(fp3);

  fclose(fp);
  fclose(fp1);
  return 0;
}
