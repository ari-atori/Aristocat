#include "Discord.hpp"
#include "Database.hpp"
#include "Message.hpp"
#include "commands/slashcommands.hpp"
#include "cronjobs/cronjobs.hpp"
#include <bitset>
#include <chrono>
#include <time.h>

dpp::cluster* Discord::c_bot;
std::vector<Command> Discord::c_commands = std::vector<Command>();
std::map<dpp::snowflake, dpp::members_container> Discord::c_guilds = std::map<dpp::snowflake, dpp::members_container>();
nlohmann::json Discord::c_settings;
nlohmann::json Discord::c_crontimes;
std::map<std::string, Cronjob> Discord::c_cronjobs;
std::thread* Discord::c_thread;
volatile bool Discord::c_alive;

static nlohmann::json loadJSON(std::string filename) {
	nlohmann::json json;
	std::ifstream file(filename);
	file >> json;
	file.close();
	return json;
}

static void saveJSON(std::string filename, nlohmann::json& json) {
	std::ofstream file(filename);
	file << std::setw(1) << std::setfill('\t') << json;
	file.close();
}

void Discord::init() {
#ifdef ARIBOT_BETA
	nlohmann::json json = loadJSON("secrets/config_beta.json");
	c_settings = loadJSON("staging.json");
	c_crontimes = loadJSON("cronjobs_staging.json");
#else
	nlohmann::json json = loadJSON("secrets/config.json");
	c_settings = loadJSON("public.json");
	c_crontimes = loadJSON("cronjobs.json");
#endif

	std::string host = json["db_addr"];
	std::string user = json["db_user"];
	std::string pswd = json["db_pswd"];
	Database::init(host, user, pswd);

	c_bot = new dpp::cluster(json["token"]);

	auto guilds = c_bot->current_user_get_guilds_sync();
	for (auto g : guilds) {
		c_guilds[g.first] = c_bot->guild_get_members_sync(g.first, 1000, 0);
		// TODO: Find more constructive way to merge larger data sets in the case for more users
	}

	c_bot->set_websocket_protocol(dpp::websocket_protocol_t::ws_etf);

	c_bot->on_log(Discord::onLog);

	c_bot->on_slashcommand(Discord::onSlashCommand);

	c_bot->on_ready(Discord::onReady);

	c_bot->on_guild_member_add(Discord::onGuildMemberJoin);
	c_bot->on_guild_member_remove(Discord::onGuildMemberLeave);
}

void Discord::terminate() {
	Database::terminate();
	c_alive = false;
	c_thread->join();
	delete c_thread;
	delete c_bot;
}

void Discord::start() {
	c_bot->start(dpp::st_wait);
}

void Discord::onLog(const dpp::log_t& event) {
#ifdef ARIBOT_BETA
	std::fstream file("logs_beta.txt", std::ios::app);
#else
	std::fstream file("logs.txt", std::ios::app);
#endif
	static std::string types[6] = {"[TRACE] ", "[DEBUG] ", "[INFO] ", "[WARNING] ", "[ERROR] ", "[CRITICAL] "};
	file << types[event.severity] << event.message << std::endl;
}

void Discord::onReady(const dpp::ready_t& event) {
	if (dpp::run_once<struct register_bot_commands>()) {

#ifdef ARIBOT_BETA
		nlohmann::json json = loadJSON("dirty_beta.json");
#else
		nlohmann::json json = loadJSON("dirty.json");
#endif

		std::vector<dpp::command_option> ping_options;
		addCommand("ping", "Ping pong!", command_ping, ping_options, json["ping"]);

		std::vector<dpp::command_option> birthday_options = {
			dpp::command_option(dpp::command_option_type::co_user, "user", "The user whose birthday you want")
		};
		addCommand("birthday", "Get a  birthday", command_birthday, birthday_options, json["birthday"]);

		std::vector<dpp::command_option> setbirthday_options = {
			dpp::command_option(dpp::command_option_type::co_integer, "day", "Day of birthday", true),
			dpp::command_option(dpp::command_option_type::co_integer, "month", "Month of birthday", true),
			dpp::command_option(dpp::command_option_type::co_number, "utc", "Hours ahead or behind of UTC time zone", true)
		};
		addCommand("setbirthday", "Set your birthday", command_setbirthday, setbirthday_options, json["setbirthday"]);

		std::vector<dpp::command_option> basement_options = {
			dpp::command_option(dpp::command_option_type::co_user, "user", "Imminent dweller", true),
			dpp::command_option(dpp::command_option_type::co_boolean, "basement", "True to be sent to, false to be released")
		};
		addCommand("basement", "Cast someone to the basement", command_basement, basement_options, json["basement"]);

		json["ping"] = false;
		json["birthday"] = false;
		json["setbirthday"] = false;
		json["basement"] = false;

#ifdef ARIBOT_BETA
		saveJSON("dirty_beta.json", json);
#else
		saveJSON("dirty.json", json);
#endif

		c_cronjobs.insert({"birthdays", Cronjob(CRONJOB_DAILY, cronjob_birthday, 8, 00, 0)}); // 12:00 UTC
		c_cronjobs.insert({"pings", Cronjob(CRONJOB_MINUTELY, cronjob_pings, 0, 0, 0)});

		c_alive = true;
		c_thread = new std::thread(Discord::cronJobThread);
	}
}

