
#include <stdio.h>
#include <stddef.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>
#include <byteswap.h>
#include <stdlib.h>


uint16_t ip_checksum2(char* data, int length) {
    // Initialise the accumulator.
    uint32_t acc=0xffff;

    int i;
    for (i=0;i+1<length;i+=2) {
        uint16_t word;
        memcpy(&word,data+i,2);
        acc+=word;
        if (acc>0xffff) {
            acc-=0xffff;
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

int Usage(char* arg0){
	printf("\033[1;37mUsage: \033[0m <inputfile> <senderip> <receiverip>\
  <senderport> <receiverport> <outputfilename>\n");
	return -1;
}

int CreateDatagram(char* line, uint16_t file_size, int sourceport, int destport, char *argv[]){
  // Read the created tempfile and calculate checksum, then
  //write the output datagram file with checksum attached

  char *file_contents;
  long input_file_size;

  FILE* input = fopen(argv[1], "r");

  uint16_t checksum;
  FILE *input_file = fopen("tempfile", "rb");
  fseek(input_file, 0, SEEK_END);
  input_file_size = ftell(input_file);
  rewind(input_file);
  file_contents = malloc((input_file_size + 1) * (sizeof(char)));
  fread(file_contents, sizeof(char), input_file_size, input_file);
  fclose(input);
  file_contents[input_file_size] = 0;
  checksum = ip_checksum2(file_contents, input_file_size);
  printf("Checksum:  %x \n", checksum);

  FILE* fp3 = fopen(argv[6], "w");

  fwrite(&sourceport, 2, 1, fp3);
  fwrite(&destport, 2, 1, fp3);
  fwrite(&file_size, 2, 1, fp3);
  fwrite(&checksum, 2, 1, fp3);
  fwrite(line, strlen(line), 1, fp3);
  fclose(fp3);

  return 0;
}

int CreateTempChecksumFile(char* line, uint16_t file_size, uint32_t source_ip_int, uint32_t dest_ip_int, int sourceport, int destport,char *argv[]){
  // Creates a file which has the pseudo header, udp header and data,
  //for calculating the checksum, as well as allowing a hexdump of what
  //the checksum is working with for debugging

  FILE* tempfile = fopen("tempfile", "w");

  printf("File size: %i\n", file_size);

  fwrite(&source_ip_int, 4, 1, tempfile);
  fwrite(&dest_ip_int, 4, 1, tempfile);

  int protocol = 17;
  fwrite(&protocol, 2, 1, tempfile);
  fwrite(&file_size, 2, 1, tempfile);

  int checksum = 0;
  fwrite(&sourceport, 2, 1, tempfile);
  fwrite(&destport, 2, 1, tempfile);
  fwrite(&file_size, 2, 1, tempfile);

  fwrite(&checksum, 2, 1, tempfile);
  fwrite(line, strlen(line), 1, tempfile);
  fclose(tempfile);

  return 0;
}

int DisplayOutput(char *argv[]){
  printf("Source IP: %s \n", argv[2]);
  printf("Dest. IP: %s \n", argv[3]);
  printf("Source port: %s \n", argv[4]);
  printf("Dest port: %s \n", argv[5]);

  return 0;
}

int main(int argc, char *argv[])
{
  if(argc != 7) return Usage(argv[0]);

  FILE* input = fopen(argv[1], "r");

  char line[80];
  fscanf(input, "%s", line);
  uint16_t file_size = strlen(line)+8;

  uint32_t source_ip_int = inet_addr(argv[2]);
  uint32_t dest_ip_int = inet_addr(argv[3]);
  int sourceport = atoi(argv[4]);
  int destport = atoi(argv[5]);

  DisplayOutput(argv);
  CreateTempChecksumFile(line, file_size, source_ip_int, dest_ip_int, sourceport, destport, argv);
  CreateDatagram(line, file_size, sourceport, destport, argv);

  return 0;
}
