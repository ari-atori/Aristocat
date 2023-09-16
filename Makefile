C_FLAGS = -std=c++17
L_FLAGS = -ldpp -lmysqlcppconn

ifeq ($(version),beta)
	C_FLAGS += -g -DARIBOT_BETA
	OUT =aribot_beta
else
	OUT = aribot
endif

all: cleantop root commands cronjobs build

wipe:
	rm -f *.o
	rm -rf tmp/

setup:
	mkdir -p tmp/
	mkdir -p tmp/commands
	mkdir -p tmp/cronjobs

root: *.cpp
	g++ *.cpp  -c $(C_FLAGS) > error.txt 2>&1
	mv *.o tmp/

commands: commands/*.cpp
	g++ commands/*.cpp -c $(C_FLAGS) > error.txt 2>&1
	mv *.o tmp/commands

cronjobs: cronjobs/*.cpp
	g++ cronjobs/*.cpp -c $(C_FLAGS) > error.txt 2>&1
	mv *.o tmp/cronjobs

build:
	g++ tmp/*.o tmp/commands/*.o tmp/cronjobs/*.o -o $(OUT) $(C_FLAGS) $(L_FLAGS) > error.txt 2>&1

cleantop:
	rm -f *.o

clean:
	rm -f *.o
	rm -f tmp/*.o tmp/commands/*.o tmp/cronjobs/*.o