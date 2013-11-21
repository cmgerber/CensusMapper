drop table if exists censusgeo;

create table censusgeo 
  (fipscode varchar(11),
   name varchar(100),
   geotype varchar(10),
   geom geometry
);

insert into censusgeo
select state fipscode, name, 'state' geotype, geom
from state;

insert into censusgeo
select state||county, name, 'county', geom
from county;

insert into censusgeo
select state||county||tract, name, 'tract', geom
from tract
where county in ('001','013','041','055','075','081','085','087','095','097');


-- ./pgsql2shp jost censusgeo