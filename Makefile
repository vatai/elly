AS := yasm
CFLAGS := -std=gnu99
ASFLAGS := -felf64
CC := gcc

3c: 3c.o 3asm.o
	$(CC) $(CFLAGS) $^ -o $@ 

4c: 4c.o 4asm.o
	$(CC) $(CFLAGS) $^ -o $@ 
5c: 5c.o 5asm.o
	$(CC) $(CFLAGS) $^ -o $@ 

clean:
	rm *.o *~
