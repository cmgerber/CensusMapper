-- generate the cartodb query
SELECT 'SELECT a.cartodb_id, a.geotype, sum(case when b.fieldid in (' UNION ALL
SELECT '''' || fieldid || ''',' FROM datalayers d JOIN numerator n ON d.measureid = n.measureid WHERE d.datalayersid = 5 UNION ALL
SELECT '''ZZZ'') then b.value else 0 end) ' UNION ALL
SELECT case when max(r.denominatorid) is not null then '/ sum(case when b.fieldid in (' else '' end FROM datalayers d JOIN denominator r ON d.measureid = r.measureid WHERE d.datalayersid = 5 UNION ALL
SELECT '''' || fieldid || ''',' FROM datalayers d JOIN denominator r ON d.measureid = r.measureid WHERE d.datalayersid = 5 UNION ALL
SELECT case when max(r.denominatorid) is not null then '''ZZZ'') then b.value else 0 end) ' else '' end FROM datalayers d JOIN denominator r ON d.measureid = r.measureid WHERE d.datalayersid = 5 UNION ALL
SELECT 'measure, a.the_geom_webmercator FROM censusgeo a JOIN acsdata b ON a.fipscode = b.fipscode GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator';

-- generate the cartocss polygon fill style
SELECT '[ measure <= ' || round(cast(maxvalue as numeric),2) || ' ] { polygon-fill: rgb(' || redvalue || ',' || bluevalue || ',' || greenvalue || ')}' cartocss
FROM datalayers d JOIN colorschemes c ON d.colorschemename = c.colorschemename and d.numcategories = c.numcategories
  JOIN valuebreaks v ON d.datalayersid = v.datalayersid and v.categorynumber = c.categorynumber
WHERE d.datalayersid = 5
ORDER BY maxvalue desc;

-- update the value breaks
UPDATE valuebreaks
SET maxvalue = 
  case categorynumber
    when 1 then 0.03
    when 2 then 0.06
    when 3 then 0.10
    when 4 then 0.15
    when 5 then 1.0 end
WHERE datalayersid = 5;

UPDATE valuebreaks as v1
SET minvalue = 
  case when categorynumber = 1 then 0
       else (SELECT v2.maxvalue FROM valuebreaks v2 WHERE v1.datalayersid = v2.datalayersid and v2.categorynumber = v1.categorynumber - 1) end
WHERE datalayersid = 5;


[ measure <= 1.00 ] { polygon-fill: rgb(179,0,0)}
[ measure <= 0.40 ] { polygon-fill: rgb(227,51,74)}
[ measure <= 0.25 ] { polygon-fill: rgb(252,89,141)}
[ measure <= 0.15 ] { polygon-fill: rgb(253,138,204)}
[ measure <= 0.05 ] { polygon-fill: rgb(254,217,240)}