from src.database.update_table_analysis_info_revenue_sp500 import insert_updated_analysis_info_revenue_data_into_db

def weekly_update_analysis_info_revenue():
    insert_updated_analysis_info_revenue_data_into_db()
    print('complete analysis info revenue sp500')


if __name__ == '__main__':
    weekly_update_analysis_info_revenue()