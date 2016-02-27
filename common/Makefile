include $(AD_ROOT)/Makefile.common

.PHONY: all clean

COMMON_SRC = \
	basics.cpp
	
COMMON_OBJ = $(COMMON_SRC:%.cpp=%.o)
	


all: commonLib.a
	
	
commonLib.a: $(COMMON_OBJ)
	$(AR) cr $@ $(COMMON_OBJ)
	
clean:
	rm -rf commonLib.a $(COMMON_OBJ)
	