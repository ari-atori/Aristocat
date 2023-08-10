#include "slashcommands.hpp"

void command_ping(dpp::cluster* bot, const dpp::slashcommand_t& event) {
	event.reply("Pong!");
}

