# Service Order Management App

Simple internal web application for managing service orders, customers, priorities, status and operational indicators.

This project demonstrates how a small business, maintenance team or technical service provider can replace manual spreadsheets with a lightweight internal tool for tracking service requests and operational workflows.

## Overview

Many small businesses and technical teams manage service orders using spreadsheets, messages or paper forms.

This can make it difficult to track status, priorities, responsible people, deadlines, costs and operational performance.

This app provides a simple example of how to organize service orders in a structured way using Python and Streamlit.

## Features

- Load service order data from CSV
- Track order status
- Filter by status, priority, service type and technician
- Display operational KPI cards
- Monitor open, in-progress and completed orders
- Analyze workload by technician
- Analyze orders by priority
- Analyze orders by service type
- Track monthly service order volume
- Display filtered service order records

## Example KPIs

- Total service orders
- Open service orders
- In-progress service orders
- Completed service orders
- Estimated total cost
- Average resolution time
- Orders by status
- Orders by priority
- Workload by technician

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- CSV

## Project Structure

```text
service-order-management-app/
├── README.md
├── requirements.txt
├── .gitignore
├── app.py
├── data/
│   └── sample_service_orders.csv
└── screenshots/
    └── app_preview.png