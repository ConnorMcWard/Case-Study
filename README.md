# ER Diagram Overview

![image](https://github.com/ConnorMcWard/Case-Study/assets/57818139/8bd0bcf6-f150-4362-80c8-9587800d3b1d)


This ERD diagram consists of four tables: **Property**, **Unit**, **Pricing**, and **Fee**. Below is a description of the relationships and fields within each table:

## 1. Property Table
- **Fields**: Property ID (PK), Property Name, Marketing Name, Full Address, Street Address, City, State Code, Postal Code, Country Code, Longitude, Latitude, Belonged City, Description, Neighborhood, Neighborhood Description, Currency Code.
- **Relationship**: Each property can have one or more associated units, establishing a one-to-many relationship with the **Unit** table.

## 2. Unit Table
- **Fields**: Unit ID (Primary Key), Property ID (Foreign Key), Room Number, Number of Bedrooms, Listing Square Footage, Unit Square Footage, Occupancy Type, Availability Date, Minimum Stay, Minimum Price, Maximum Price.
- **Relationships**:
  - **Fee**: A unit can have zero or more relationships with the **Fee** table, indicating that a unit may have none, one, or multiple fees associated.
  - **Pricing**: A unit can have one or more relationships with the **Pricing** table, meaning each unit can have one or multiple pricing entries.

## 3. Pricing Table
- **Fields**: Unit ID (Foreign Key), Name, Number of Months, Amount, Concession Description.
- **Description**: This table stores different pricing options for each unit, where each pricing entry can include potential concessions.

## 4. Fee Table
- **Fields**: Unit ID (Foreign Key), Fee Name, Description, Amount, Is Mandatory (boolean), Is Refundable (boolean).
- **Description**: The fee table records various fees associated with each unit, specifying whether each fee is mandatory and whether it is refundable.

## Deviation from 3NF
- **Explanation**: In implementing this database design, we do not fully adhere to the third normal form. This decision stems from the need to optimize for practical usage scenarios over theoretical database normalization principles. Specifically, the challenge lies in accommodating a flexible pricing structure that can vary significantly across different properties without necessitating a complete system redesign or a standardized pricing model.

## Scalability Considerations
- **Adding More Properties**: The design supports scalability in terms of property expansion. New properties can be added seamlessly to the **Property** table without impacting the performance of the system. The one-to-many relationship from properties to units ensures that the system can scale horizontally as new properties are added.
- **Handling Increased Transaction Volume and Data Size**: The separation of concerns by having distinct tables for units, pricing, and fees allows the database to handle increased loads and transaction volumes effectively. This modular approach means that queries can be optimized on a per-table basis, and indexes can be used efficiently to speed up data retrieval operations as the size of the database grows.

**Summary**:
This schema is designed to balance practicality and performance, acknowledging trade-offs in normalization for the benefit of scalability and flexibility in real-world applications.
