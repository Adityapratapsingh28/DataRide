CREATE OR REPLACE VIEW transportation.gold.fact_trips_lucknow
AS (
SELECT *
FROM transportation.gold.fact_trips
WHERE city_id = 'UP01'
);