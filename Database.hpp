#pragma once

#include <mysql_driver.h>
#include <mysql_connection.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>
#include <mutex>
#include "include/json.hpp"

class Database {
public:
	static void init(std::string addr, std::string user, std::string pswd);
	static void connect();
	static void disconnect();
	static void terminate();

	static sql::PreparedStatement* statement(std::string query);
private:
	static sql::mysql::MySQL_Driver *c_driver;
	static sql::Connection *c_connection;
	static std::mutex c_mutex;
};