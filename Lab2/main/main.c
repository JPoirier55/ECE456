    
    #include <stdio.h>
    #define LAST 10
      
    int main()
    {
	 FILE* fp = fopen("test.txt", "w");

	int val = 80;

        fwrite(&val, sizeof(unsigned short), 1, fp);
	
	val = 22;

	fwrite(&val, sizeof(unsigned short), 1, fp);

	val = 14;

	fwrite(&val, sizeof(unsigned short), 1, fp);

	char* str = "12345";

	fwrite(str, sizeof(str), 1, fp);

	fclose(fp);
	return 0;
    }
