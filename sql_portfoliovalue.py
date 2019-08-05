import config

# ssh variables
host = config.sqldb_ssh

# database variables
user = config.sqldb_superuser['id']
password = config.sqldb_superuser['secret']
db_name = 'brokers_master'
db_folder = config.db_path

from sqlalchemy import exc
import pandas as pd
from sqlalchemy import create_engine
import os

pd.set_option('display.max_columns', 500)



def get_different_rows(source_df, new_df):
    # print(new_df.tail())
    # print(source_df.tail())
    """Returns just the rows from the new dataframe that differ from the source dataframe"""
    if len(new_df) > len(source_df):
        longer_df = new_df
        short_df = source_df
    else:
        longer_df = source_df
        short_df = new_df
    new_rows = []
    for i in range(len(longer_df)):
        d1 = longer_df['Date'].iloc[i]
        try:
            d2 = short_df['Date'].iloc[i]
        except:
            d2 = False

        if d2 == False:
            new_rows.append(longer_df.iloc[i])
            print('df1:', d1, 'df2:', d2)
    print(new_rows)
    return new_rows


def append_portfolio_values_sql(accountnumber):
    df = pd.read_csv(os.path.join(db_folder, 'mysql_db_csv/portfolio_value/', str(accountnumber + '.csv')))
    df.rename(columns={'Date': 'Date'})
    df['account_number'] = accountnumber


    # con = mysql.connector.connect(user=user, password=password, host=host, port='3307', db=db_name)
    engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + '3307' + '/' + db_name,
                           echo=False)
    con = engine.connect()

    df_old = pd.read_sql(sql='portfolio_value', con=con, index_col='entry', parse_dates='Date')
    df_old = df_old.reset_index(drop=True)
    df_old = df_old.loc[df_old['account_number'] == int(accountnumber)]

    df = df.reset_index(drop=False)



    new_rows = get_different_rows(df_old, df)
    print(new_rows)
    # new_rows = df
    num_rows = len(new_rows)

    dub = 0
    for i in range(num_rows):

        try:
            # Try inserting the row
            row = pd.DataFrame(new_rows[i]).T
            row=row.drop(['index'],axis=1)
            print(row)
            row['Date'] = pd.to_datetime(row['Date'])
            row['cash'] = float(row['cash'])
            row['portfolio_value'] = float(row['portfolio_value'])
            row['total_value'] = float(row['total_value'])
            row['account_number'] = int(row['account_number'])
            row['broker_id'] = int(row['broker_id'])
            row['entry'] = 0


            row.to_sql(con=con, name='portfolio_value', index=False, if_exists='append', schema=db_name)

        except exc.IntegrityError:
            #     # Ignore duplicates
            print('error')
            dub += 1
            pass

    con.close()


def update_local_portfoliovalue_csv_fromsql(accountnumber):
    engine = create_engine('mysql+pymysql://' + user + ':' + password + '@' + host + ':' + '3307' + '/' + db_name,
                           echo=False)
    con = engine.connect()
    # print(con.get_server_info())
    df_old = pd.read_sql(sql='portfolio_value', con=con, index_col='entry', parse_dates='Date')
    df_old = df_old.reset_index(drop=True)
    df_old = df_old.loc[df_old['account_number'] == int(accountnumber)]

    '''Write CSV'''
    df_old.to_csv(os.path.join(db_folder, 'mysql_db_csv/portfolio_value/', str(accountnumber + '.csv')), index=False)
    print(df_old.tail())
    con.close()


def clean_local_csv(accountnumber):
    df = pd.DataFrame.from_csv(os.path.join(db_folder, 'mysql_db_csv/portfolio_value/', str(accountnumber + '.csv')))

    print(df.head())
    df['total_value'] = df['total_value'].map(lambda x: x.lstrip('$').rstrip(''))
    df['total_value'] = df['total_value'].str.replace(",", "").astype(float)
    print(df.tail())
    df['total_value'] = df['total_value'].astype(float)
    df.reset_index(drop=False)

    print(df.tail())
    df.to_csv(os.path.join(db_folder, 'mysql_db_csv/portfolio_value/', str(accountnumber + '.csv')))


append_portfolio_values_sql('54816757')
#update_local_portfoliovalue_csv_fromsql('54816757')