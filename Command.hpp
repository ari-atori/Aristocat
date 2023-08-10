#pragma once

#include <dpp/dpp.h>
#include <vector>

typedef void (*cmdfunc)(dpp::cluster* bot, const dpp::slashcommand_t& event);

struct Command {
	dpp::slashcommand comm;
	cmdfunc func;
};
