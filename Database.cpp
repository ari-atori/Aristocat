#include "Database.hpp"

sql::mysql::MySQL_Driver *Database::c_driver;
sql::Connection *Database::c_connection;
std::mutex Database::c_mutex;

void Database::init(std::string addr, std::string user, std::string pswd) {
	c_driver = sql::mysql::get_mysql_driver_instance();

	c_connection = c_driver->connect("tcp://" + addr + ":3306", user, pswd);
	if (!c_connection->isValid()) {
		throw std::runtime_error("Database parameters are not correct!");
	}
#ifdef ARIBOT_BETA
	c_connection->setSchema("aristocat_beta");
#else
	c_connection->setSchema("aristocat");
#endif
}

void Database::connect() {
	c_mutex.lock();
	c_connection->reconnect();
#ifdef ARIBOT_BETA
	c_connection->setSchema("aristocat_beta");
#else
	c_connection->setSchema("aristocat");
#endif
}

void Database::disconnect() {
	c_mutex.unlock();
}

void Database::terminate() {
	c_mutex.lock();
	delete c_connection;
	c_mutex.unlock();
}

sql::PreparedStatement* Database::statement(std::string query) {
	return c_connection->prepareStatement(query);
}