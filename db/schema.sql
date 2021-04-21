CREATE TABLE songs (
	id serial PRIMARY KEY,
	artist_name varchar(300),
	title varchar(300),
	year integer, 
	release varchar(300),
	ingestion_time timestamp DEFAULT NOW()
);

CREATE TABLE movies (
	id serial PRIMARY KEY,
	original_title varchar(300),
	original_language varchar(300),
	budget integer,
	is_adult boolean,
	release_date date,
	original_title_normalized varchar(300)
);

CREATE TABLE apps(
	id serial PRIMARY KEY,
	name varchar(300),
	genre varchar(300),
	rating numeric(4, 2),
	version varchar(300),
	size_bytes bigint,
	is_awesome boolean
);

CREATE TRIGGER awesome 
	BEFORE INSERT ON apps
	FOR EACH ROW
	EXECUTE PROCEDURE check_awesomeness();

CREATE OR REPLACE FUNCTION check_awesomeness()
returns TRIGGER
language plpgsql
AS
$$
BEGIN
	NEW.is_awesome = NEW.rating IS NOT NULL AND NEW.rating >= 5; -- this is the criteria for awesomeness
	return NEW;
END;
$$;