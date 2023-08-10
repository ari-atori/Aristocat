#include "slashcommands.hpp"
#include "../Database.hpp"

void command_setbirthday(dpp::cluster* bot, const dpp::slashcommand_t& event) {
	dpp::command_interaction interaction = event.command.get_command_interaction();

	std::string userid = std::to_string(event.command.get_issuing_user().id);
	long int day = interaction.get_value<long int>(0); // day
	long int month = interaction.get_value<long int>(1); // month
	double utc = interaction.get_value<double>(2); // utc offset
	
	
	long int days_in_month[12] = {31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

	if (month < 1 || month > 12) {
		event.reply("You do not have a valid birthday entered in");
		return;
	}
	if (day < 1 || day > days_in_month[month - 1]) {
		event.reply("You do not have a valid birthday entered in");
		return;
	}
	if (utc < -12 || utc > 14) {
		event.reply("You do not have a valid UTC offset. It must be between -12 to +14");
		return;
	}

	static std::string months[12] = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
	static std::string endings[10] = {"th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th"};
	
	std::string ending = (11 <= day && day <= 19) ? "th" : endings[day % 10];

	Database::connect();

	sql::PreparedStatement* checker = Database::statement("SELECT user_id FROM birthdays WHERE user_id=?;");
	checker->setString(1, userid);

	sql::ResultSet *existence = checker->executeQuery();

	if (existence->next()) {
		sql::PreparedStatement* statement = Database::statement("UPDATE birthdays SET day=?, month=?, utc=? WHERE user_id=?;");
		statement->setInt(1, day);
		statement->setInt(2, month);
		statement->setDouble(3, utc);
		statement->setString(4, userid);

		statement->executeUpdate();

		delete statement;
	} else {
		sql::PreparedStatement* statement = Database::statement("INSERT INTO birthdays (user_id, day, month, utc) VALUES (?, ?, ?, ?);");
		statement->setString(1, userid);
		statement->setInt(2, day);
		statement->setInt(3, month);
		statement->setDouble(4, utc);

		statement->execute();

		delete statement;
	}

	delete existence;
	delete checker;

	Database::disconnect();

	event.reply("Your birthday is set for " + months[month - 1] + " " + std::to_string(day) + ending);
}