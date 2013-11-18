SELECT a.cartodb_id, a.geotype, sum(case when b.fieldid = 'B03002004' then b.value else 0 end) / sum(case when b.fieldid = 'B01001001' then b.value else 0 end) measure, a.the_geom_webmercator
FROM censusgeo a join acsdata b on a.fipscode = b.fipscode
GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator;
