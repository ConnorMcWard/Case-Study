# Case Study Overview

## Table of Contents
- [Case Study Overview](#case-study-overview)
- [Description](#description)
- [Schema Write-up](#schema-write-up)
  - [ER Diagram Overview](#er-diagram-overview)
  - [Normalization](#normalization)
  - [Assumptions](#assumptions)
- [Tables and Relationships](#tables-and-relationships)
  - [Property Table](#1-property-table)
  - [Unit Table](#2-unit-table)
  - [Pricing Table](#3-pricing-table)
  - [Fee Table](#4-fee-table)
- [Scalability](#scalability)
- [Docker Run Commands](#docker-run-commands)

## Description
We rent units of two major types: Co-living and Traditional.

A Co-living Unit is a Room within an Apartment that is rented.  
A Traditional Unit is an entire Apartment that is rented.

Both types of rentable Units have at least one Applicant.  
Both types of rentable Units may have additional Co-Applicants.

An Apartment may be:
- entirely Co-living
- entirely Traditional
- a mix of Co-living and Traditional

Unit (Rent) Prices are for individual Units and given durations (e.g., $1,307 for 18 Months).  
A Price may have zero or more Concessions (i.e., money off).

Units have zero or more Fees (e.g., Screen Fee).

## Schema Write-up
Create a write-up detailing your proposed (normalized) schema for the above relationships. Please attach visuals in the form of either an ER diagram or a relational schema. Your write-up should be in narrative format (not bullet points).

You do not need to assume that you are working in any particular database system.

### ER Diagram Overview
![ER Diagram](https://github.com/ConnorMcWard/Case-Study/assets/57818139/946d5071-f051-4bc6-9342-c227604dcf7e)

This ER diagram consists of four tables: **Property**, **Unit**, **Pricing**, and **Fee**. I chose both Property and Unit tables due to them having their own IDs when we call the API. This separation allows us to capture the most granular information for our records without introducing redundancy.

With performance in mind, I decided to create both a fee table and a pricing table. When running queries, if pricing and fee information were in the same table as unit information, it might make queries more complex and slower due to the larger dataset. By keeping them separate, you can quickly run reports or queries on pricing and fees without having to deal with unit-specific data, which may not be relevant to the query.

Represented in the ER Diagram, I have a Composite Key (CK) for both the Pricing and Fee Tables. The Composite Key is how to uniquely identify a pricing option or fee.

I also initially created a Neighborhood table to store the neighborhood description (again improving performance). However, since there are no unique modifiers and it would be possible to have two of the same neighborhood name, I decided against it and merged the Neighborhood table into the Property table.

### Normalization
I used a 3 Normal Form (3NF) for my normalization of this database schema. 3NF is a good balance between normalization and performance and standard for most business applications. For 3NF, I first have to satisfy the 1NF requirement of each table having a primary key as a way to keep unique records and all attributes are atomic (non-divisible). Using a composite key, as I did for both the Pricing and Fee tables, still maintains 1NF. For 2NF, this is completed by ensuring all attributes are dependent on the primary or composite key. Finally, for 3NF, I made sure that every non-key attribute isn't dependent on any other non-key attribute.

### Assumptions
- Property information is fairly stable and doesn't change frequently.
- Each Unit is unique to the Property it belongs to.
- Each Fee is unique enough that it warrants a separate record linking it to the unit. When looking at my results.json, it seems that we could simplify the Fee table to only a few records and connect them to the Unit table with a foreign key. This would require a standardized Fee ID (PK) that doesn't require a foreign key as part of its composite key.

## Tables and Relationships

### 1. Property Table
- **Fields**: Property ID (Primary Key), Property Name, Marketing Name, Full Address, Street Address, City, State Code, Postal Code, Country Code, Longitude, Latitude, Belonged City, Description, Neighborhood, Neighborhood Description, Currency Code.
- **Description**: The Property table records the information about the physical location that the unit or units are located on.
- **Relationship**: Each property can have one or more associated units, establishing a one-to-many relationship with the **Unit** table.

### 2. Unit Table
- **Fields**: Unit ID (Primary Key), Property ID (Foreign Key), Room Number, Number of Bedrooms, Listing Square Footage, Unit Square Footage, Occupancy Type, Availability Date, Minimum Stay, Minimum Price, Maximum Price.
- **Description**: The Unit table records various attributes about the physical apartment, as well as when it is available and the minimum and maximum pricing options.
- **Relationships**:
  - **Fee**: A unit can have zero or more relationships with the **Fee** table, indicating that a unit may have none, one, or multiple fees associated.
  - **Pricing**: A unit can have one or more relationships with the **Pricing** table, meaning each unit can have one or multiple pricing entries.

### 3. Pricing Table
- **Fields**: Unit ID (Foreign Key, Composite Key), Name (Composite Key), Number of Months, Amount, Concession Description.
- **Description**: The Pricing table stores different pricing options for each unit, where each pricing entry can include potential concessions.

### 4. Fee Table
- **Fields**: Unit ID (Foreign Key, Composite Key), Fee Name (Composite Key), Description, Amount, Is Mandatory (boolean), Is Refundable (boolean).
- **Description**: The Fee table records various fees associated with each unit, specifying whether each fee is mandatory and whether it is refundable.

## Scalability
With this database design, we can scale for renting to businesses with no issues. We could create a Business table which links to the Unit table through a unit_id Foreign Key. This would not cause any major change in the database design.



# Docker Run Commands
- Clone the repository
```
git clone https://github.com/ConnorMcWard/Case-Study
```

- Change directory
```
cd Case-Study
```

- Build Docker Image
```
docker build -t etl .
```

- Run Docker Container with Volume Mounting to output folder
```
docker run -v "$(pwd)/output:/output" etl
```
