from pyspark import pipelines as dp
from pyspark.sql import functions as F

start_date = spark.conf.get("start_date")
end_date = spark.conf.get("end_date")


@dp.materialized_view(
    name="transportation.silver.calendar",
    comment="Calendar dimension with comprehensive date attributes and Indian holidays (2025)",
    table_properties={
        "quality": "transportation.silver.calendar",
        "layer": "silver",
        "delta.enableChangeDataFeed": "true",
        "delta.autoOptimize.optimizeWrite": "true",
        "delta.autoOptimize.autoCompact": "true",
    },
)
def calendar():
    df = spark.sql(
        f"""
        SELECT explode(sequence(
            to_date('{start_date}'),
            to_date('{end_date}'),
            interval 1 day
        )) as date
    """
    )

    df = df.withColumn(
        "date_key", F.date_format(F.col("date"), "yyyyMMdd").cast("int")
    )

    df = (
        df.withColumn("year", F.year(F.col("date")))
        .withColumn("month", F.month(F.col("date")))
        .withColumn("quarter", F.quarter(F.col("date")))
    )

    df = (
        df.withColumn("day_of_month", F.dayofmonth(F.col("date")))
        .withColumn("day_of_week", F.date_format(F.col("date"), "EEEE"))
        .withColumn("day_of_week_abbr", F.date_format(F.col("date"), "EEE"))
        .withColumn("day_of_week_num", F.dayofweek(F.col("date")))
    )

    df = (
        df.withColumn("month_name", F.date_format(F.col("date"), "MMMM"))
        .withColumn(
            "month_year",
            F.concat(F.date_format(F.col("date"), "MMMM"), F.lit(" "), F.col("year")),
        )
        .withColumn(
            "quarter_year",
            F.concat(F.lit("Q"), F.col("quarter"), F.lit(" "), F.col("year")),
        )
    )

    df = df.withColumn(
        "week_of_year", F.weekofyear(F.col("date"))
    ).withColumn("day_of_year", F.dayofyear(F.col("date")))

    df = df.withColumn(
        "is_weekend",
        F.when(F.col("day_of_week_num").isin([1, 7]), True).otherwise(False),
    ).withColumn(
        "is_weekday",
        F.when(F.col("day_of_week_num").isin([1, 7]), False).otherwise(True),
    )

    df = df.withColumn(
        "holiday_name",
        F.when(
            (F.col("month") == 1) & (F.col("day_of_month") == 26), F.lit("Republic Day")
        )
        .when(
            (F.col("month") == 8) & (F.col("day_of_month") == 15),
            F.lit("Independence Day"),
        )
        .when(
            (F.col("month") == 10) & (F.col("day_of_month") == 2),
            F.lit("Gandhi Jayanti"),
        )
        .otherwise(None),
    ).withColumn(
        "is_holiday", F.when(F.col("holiday_name").isNotNull(), True).otherwise(False)
    )

    df = df.withColumn(
        "silver_processed_timestamp", F.current_timestamp()
    )

    df_silver = df.select(
        "date",
        "date_key",
        "year",
        "month",
        "day_of_month",
        "day_of_week",
        "day_of_week_abbr",
        "month_name",
        "month_year",
        "quarter",
        "quarter_year",
        "week_of_year",
        "day_of_year",
        "is_weekday",
        "is_weekend",
        "is_holiday",
        "holiday_name",
        "silver_processed_timestamp"
    )

    return df_silver
