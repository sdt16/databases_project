create or replace function empty(x varchar) returns bool as $$
BEGIN
	return (x is null OR x = '');
END;
$$ LANGUAGE plpgsql;

create or replace function sell_in_anywhere(book book) returns bool as $$
declare
	can_sell BOOL;
	author_count BIGINT;
	contributor_count BIGINT;
	editor_count BIGINT;
	illustrator_count BIGINT;
	translator_count BIGINT;
	one_person BOOL;
begin
	select count(person_id) into author_count from authors where book_id = book.id;
	select count(person_id) into contributor_count from contributors where book_id = book.id;
	select count(person_id) into editor_count from editors where book_id = book.id;
	select count(person_id) into illustrator_count from illustrators where book_id = book.id;
	select count(person_id) into translator_count from translators where book_id = book.id;

	one_person := false;
	if author_count > 0 OR contributor_count > 0 
		OR editor_count > 0 OR illustrator_count > 0 
		OR translator_count > 0 then
			one_person := true;
	end if;

	can_sell := true;
	if empty(book.title) then
		can_sell := false;
	elsif empty(book.language) then
		can_sell := false;
	elsif book.release_date is null then
		can_sell := false;
	elsif empty(book.description) then
		can_sell := false;
	elsif one_person = false then
		can_sell := false;
	end if;

	return can_sell;
end;
$$ LANGUAGE plpgsql;

create or replace function sell_in_uk(book book) returns bool as $$
declare
	can_sell BOOL;
begin
	can_sell := true;
	if not sell_in_anywhere(book.*) then
		can_sell := false;
	elsif empty(book.bic) then
		can_sell := false;
	end if;
	return can_sell;
end;
$$ LANGUAGE plpgsql;

create or replace function sell_in_us(book book) returns bool as $$
declare
	can_sell BOOL;
begin
	can_sell := true;
	if not sell_in_anywhere(book.*) then
		can_sell := false;
	elsif empty(book.bisac) then
		can_sell := false;
	end if;
	return can_sell;
end;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE VIEW for_sale_status AS 
 SELECT b.id, sell_in_uk(b.*) AS sell_in_uk, sell_in_us(b.*) AS sell_in_us
   FROM book b
  ORDER BY b.id;
