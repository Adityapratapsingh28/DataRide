CREATE OR REPLACE VIEW transportation.gold.fact_trips_coimbatore
AS (
SELECT *
FROM transportation.gold.fact_trips
WHERE city_id = 'TN01'
);