create or replace function empty(x varchar) returns bool as $$
BEGIN
	return (x is null OR x = '');
END;
$$ LANGUAGE plpgsql;