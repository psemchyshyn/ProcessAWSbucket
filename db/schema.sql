CREATE TABLE songs (
	id serial PRIMARY KEY,
	artist_name varchar,
	title varchar,
	year integer, 
	release varchar,
	ingestion_time timestamp DEFAULT NOW()
);

CREATE TABLE movies (
	id serial PRIMARY KEY,
	original_title varchar,
	original_language varchar,
	budget bigint,
	is_adult boolean,
	release_date date,
	original_title_normalized varchar
);

CREATE TABLE apps(
	id serial PRIMARY KEY,
	name varchar,
	genre varchar,
	rating numeric(4, 2),
	version varchar,
	size_bytes bigint,
	is_awesome boolean
);


CREATE OR REPLACE FUNCTION check_awesomeness()
RETURNS TRIGGER
LANGUAGE plpgsql
AS
$$
BEGIN
	NEW.is_awesome = NEW.rating IS NOT NULL AND NEW.rating >= 5; -- this is the criteria for awesomeness
	return NEW;
END;
$$;

CREATE TRIGGER awesome 
	BEFORE INSERT ON apps
	FOR EACH ROW
	EXECUTE PROCEDURE check_awesomeness();

CREATE OR REPLACE FUNCTION normalize_title()
RETURNS TRIGGER
LANGUAGE plpgsql
AS
$$
BEGIN 
	NEW.original_title_normalized = REGEXP_REPLACE(REGEXP_REPLACE(LOWER(NEW.original_title), '\s', '_', 'g'), '\W', '', 'g');  -- lowercase, remove non-letters and non-numbers, replace spaces with _
	RETURN NEW;
END;
$$;

CREATE TRIGGER normalization
	BEFORE INSERT ON movies
	FOR EACH ROW
	EXECUTE PROCEDURE normalize_title();
	