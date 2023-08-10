#pragma once

#include <mutex>
#include <dpp/dpp.h>
#include "Command.hpp"
#include "Cronjob.hpp"

class Discord {
public:
	static void init();
	static void terminate();

	static dpp::snowflake getUser(std::string userName);
	static dpp::snowflake getRole(std::string roleName);

	static dpp::cluster* getBot() { return c_bot; }

	static dpp::guild_member& getMember(dpp::snowflake);
	static dpp::snowflake getChannel(std::string);

	static void start();
private:
	static void onReady(const dpp::ready_t& event);
	static void onSlashCommand(const dpp::slashcommand_t& event);
	static void onGuildMemberJoin(const dpp::guild_member_add_t& event);
	static void onGuildMemberLeave(const dpp::guild_member_remove_t& event);
	static void addCommand(std::string name, std::string description, cmdfunc function, std::vector<dpp::command_option>& options, bool dirty);

	static void cronJobThread();

	static std::vector<Command> c_commands;
	static dpp::cluster *c_bot;
	static std::map<dpp::snowflake, dpp::members_container> c_guilds;
	static nlohmann::json c_settings;
	static std::thread* c_thread;
	static volatile bool c_alive;
	static nlohmann::json c_crontimes;
	static std::map<std::string, Cronjob> c_cronjobs;
};
