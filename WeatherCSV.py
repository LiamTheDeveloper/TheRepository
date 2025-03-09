import pandas as pd
import pyodbc

#############################################################################################################
# Define Variables
#############################################################################################################
sqlServer   = r'.\sqlexpress;'
sqlDataBase = 'dbWeather;'
sqlTable    = '[public.rainfall]'
csvFile     = 'Rainfall_Data_2000_to_2024-sample.csv'
pushToSQL   = 1 # See line 49

try:
    #############################################################################################################
    # Build DataFrame
    #############################################################################################################

    # Import source file, set first row as headers, then drop first row from dataset
    df         = pd.read_csv(csvFile, header=None)
    df.columns = df.iloc[0]
    df         = df.drop(0).reset_index(drop=True)

    # Create list of location names -> for melting df from wide to long
    column_names     = df.columns.tolist()
    location_columns = column_names[1:10]

    # Transform data from wide to long format to match destination
    df_melted = pd.melt(df, 
                        id_vars    =['DATE'],
                        value_vars = location_columns,
                        var_name   ='Location',
                        value_name ='Rainfall_amount')
    #############################################################################################################
    # Clean data
    #############################################################################################################
    unique_values         = df_melted['Rainfall_amount'].unique()
    unique_values_decimal = str(len([val for val in unique_values if '.'  in str(val)]))
    unique_values_REF     = str(len([val for val in unique_values if val == '#REF!' in str(val)]))

    # Strip trailing .'s
    df_melted['Rainfall_amount'] = df_melted['Rainfall_amount'].str.rstrip('.')

    # Replace #REF!s with NULL
    df_melted.replace('#REF!', None, inplace=True)

    # Convert data to destination types
    df_melted['Location']        = df_melted['Location'].astype(str)
    df_melted['Rainfall_amount'] = pd.to_numeric(df_melted['Rainfall_amount'], errors='coerce')
    df_melted['Rainfall_amount'] = df_melted['Rainfall_amount'].fillna(0).round().astype(int)
    df_melted['Rainfall_amount'] = df_melted['Rainfall_amount'].replace(0, None)

except Exception as e:
    print(f"An error occurred: {e}")
    exit()
#############################################################################################################
# Push data to SQL -> set PushToSQL parameter = 1 to execute. PushToSQL = 0 for the purpose of this excercise
#############################################################################################################
if pushToSQL == 1:
    try:
        sql = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                            'SERVER='  +sqlServer+
                            'DATABASE='+sqlDataBase+
                            'Trusted_Connection=yes;')
        cursor = sql.cursor()

        for index, row in df_melted.iterrows():
            cursor.execute("INSERT INTO [dbo]." +sqlTable+ "(date, location, rainfall) VALUES (?, ?, ?)", 
                        (row['DATE'] ,row['Location'], row['Rainfall_amount']))
        sql.commit()
        print('Script Ran Successfully: Check table ' +sqlTable+ ' in SQL for the results')
        print('Note: The source data contained ' +unique_values_decimal+ ' rainfall decimal value(s) that were rounded to match destination type INT.')
        print('Note: The source data contained ' +unique_values_REF+ ' rainfall #REF! value(s) file.')
    
    except Exception as e:
        print(f"An error occurred when pushing to SQL: {e}")

elif pushToSQL != 1:
    print('Script Ran Successfully: No data sent to SQL, as PushToSQL parameter = ' +str(pushToSQL))
    print('Set parameter to 1 should you wish to send data to SQL.' )
