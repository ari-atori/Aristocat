#include "cronjobs.hpp"

void cronjob_pings(const std::tm* time) {
	// Silly ping function running every minute to ensure the bot stays alive
	Discord::getBot()->guild_get_member_sync(Discord::getGuild(), Discord::getUser("Aristocat"));
}