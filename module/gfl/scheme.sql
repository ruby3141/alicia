.separator ","

CREATE TABLE gfl_expc
(
	lv integer not null primary key,
	experience integer not null
);

.import module/gfl/gfl_expc.csv gfl_expc
