from src.database.update_table_stock_statistics import (
    insert_updated_statistics_data_into_db,
)


def weekly_update_stock_statistics():
    insert_updated_statistics_data_into_db()
    print("complete stock statistics")


if __name__ == "__main__":
    weekly_update_stock_statistics()