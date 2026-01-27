CREATE OR REPLACE VIEW transportation.gold.fact_trips_jaipur
AS (
SELECT *
FROM transportation.gold.fact_trips
WHERE city_id = 'RJ01'
);