void Discord::onSlashCommand(const dpp::slashcommand_t& event) {
	for (auto c : c_commands) {
		if (c.comm.name == event.command.get_command_name()) {
			c.func(c_bot, event);
			return;
		}
	}
}

void Discord::onGuildMemberJoin(const dpp::guild_member_add_t& event) {
	c_guilds[event.adding_guild->id].insert({event.added.user_id, event.added});
}

void Discord::onGuildMemberLeave(const dpp::guild_member_remove_t& event) {
	c_guilds[event.removing_guild->id].erase(event.removed->id);
}

dpp::snowflake Discord::getUser(std::string userName) {
	return dpp::snowflake((uint64_t)c_settings["users"][userName]);
}

dpp::snowflake Discord::getRole(std::string roleName) {
	return dpp::snowflake((uint64_t)c_settings["roles"][roleName]);
}

dpp::snowflake Discord::getChannel(std::string channelName) {
	return dpp::snowflake((uint64_t)c_settings["channels"][channelName]); 
}

dpp::snowflake Discord::getGuild() {
	return dpp::snowflake((uint64_t)c_settings["guild"]);
}

dpp::guild_member& Discord::getMember(dpp::snowflake member) {
	dpp::snowflake guild((uint64_t)c_settings["guild"]);
	if (c_guilds.count(guild))
		if (c_guilds[guild].count(member))
			return c_guilds[guild][member];
	std::string exception = "Not able to find guild member of " + std::to_string(guild) + " and with id of " + std::to_string(member);
	throw dpp::logic_exception(exception);
}

void Discord::addCommand(std::string name, std::string description, cmdfunc function, std::vector<dpp::command_option>& options, bool dirty) {
	dpp::slashcommand slash(name, description, c_bot->me.id);
	for (auto o : options)
		slash.add_option(o);
	Command command = {slash, function};
	c_commands.push_back(command);
	if (dirty) {
		auto maps = c_bot->global_commands_get_sync();
		for (auto& m : maps) {
			if (m.second.name == name) {
				c_bot->global_command_delete_sync(m.first);
				break;
			}
		}
		c_bot->global_command_create(slash);
	}
}

void Discord::cronJobThread() {
	auto now = std::chrono::high_resolution_clock::now();
	auto miliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch());
	auto nextsec = now + std::chrono::seconds(1) - std::chrono::milliseconds(miliseconds % std::chrono::seconds(1));
	auto duration = nextsec - now;
	std::this_thread::sleep_for(duration);
	while (c_alive) {
		std::time_t currentTime = std::time(nullptr);
		
		bool anyCompleted = false;
		for (auto& cj : c_cronjobs) {
			if (cj.second.execute(currentTime)) {
				c_crontimes[cj.first] = (uint64_t) time;
				anyCompleted = true;
			}
		}

		if (anyCompleted) {
#ifdef ARIBOT_BETA
	saveJSON("cronjobs_staging.json", c_crontimes);
#else
	saveJSON("cronjobs.json", c_crontimes);
#endif	
		}

		now = std::chrono::high_resolution_clock::now();
		miliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch());
		nextsec = now + std::chrono::seconds(1) - std::chrono::milliseconds(miliseconds % std::chrono::seconds(1));
		duration = nextsec - now;
		std::this_thread::sleep_for(duration);
	}
}