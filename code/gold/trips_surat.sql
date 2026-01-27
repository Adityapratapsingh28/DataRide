CREATE OR REPLACE VIEW transportation.gold.fact_trips_surat
AS (
SELECT *
FROM transportation.gold.fact_trips
WHERE city_id = 'GJ01'
);