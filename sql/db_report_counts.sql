SELECT count(distinct fieldid) FROM censusdata;
SELECT case length(fipscode) 
         when 2 then 'state' 
         when 5 then 'county' 
         else 'tract' end, 
       count(*)
FROM censusdata
GROUP BY 1;

select 'users' tablename, count(*) from users union all
select 'maps', count(*) from maps union all
select 'datalayers', count(*) from datalayers union all
select 'valuebreaks', count(*) from valuebreaks;



