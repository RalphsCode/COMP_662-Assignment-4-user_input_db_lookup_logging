# !/usr/bin/env python3

# Assignment 4 - More SQL
# Author: Ralph Godkin

'''
General Comments: This Assignment is 2 parts, divided below by a line of hashes #####.
(1) The first part makes a couple of adjustments to the dbmovies.db database.
(2) The second part asks the user to enter a year and then searches the database
    for movies made in that year.
The log file 'movieDB.log' tracks the application progress.
 '''

# Imports
import logging
import os
import sqlite3

# Configure the logging module
logging.basicConfig(filename="movieDB.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():

    ##########################################################################################
    #  Part 1 - Database Updates

    # Update log 
    logging.debug('+++   Starting App   +++') 
    # Open the database connection
    database_file = 'dbmovies.sqlite'
    # Ensure the database exists prior to continueing. Thereby preventing a database being created by this application
    if os.path.exists(database_file):
        conn = sqlite3.connect(database_file)
    else:
        print(f"Database file '{database_file}' was not found.")    
        return

    # Create a cursor object to execute SQL statements
    cursor = conn.cursor()

    # Update log
    logging.debug('Successfully: (1)connected to database  (2)created cursor') 

    # Perform database updates
    cursor.execute("UPDATE Movie SET year = 1995 WHERE name = 'Toy Story';") 
    cursor.execute("DELETE FROM Movie WHERE name = 'Lawrence of Arabia';")

    # Commit the changes to the database
    conn.commit()

    # Print completion statement
    print('\n\t DATABASE UPDATES COMPLETED SUCCESFULLY.')
    
    # Update log
    logging.debug('Successfully completed Part 1: the database updates. Starting part 2.') 


    ###########################################################################################
    #  Part 2 - Find a Movie based on year as entered by user.

    def get_a_year(): 
        ''' This function requests the user to enter a year to lookup.
            The function then calls a function to validate the user input.
            '''
        entered_str = input('Please enter a year to look up between 1975 and 2013: ') or 2002
        
        # Update log
        logging.debug(f'User entered: {entered_str}.') 

        # Call the function to validate the user input
        return validate_year(entered_str)

        
    def validate_year(entered_str):
        ''' This function validates the user entry to ensure it is a valid year.'''

        # Ensure the entry is an integer
        try:
            int(entered_str)
        except ValueError:
            print(f'\nOoops: {entered_str} is not a year between 1975 and 2013, please try again.\n')
            return None
        
        # Check that the entry is between 1975 and 2013
        year_verified = int(entered_str)
        if year_verified < 1975:
            print(f'\nOoops: {year_verified} is prior to 1975, please try again.\n')
            return None
        elif year_verified > 2013:
            print(f'\nOoops: {year_verified} is after 2013, please try again.\n')
            return None
        
        # Update log
        logging.debug('Valid entry by user - looking up year in database') 

        # Once validated, return the year to the application    
        return year_verified


    def look_for_movies(lookup_year):
        ''' This function searches the dbmovies.db database for all Movies that were made in the year entered by the user
            and displays the results.
            '''
        cursor.execute("SELECT Movie.year, Movie.name, Movie.minutes, Category.name FROM Movie INNER JOIN category ON Movie.categoryID = Category.categoryID WHERE Movie.year = ?;", (lookup_year,))

        results = cursor.fetchall()
        if len(results) == 0:
            print(f'Sorry, no movies found that were made in {lookup_year}.')
            # Update log
            logging.debug('No movie results found.') 
        
            return
        else:
            print('Year / Movie Name / Length / Genre')
            print('-' *40)
            for row in results:
                print(f'{row[0]}  /  {row[1]}  /   {row[2]}  /  {row[3]}')
            # Update log
            logging.debug('Matching movie results displayed.') 


    # Print a welcome message
    print('\n\tWelcome to the Movie Year Lookup App.\n')

    # Create a 'while not break' loop to be able to repeat the lookup
    while True:
        # Call the function to request a year from the user
        lookup_year = get_a_year()
        # Display the year being searched for
        if lookup_year != None:
            print(f'\nLooking up {lookup_year}...\n')

        # Call the function to look for a movie from that year
            look_for_movies(lookup_year)

        # Ask the user if they want to try another year
        again = input('\nSearch another year (y/n)? ')
        if again != 'y': 
            print('\nThanks for using the Movie Year Lookup App. Bye.\n')
            break
        else:
            # Update log
            logging.debug('User elected to try again.') 
            continue

    # Close the cursor and database connection
    cursor.close()
    conn.close()
    
    # Update log
    logging.debug('Successfully: (1)closed database  (2)Closed cursor.') 
    logging.debug('>>>  Exiting app  <<<') 


if __name__ == "__main__":
    main()