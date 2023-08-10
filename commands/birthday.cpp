#include "slashcommands.hpp"
#include "../Database.hpp"

void command_birthday(dpp::cluster* bot, const dpp::slashcommand_t& event) {
	dpp::command_interaction interaction = event.command.get_command_interaction();

	bool is_you = interaction.options.empty();

	std::string userid = (is_you) ? std::to_string(event.command.get_issuing_user().id) : std::to_string(interaction.get_value<dpp::snowflake>(0));

	static std::string months[12] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
	static std::string endings[10] = {"th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th"};

	Database::connect();

	sql::PreparedStatement* checker = Database::statement("SELECT day, month FROM birthdays WHERE user_id=?;");
	checker->setString(1, userid);

	sql::ResultSet *existence = checker->executeQuery();

	if (existence->next()) {
		int day = existence->getInt(1);
		int month = existence->getInt(2);
		std::string ending = (11 <= day && day <= 19) ? "th" : endings[day % 10];

		std::string start = (is_you) ? "Your " : "Their ";
		event.reply(start + "birthday is " + months[month - 1] + " " + std::to_string(day) + ending);
	} else {
		std::string start = (is_you) ? "Hmm... you " : "Hmm... they ";
		event.reply(start + "don't seem to have a birthday listed here");
	}

	delete existence;
	delete checker;

	Database::disconnect();
}