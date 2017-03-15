# Table Sources
Create Table IF NOT EXISTS Source (
	cde varchar(5) not null,
	description varchar(25)
	)
;

# Table Spread
Create Table IF NOT EXISTS Spread (
	cde varchar(10) not null,
	description varchar(50)
	)
;

# Table Instrument
Create Table IF NOT EXISTS Instrument (
	cde varchar(10) not null,
	description varchar(50)
	)
;