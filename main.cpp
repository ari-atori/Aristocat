#include <dpp/dpp.h>
#include <cstdlib>
#include <fstream>
#include "include/json.hpp"
#include "Discord.hpp"
#include "Database.hpp"
#include "commands/slashcommands.hpp"

int main() {
	Discord::init();

	Discord::start();

	Discord::terminate();

	return 0;
}