#include "slashcommands.hpp"

void command_basement(dpp::cluster* bot, const dpp::slashcommand_t& event) {
	
	try {
		dpp::command_interaction interaction = event.command.get_command_interaction();
		bool imprison = (interaction.options.size() == 1) || (interaction.get_value<bool>(1));

		dpp::snowflake guildSnowflake  = event.command.get_guild().id;
		dpp::snowflake issuerSnowflake = event.command.get_issuing_user().id;
		dpp::snowflake targetSnowflake = interaction.get_value<dpp::snowflake>(0);

		dpp::guild_member issuer = Discord::getMember(event.command.get_issuing_user().id);
		dpp::guild_member user   = Discord::getMember(interaction.get_value<dpp::snowflake>(0));

		if (issuer.user_id == user.user_id) {
			event.reply("While one may be a prisoner inside their own mind, one may not imprison themself here");
			return;
		}

		dpp::snowflake snowflakeAriAtori  = Discord::getUser("Ari Atori");
		dpp::snowflake snowflakeAristocat = Discord::getUser("Aristocat");

		bool issuedByAri = (issuer.user_id == Discord::getUser("Ari Atori"));

		if (!issuedByAri) {
			for (auto r : issuer.roles) {
				if (r == Discord::getRole("dweller")) {
					event.reply("Basement dwellers may not compel others to join them in their lifestyles");
					return;
				}
			}
		}

		bool hasDwellerRole = false;

		dpp::snowflake roleDweller = Discord::getRole("dweller");
		
		dpp::snowflake roleMod = Discord::getRole("Moderator");

		if (user.user_id == snowflakeAriAtori) {
			event.reply("Ari Atori is already a dweller, there exists no need");
			return;
		}
		if (user.user_id == snowflakeAristocat) {
			event.reply("One may not be the judge of their own case");
			return;
		}



		for (auto r : user.roles) {
			if (r == roleMod && !issuedByAri) { // Moderator, but not issued by Ari Atori
				event.reply("Only Ari Atori may send a moderator to the basement");
				return;
			}
			if (r == roleDweller && imprison) {
				event.reply("The dweller's neckbeard cannot grow any faster than it already is");
				return;
			}
			if (r == roleDweller && !imprison) {
				hasDwellerRole = true;
			}
		}

		if (!hasDwellerRole && !imprison) {
			event.reply("You cannot free someone who is already not imprisoned");
			return;
		}

		if (imprison) {
			bot->guild_member_add_role_sync(guildSnowflake, user.user_id, roleDweller);
		} else {
			auto confirm = bot->guild_member_delete_role_sync(guildSnowflake, user.user_id, roleDweller);
			std::cout << "Confirm: " << confirm.success << std::endl;
		}

		Discord::getMember(targetSnowflake) = bot->guild_get_member_sync(guildSnowflake, targetSnowflake);
		std::string ending = (imprison) ? "neckbeard" : "normal human being";

		event.reply("They are now living the life of a " + ending);
	} catch (dpp::logic_exception ex) {
		std::cout << ex.what() << std::endl;
		event.reply("This user does not seem to exist here");
		return;
	}
}