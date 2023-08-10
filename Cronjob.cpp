#include "Cronjob.hpp"
#include <iostream>

// Cronjob::Cronjob() {
// 	m_lastCompleted = 0;
// 	m_type = CRONJOB_SECONDLY;
// 	m_func = nullptr;
// 	m_hour = 0;
// 	m_minute = 0;
// 	m_second = 0;
// }

// Cronjob::Cronjob(const Cronjob& cj) {
// 	m_lastCompleted = cj.m_lastCompleted;
// 	m_type = cj.m_type;
// 	m_func = cj.m_func;
// 	m_hour = cj.m_hour;
// 	m_minute = cj.m_minute;
// 	m_second = cj.m_second;
// }

Cronjob::Cronjob(CronjobType type, cronjobfunc func, int hour = 0, int minute = 0, int second = 0) {
	m_lastCompleted = 0;
	m_type = type;
	m_func = func;
	m_hour = hour;
	m_minute = minute;
	m_second = second;
}

Cronjob::~Cronjob() {

}

bool Cronjob::execute(const std::time_t& time) {
	std::tm* localTime = std::localtime(&time);
	int remainder = 0;
	int modt = 0;
	switch (m_type) {
		case CRONJOB_SECONDLY:
			break;
		case CRONJOB_MINUTELY:
			remainder = localTime->tm_sec;
			modt = m_second;
			if ((time - m_lastCompleted) <= 30) return false;
			if (remainder == modt || remainder == ((modt + 1) % 60))
				break;
			return false;
		case CRONJOB_HOURLY:
			remainder = localTime->tm_min * 60 + localTime->tm_sec;
			modt = m_minute * 60 + m_second;
			if ((time - m_lastCompleted) <= 1800) return false;
			if (remainder == modt || remainder == ((modt + 1) % 3600))
				break;
			return false;
		case CRONJOB_DAILY:
			remainder = localTime->tm_hour * 3600 + localTime->tm_min * 60 + localTime->tm_sec;
			modt = m_hour * 3600 + m_minute * 60 + m_second;
			if ((time - m_lastCompleted) <= 43200) return false;
			if (remainder == modt || remainder == ((modt + 1) % 86400))
				break;
			return false;
	}
	m_func(localTime);
	m_lastCompleted = time;
	return true;
}