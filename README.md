# Service Order Management App

Simple internal web application for managing service orders, customers, priorities, status and operational indicators.

This project demonstrates how a small business or technical team can replace manual spreadsheets with a lightweight internal tool for tracking service requests and operational workflows.

## Overview

Many small businesses, maintenance teams and technical service providers manage service orders using spreadsheets, messages or paper forms.

This can make it difficult to track status, priorities, responsible people, deadlines and operational performance.

This app provides a simple example of how to organize service orders in a structured way.

## Features

- Register service orders
- Manage customer information
- Track order status
- Define priority levels
- Record service type
- Monitor deadlines
- View operational KPIs
- Filter orders by status, priority or customer
- Export or review operational data

## Example KPIs

- Total service orders
- Open service orders
- Completed service orders
- Orders by status
- Orders by priority
- Average resolution time
- Pending workload

## Tech Stack

- Python
- Streamlit
- Pandas
- SQLite
- Plotly

## Project Structure

```text
service-order-management-app/
├── README.md
├── requirements.txt
├── app.py
├── database/
│   └── service_orders.db
├── data/
│   └── sample_service_orders.csv
└── screenshots/
    └── app_preview.png
