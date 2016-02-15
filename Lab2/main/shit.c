unsigned short CalcChecksum(unsigned char *start_addr, int bytecount){
  int i;
  unsigned short chksum;

  chksum = 0;
  printf("Start: %s\n", start_addr);

  for(i=0; i<bytecount; i++){
    chksum += *(start_addr+i);
    printf("%x\n", *(start_addr+i));
    printf("Checksum= %x \n", chksum);
    if(sizeof(chksum) > 4 ){
      printf("Checksum overflow: %x\n",chksum);
    }
  }
  chksum = ~chksum;
  return chksum;
}

unsigned int addcheck (sum, array, length)
unsigned int *sum;
char *array;
int length;
{
	register int i;
	unsigned short *iarray;
	int	 len;

	iarray = (unsigned short *) array;
	len = length / 2;

	for (i=0; i<len; i++)
	    *sum += iarray[i];

	/* wrap the carry back into the low bytes (assumes length < 2**17)
	 */
	while (*sum>>16)
	    *sum = (*sum & 0xFFFF) + (*sum>>16);

	return (*sum);
}


#define LAST 10

uint16_t ip_checksum(void* vdata, size_t length) {
    // Cast the data pointer to one that can be indexed.
    char* data = (char*)vdata;

    // Initialise the accumulator.
    uint32_t acc=0x0000;

    // Handle complete 16-bit blocks.
    size_t i;
    for (i=0;i+1<length;i+=2) {
        uint16_t word;
        printf("DATA:   %s ", data+i);
        memcpy(&word,data+i,2);
        printf("--%x  \n", word);
        acc+=ntohs(word);
        printf("BEFORE word: %x \n", acc);
        if (acc>0xffff) {
            acc-=0xffff;
            printf("AFTER word: %x \n", acc);
        }
    }

    // Handle any partial block at the end of the data.
    if (length&1) {
        uint16_t word=0;
        memcpy(&word,data+length-1,1);
        acc+=ntohs(word);
        if (acc>0xffff) {
            acc-=0xffff;
        }
    }

    // Return the checksum in network byte order.
    return ~acc;
}
