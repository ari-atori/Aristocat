#include "cronjobs.hpp"
#include "../Database.hpp"

void cronjob_birthday(const std::tm* time) {
	std::tm local = *time, next = *time;
	next.tm_mday + 1;
	std::mktime(&next);
	Database::connect();

	sql::PreparedStatement* checker = Database::statement("SELECT * FROM birthdays WHERE (month = ? AND day = ? AND utc < 12) OR (month = ? AND day = ? AND utc >= 12);");
	
	checker->setInt(1, local.tm_mon + 1);
	checker->setInt(2, local.tm_mday);
	checker->setInt(3, next.tm_mon + 1);
	checker->setInt(4, next.tm_mday);

	sql::ResultSet *birthdays = checker->executeQuery();

	std::string bdaymsg = "";
	bool hasbirthdays = false;
	while (birthdays->next()) {
		hasbirthdays = true;
		dpp::snowflake userid = std::stoull(birthdays->getString(1));
		dpp::guild_member member = Discord::getMember(userid);
		bdaymsg += "Happy Birthday " + member.get_mention() + "!!!\n";
	}

	if (hasbirthdays) {
		dpp::message message(Discord::getChannel("general"), bdaymsg);
		message.allowed_mentions.parse_users = true;
		Discord::getBot()->message_create_sync(message);
	}

	delete birthdays;
	delete checker;
	Database::disconnect();
}