CC := gcc

CFLAGS := -std=gnu99 -Wall -Wextra -Wpedantic -Wunused-parameter -O3 -fopenmp
SRCDIR := src
CFILES := $(filter-out ./$(SRCDIR)/main.c,$(wildcard ./$(SRCDIR)/*.c))
OFILES := $(CFILES:.c=.o)

LIB := -lm

spmv: $(OFILES)
	    $(CC) -o spmv.x ./$(SRCDIR)/main.c $(OFILES) $(CFLAGS) $(LIB)

$(SRCDIR)/%.o: $(SRCDIR)/%.c
	    $(CC) -c -o $@ $< $(CFLAGS) $(LIB)

clean:
	    -rm  *.x $(OFILES) main.o
