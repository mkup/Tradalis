# Table=Transactions
Create table IF NOT EXISTS Transaction (
	id int auto_increment Primary Key,
	dt datetime not null,
	vendorId varchar(15),
	description varchar(100),
	quantity int not null,
	symbol varchar(10) not null,
	price numeric(15,2) default 0.0,
	commission numeric(7,2) default 0.0,
	net_cash numeric(15,2),
	instrument ENUM('stock', 'call', 'put')	default null,
	expiration date default null,
	strike numeric(7.2) default 0.0,
	trade int default 0,
	acct    varchar(10) not null
	)
;

# Table Trade
Create Table IF NOT EXISTS Trade (
	id int auto_increment Primary Key,
	acct varchar(10) default NULL,        # account nick (for now)
	description varchar(50),
	symbol varchar(10) not null,
	long_short ENUM('LONG', 'SHORT'),
	open_closed ENUM('OPEN', 'CLOSED', 'PLAN') NOT NULL default 'OPEN',
	dt_open date default NULL,		        # calculated by the application
	dt_close date default NULL,		        # calculated by the application
	risk numeric(15,2) default 0.00,		# calculated by the application
	net numeric(15,2) default 0.00          # calculated by the application
	spread varchar(10),
	strategy varchar(10),
	outcome varchar(10) default NULL,
	verdict varchar(200) default NULL,
	)
;

# Table Strategy
Create Table IF NOT EXISTS Strategy (
	cde varchar(10) not null,
	description varchar(50)
	)
;

# Table Outcome
Create Table IF NOT EXISTS Outcome (
	cde varchar(10) not null,
	description varchar(50)
	)
;
