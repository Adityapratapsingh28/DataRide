CREATE OR REPLACE VIEW transportation.gold.fact_trips_mysore
AS (
SELECT *
FROM transportation.gold.fact_trips
WHERE city_id = 'KA01'
);