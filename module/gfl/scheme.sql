.separator ","

CREATE TABLE gfl_expc
(
	lv integer not null primary key,
	experience integer not null
);

.import module/gfl/gfl_expc.csv gfl_expc

CREATE TABLE gfl_produce
(
	time integer not null,
	rarity integer not null,
	dtype varchar[3] not null,
	doll varchar[128] not null
);

.import module/gfl/gfl_produce.csv gfl_produce
