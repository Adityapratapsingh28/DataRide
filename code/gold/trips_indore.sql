CREATE OR REPLACE VIEW transportation.gold.fact_trips_indore
AS (
SELECT *
FROM transportation.gold.fact_trips
WHERE city_id = 'MP01'
);