CREATE TABLE gfl_expc
(
	lv integer not null primary key,
	experience integer not null
);

CREATE TABLE gfl_produce
(
	time integer not null,
	rarity integer not null,
	typename varchar not null,
	name varchar not null
);

CREATE TABLE gfl_pequip
(
	time integer not null,
	rarity integer not null,
	typename varchar not null,
	name varchar not null
);
