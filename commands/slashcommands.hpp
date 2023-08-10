#pragma once

#include <dpp/dpp.h>
#include "../Discord.hpp"

void command_ping(dpp::cluster* bot, const dpp::slashcommand_t& event);

void command_birthday(dpp::cluster* bot, const dpp::slashcommand_t& event);

void command_setbirthday(dpp::cluster* bot, const dpp::slashcommand_t& event);

void command_basement(dpp::cluster* bot, const dpp::slashcommand_t& event);