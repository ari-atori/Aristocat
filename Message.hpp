#pragma once

#include <dpp/dpp.h>

class Message {
public:
	static void creation(const dpp::message_create_t& message);
	static void deletion(const dpp::message_delete_t& message);
	static void update(const dpp::message_update_t& message);
private:

};

