include $(AD_ROOT)/Makefile.common
ROOT=example-

NUMBERS := 0 1 2 4
TUTORIALS := $(addprefix $(ROOT),${NUMBERS})
.PHONY: all 

	
DO_LINK=g++ -o $@ $< $(LDFLAGS) 
	
.PHONY: all clean

all: $(TUTORIALS)

${TUTORIALS}: $(ROOT)%: $(ROOT)%.o 
	$(DO_LINK)
	
	
clean:
	rm $(TUTORIALS) *.o