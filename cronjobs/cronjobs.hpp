#pragma once

#include <dpp/dpp.h>
#include "../Discord.hpp"

void cronjob_birthday(const std::tm* time);

void cronjob_pings(const std::tm* time);