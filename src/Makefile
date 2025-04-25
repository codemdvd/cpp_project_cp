CXX      := g++
CXXFLAGS := -std=c++17 -O2 -Wall -Wextra -pedantic
LDLIBS   := -lgecodeint -lgecodesearch -lgecodeminimodel \
            -lgecodekernel -lgecodesupport
TARGET   := dfa
SRC      := dfa_solver.cpp

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $@ $(LDLIBS)

clean:
	rm -f $(TARGET)
