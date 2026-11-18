CC = gcc

CFLAGS = -Wall -Wextra -O2

TARGET = timer_demo

SRC = main.c timer.c

all:
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

run: all
	./$(TARGET)

clean:
	rm -f $(TARGET)