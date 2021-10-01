CREATE TABLE category (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT
);

CREATE TABLE entry (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_id INTEGER,
	title TEXT,
	author TEXT,
	year_of_release TEXT,
	number_of_pages INTEGER,
	last_read_page INTEGER DEFAULT 0,
	last_day_of_reading TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	status TEXT DEFAULT dostępna
);

