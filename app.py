from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sample_service_orders.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and prepare service order data."""
    df = pd.read_csv(DATA_PATH)

    date_columns = ["created_date", "due_date", "completed_date"]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    df["estimated_cost"] = pd.to_numeric(df["estimated_cost"], errors="coerce")
    df["created_month"] = df["created_date"].dt.to_period("M").astype(str)

    df["resolution_days"] = (
        df["completed_date"] - df["created_date"]
    ).dt.days

    df["is_overdue"] = (
        (df["status"] != "Completed")
        & (df["due_date"] < pd.Timestamp.today())
    )

    return df


def format_currency(value: float) -> str:
    """Format numeric values as currency."""
    return f"${value:,.2f}"


def main() -> None:
    st.set_page_config(
        page_title="Service Order Management App",
        page_icon="🛠️",
        layout="wide",
    )

    st.title("Service Order Management App")
    st.caption(
        "Simple internal tool for managing service orders, status, priorities and operational KPIs."
    )

    df = load_data()

    st.sidebar.header("Filters")

    status_options = sorted(df["status"].dropna().unique())
    priority_options = sorted(df["priority"].dropna().unique())
    service_type_options = sorted(df["service_type"].dropna().unique())
    assigned_options = sorted(df["assigned_to"].dropna().unique())

    selected_status = st.sidebar.multiselect(
        "Status",
        options=status_options,
        default=status_options,
    )

    selected_priority = st.sidebar.multiselect(
        "Priority",
        options=priority_options,
        default=priority_options,
    )

    selected_service_type = st.sidebar.multiselect(
        "Service Type",
        options=service_type_options,
        default=service_type_options,
    )

    selected_assigned_to = st.sidebar.multiselect(
        "Assigned To",
        options=assigned_options,
        default=assigned_options,
    )

    filtered_df = df[
        df["status"].isin(selected_status)
        & df["priority"].isin(selected_priority)
        & df["service_type"].isin(selected_service_type)
        & df["assigned_to"].isin(selected_assigned_to)
    ]

    total_orders = len(filtered_df)
    open_orders = len(filtered_df[filtered_df["status"] == "Open"])
    in_progress_orders = len(filtered_df[filtered_df["status"] == "In Progress"])
    completed_orders = len(filtered_df[filtered_df["status"] == "Completed"])

    total_estimated_cost = filtered_df["estimated_cost"].sum()

    completed_df = filtered_df.dropna(subset=["resolution_days"])
    average_resolution_days = (
        completed_df["resolution_days"].mean()
        if not completed_df.empty
        else 0
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Orders", f"{total_orders:,}")
    col2.metric("Open", f"{open_orders:,}")
    col3.metric("In Progress", f"{in_progress_orders:,}")
    col4.metric("Completed", f"{completed_orders:,}")
    col5.metric("Estimated Cost", format_currency(total_estimated_cost))

    st.metric(
        "Average Resolution Time",
        f"{average_resolution_days:.1f} days",
    )

    st.divider()

    status_report = (
        filtered_df.groupby("status", as_index=False)
        .agg(total_orders=("order_id", "count"))
        .sort_values("total_orders", ascending=False)
    )

    priority_report = (
        filtered_df.groupby("priority", as_index=False)
        .agg(total_orders=("order_id", "count"))
        .sort_values("total_orders", ascending=False)
    )

    service_type_report = (
        filtered_df.groupby("service_type", as_index=False)
        .agg(
            total_orders=("order_id", "count"),
            estimated_cost=("estimated_cost", "sum"),
        )
        .sort_values("total_orders", ascending=False)
    )

    assigned_report = (
        filtered_df.groupby("assigned_to", as_index=False)
        .agg(total_orders=("order_id", "count"))
        .sort_values("total_orders", ascending=False)
    )

    monthly_report = (
        filtered_df.groupby("created_month", as_index=False)
        .agg(total_orders=("order_id", "count"))
        .sort_values("created_month")
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Orders by Status")
        fig_status = px.bar(
            status_report,
            x="status",
            y="total_orders",
            text_auto=True,
            labels={
                "status": "Status",
                "total_orders": "Orders",
            },
        )
        st.plotly_chart(fig_status, use_container_width=True)

    with chart_col2:
        st.subheader("Orders by Priority")
        fig_priority = px.pie(
            priority_report,
            names="priority",
            values="total_orders",
            hole=0.45,
        )
        st.plotly_chart(fig_priority, use_container_width=True)

    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.subheader("Service Types")
        fig_service_type = px.bar(
            service_type_report,
            x="service_type",
            y="total_orders",
            text_auto=True,
            labels={
                "service_type": "Service Type",
                "total_orders": "Orders",
            },
        )
        st.plotly_chart(fig_service_type, use_container_width=True)

    with chart_col4:
        st.subheader("Workload by Technician")
        fig_assigned = px.bar(
            assigned_report,
            x="assigned_to",
            y="total_orders",
            text_auto=True,
            labels={
                "assigned_to": "Technician",
                "total_orders": "Orders",
            },
        )
        st.plotly_chart(fig_assigned, use_container_width=True)

    st.subheader("Monthly Service Orders")
    fig_monthly = px.line(
        monthly_report,
        x="created_month",
        y="total_orders",
        markers=True,
        labels={
            "created_month": "Month",
            "total_orders": "Orders",
        },
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    st.subheader("Filtered Service Orders")

    display_columns = [
        "order_id",
        "customer_name",
        "service_type",
        "priority",
        "status",
        "assigned_to",
        "created_date",
        "due_date",
        "completed_date",
        "estimated_cost",
        "notes",
    ]

    st.dataframe(
        filtered_df[display_columns].sort_values("created_date", ascending=False),
        use_container_width=True,
    )


if __name__ == "__main__":
    main()