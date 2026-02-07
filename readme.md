
## What is DataRide?
DataRide is a data engineering platform that processes transportation trip data through a three-tier medallion architecture. The system ingests raw CSV files from S3 storage, applies progressive transformations and quality checks, and produces analytics-ready datasets for business intelligence and reporting.

<img width="14204" height="4628" alt="image" src="https://github.com/user-attachments/assets/892aaca7-e586-4719-84f7-4c0459dac520" />



## The platform supports:

- 10 Cities: Chandigarh, Coimbatore, Indore, Jaipur, Kochi, Lucknow, Mysore, Surat, Vadodara, and Visakhapatnam
- Two Data Domains: City reference data (dimension) and trip transaction data (fact)
- Mixed Processing Patterns: Batch loading for reference data and streaming ingestion for transactional data
- Change Data Capture: Row-level tracking of modifications with SCD Type 1 semantics


## Medallion Architecture
DataRide follows the medallion architecture pattern with three distinct layers, each serving a specific purpose in the data pipeline.
### Architecture Diagram
<img width="634" height="618" alt="Screenshot 2026-02-07 at 12 07 54 PM" src="https://github.com/user-attachments/assets/0c95e989-7a2e-4b17-b0eb-565f21d6cc1f" />

### Layer Descriptions


## Data Processing Layers

| Layer  | Schema                   | Purpose                               | Key Characteristics |
|---------|---------------------------|----------------------------------------|---------------------|
| Bronze | transportation.bronze     | Raw data ingestion from S3             | Schema inference, error handling with `_rescued_data`, minimal transformations |
| Silver | transportation.silver     | Cleaned and validated data             | Type casting, data quality expectations, CDC enabled, processing timestamps |
| Gold   | transportation.gold       | Business-ready analytics               | Star schema design, denormalized joins, city-specific views |

## Technology Stack
DataRide is built on the Databricks platform using modern data engineering technologies:
### Core Technologies

<img width="658" height="246" alt="Screenshot 2026-02-07 at 12 11 09 PM" src="https://github.com/user-attachments/assets/d0e25082-2f5a-47b6-8f07-35fc4ac6f81a" />

### Technology Components

| Component      | Purpose                           | Key Features Used |
|---------------|-----------------------------------|-------------------|
| Databricks    | Unified analytics platform         | Notebooks, workflows, collaborative environment |
| Apache Spark  | Distributed processing engine      | PySpark API, structured streaming |
| Delta Lake    | Storage layer with ACID properties | Change Data Feed, auto-optimization, time travel |
| Unity Catalog | Centralized governance             | Three-tier namespace (catalog.schema.table) |
| Auto Loader   | Incremental file processing        | Schema inference, PERMISSIVE mode, cloudFiles |
| AWS S3        | Object storage                     | Source data repository |

## Data Flow Overview
### End-to-End Pipeline

<img width="593" height="464" alt="Screenshot 2026-02-07 at 12 12 47 PM" src="https://github.com/user-attachments/assets/4d2f5b8e-9937-404c-9c98-4abfeece9732" />

### Processing Characteristics

#### Bronze Layer:

- City data: Batch processing with schema inference
- Trips data: Streaming with Auto Loader (cloudFiles)
- Error handling: PERMISSIVE mode captures corrupt records in _rescued_data column

#### Silver Layer:

- Data quality expectations on dates and ratings
- CDC upsert with id as natural key
- Processing timestamps added for lineage tracking
- Calendar dimension generated programmatically (not ingested)
#### Gold Layer:

- Star schema with fact_trips as central table
- Denormalized joins to city and calendar dimensions
- 10 filtered views for city-specific access patterns

### Unity Catalog Structure
The DataRide platform uses Unity Catalog with a three-tier namespace pattern: catalog.schema.table.

## Catalog Hierarchy


<img width="593" height="64" alt="Screenshot 2026-02-07 at 12 15 19 PM" src="https://github.com/user-attachments/assets/9f18ad3d-0a73-4457-8455-c1d27c113514" />




## Key Features
### 1. Multi-City Support
DataRide processes data for 10 cities across India, using standardized city identifiers:
## Supported Cities

| City ID | City Name      | State           |
|----------|---------------|-----------------|
| CH01     | Chandigarh    | Chandigarh      |
| TN01     | Coimbatore    | Tamil Nadu      |
| MP01     | Indore        | Madhya Pradesh  |
| RJ01     | Jaipur        | Rajasthan       |
| KL01     | Kochi         | Kerala          |
| UP01     | Lucknow       | Uttar Pradesh   |
| KA01     | Mysore        | Karnataka       |
| GJ01     | Surat         | Gujarat         |
| GJ02     | Vadodara      | Gujarat         |
| AP01     | Visakhapatnam | Andhra Pradesh  |

### 2. Streaming and Batch Processing
- Streaming: Trip data ingested via Databricks Auto Loader with incremental processing
- Batch: City reference data loaded in full batch mode
- Hybrid: Combines both patterns in a unified pipeline
### 3. Change Data Capture (CDC)
- Enabled on silver.trips table via Change Data Feed
- Tracks row-level changes for audit and incremental downstream processing
- Uses id as natural key and silver_processed_timestamp for sequencing
- Implements SCD Type 1 (overwrite on change) semantics
### 4. Data Quality Framework
- Bronze Layer: PERMISSIVE mode for resilient ingestion
- Silver Layer: Expectations for data validation
   - valid_date: Year must be >= 2020
   - valid_driver_rating: Rating in range 1-10
   - valid_passenger_rating: Rating in range 1-10
- Rescued Data: Corrupt records isolated in _rescued_data column


### 5. Star Schema Design
The gold layer implements a dimensional model:

- Fact Table: gold.fact_trips (measures: distance, sales, ratings)
- Dimensions: silver.city (geography), silver.calendar (time)
- Filtered Views: 10 city-specific views for optimized access


## Repository Structure
The DataRide codebase is organized into notebooks and configuration files:

<img width="459" height="123" alt="Screenshot 2026-02-07 at 12 19 33 PM" src="https://github.com/user-attachments/assets/1eb99747-7a7b-4bd2-8a6a-0fa68bf375dc" />


### Notebook Workflow
- Setup: Run project_setup.ipynb to create Unity Catalog structure
- Bronze: Execute bronze layer notebooks to ingest raw data
- Silver: Run silver layer notebooks to clean and validate data
- Gold: Execute gold layer notebooks to create analytics tables





## Target Use Cases
DataRide supports multiple analytical use cases:

- City-Specific Dashboards: Regional teams access filtered views for their city
- Cross-City Analytics: Compare performance metrics across all 10 cities
- Time-Series Analysis: Calendar dimension enables temporal analytics (weekday/weekend, holidays, trends)
- Data Science: Star schema provides clean, denormalized data for ML model training
- Operational Reporting: Real-time streaming enables near real-time operational metrics




















