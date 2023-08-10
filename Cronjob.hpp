#pragma once
#include <chrono>

enum CronjobType {
	CRONJOB_SECONDLY,
	CRONJOB_MINUTELY,
	CRONJOB_HOURLY,
	CRONJOB_DAILY
};

typedef void (*cronjobfunc)(const std::tm*);

class Cronjob {
public:
	// Cronjob();
	// Cronjob(const Cronjob& cj);
	Cronjob(CronjobType type, cronjobfunc func,  int hour, int minute, int second);
	virtual ~Cronjob();

	void setLastCompletion(std::time_t time) { m_lastCompleted = time; }

	bool execute(const std::time_t& time);
private:
	std::time_t m_lastCompleted;
	CronjobType m_type;
	int m_hour, m_minute, m_second;
	cronjobfunc m_func;
};