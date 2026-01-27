CREATE OR REPLACE VIEW transportation.gold.fact_trips_kochi
AS (
SELECT *
FROM transportation.gold.fact_trips
WHERE city_id = 'KL01'
);