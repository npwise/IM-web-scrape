# import libraries
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import sys


def get_table(url):
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'lxml')          #parse html
    table = soup.find_all('table')[0]           #Grab the first table
    return table

def set_columns(table):

    n_columns = 0
    n_rows=0
    column_names = []

    # Find the number of rows and columns
    for row in table.find_all('tr'):
        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)

        # Handle column names if we find them
        th_tags = row.find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

    # Error checking for Column Names
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("The column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns=columns, index= range(0,n_rows))

    return df

def get_row_count(table):
    n_rows=0
    # Find the number of rows and columns
    for row in table.find_all('tr'):
        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows+=1
    return n_rows

def get_results(df,table):
    row_marker = 0
    for row in table.find_all('tr'):
        #print(row)
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            #print(column.get_text())
            #print("ROW: {}   COL: {}".format(row_marker, column_marker))
            df.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    return df




if __name__ == '__main__':
    im_start_page = "http://www.ironman.com/triathlon/events/americas/ironman/world-championship/results.aspx"
    url = "http://www.ironman.com/triathlon/events/americas/ironman/world-championship/results.aspx?p={page_nr}&ps=20#axzz5F4J2YBv1"

    #set initial table to get columns
    table = get_table(im_start_page)
    #set initial columns names
    im_results_df = set_columns(table)

    rowcount = get_row_count(table)



    for i in range(10):
        page_nr = i + 1
        web_page = url.format(page_nr=page_nr)
        print(web_page)
        table = get_table(web_page)
        im_results_df = get_results(im_results_df,table)
        print(im_results_df)
