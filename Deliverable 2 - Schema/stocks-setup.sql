--DROP DATABASE IF EXISTS stocks;
--CREATE DATABASE stocks;

DROP SCHEMA IF EXISTS testing CASCADE;
CREATE SCHEMA testing;

DROP USER IF EXISTS stocks;
CREATE USER stocks WITH PASSWORD 'stocks';

GRANT ALL PRIVILEGES ON DATABASE stocks TO stocks;
ALTER USER stocks SET search_path = testing;


CREATE TABLE securities(
	Ticker varchar(255),
	Security varchar(255),
	SECFilings varchar(255),
	GICSSector varchar(255),
	GICSSubIndustry varchar(255),
	Address varchar(255),
	DateAdded varchar(255),
	CIK int,
	PRIMARY KEY (Ticker)
);

CREATE TABLE fundamentals(
	symbol varchar(4) REFERENCES securities(Ticker),
	ending_ DATE,
	payable Numeric(12,1),
	receivable Numeric(12, 1),
	add_inc_expense Numeric(12, 1),
	roe Numeric(5, 1),
	capital_expenditure Numeric(12, 1),
	capital_surplus Numeric(12, 1),
	cash_ratio Numeric(4, 1),
	cash_equity Numeric(13, 1),
	inventory_changes Numeric(11, 1),
	common_stock Numeric(13, 1),
	cost_of_revenue Numeric(13, 1),
	current_ratio Numeric(4, 1),
	deferred_asset_charges Numeric(12, 1),
	deferred_liability_charges Numeric(12, 1),
	depreciation Numeric(12, 1),
	earnings_before_interest Numeric(12, 1),
	earnings_before_tax Numeric(12, 1),
	PRIMARY KEY (symbol, ending_)
);
CREATE TABLE prices(
	date_ DATE,
	symbol varchar(4) REFERENCES securities(Ticker),
	open Numeric(9,6),
	close Numeric(9,6),
	low Numeric(9,6),
	high Numeric(9,6),
	volume Numeric(10,1),
	PRIMARY KEY (symbol, date_)
);