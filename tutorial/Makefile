include $(AD_ROOT)/Makefile.common

TUTORIALS= \
	example-0
	
DO_LINK=g++ -o $@ $< $(LDFLAGS) 
	
.PHONY: all clean

all: $(TUTORIALS)

example-0: example-0.o
	$(DO_LINK)
	
	
clean:
	rm $(TUTORIALS) *.o