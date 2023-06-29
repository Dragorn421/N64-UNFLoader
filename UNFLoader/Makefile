APP=UNFLoader
OS_NAME := $(shell uname -s)

CODEFILES_DEVICE = device.cpp \
                   device_64drive.cpp \
                   device_everdrive.cpp \
                   device_sc64.cpp

CODEFILES_CLI = main.cpp helper.cpp term.cpp debug.cpp $(CODEFILES_DEVICE)
CODEFILES_CLI += Include/lodepng.cpp

CODEFILES_SHARED = $(CODEFILES_DEVICE) c_wrappers.cpp

CXX=g++

DEPENDENCIES = -lftd2xx -lpthread
DEPENDENCIES_CLI = $(DEPENDENCIES)
ifeq ($(OS_NAME),Darwin)
	DEPENDENCIES_CLI += -lncurses
else
	DEPENDENCIES_CLI += -lncursesw -lrt
endif

LINKER_OPTIONS := -Wl,-rpath /usr/local/lib
CFLAGS=-D LINUX -D_XOPEN_SOURCE_EXTENDED -Wall -Wno-unknown-pragmas -std=c++11

CFLAGS += -O3
#CFLAGS += -g

ifeq ($(wildcard build/Include),)
 $(shell mkdir build)
 $(shell mkdir build/Include)
endif

default: $(APP)

$(APP): $(addprefix build/,$(CODEFILES_CLI:.cpp=.o))
	@echo "Linking $@"
	@$(CXX) $(CFLAGS) -o $@ $^ $(DEPENDENCIES_CLI) $(LINKER_OPTIONS) -L/usr/local/lib

UNFLoader.so: CFLAGS += -fPIC
UNFLoader.so: LINKER_OPTIONS += -shared
UNFLoader.so: $(addprefix build/,$(CODEFILES_SHARED:.cpp=.o))
	@echo "Linking $@"
	@$(CXX) $(CFLAGS) -o $@ $^ $(DEPENDENCIES) $(LINKER_OPTIONS) -L/usr/local/lib

build/%.o: %.cpp
	@echo "Compiling $<"
	@$(CXX) -c $(CFLAGS) -o $@ $<

clean:
	@echo "Cleaning built artifacts.."
	@rm -rf $(APP) UNFLoader.so build

install: $(APP)
	@echo "Installing $(APP) to /usr/local/bin"
	@mkdir -p /usr/local/bin
	@cp $(APP) /usr/local/bin/$(APP)

uninstall: $(APP)
	@echo "Removing $(APP) from /usr/local/bin"
	@rm -f /usr/local/bin/$(APP)