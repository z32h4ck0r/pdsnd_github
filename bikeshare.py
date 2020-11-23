import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():

	
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
	while True:
		city = input('Please choose one of the available cities (Chicago, New York City or Washington)\n').lower()
		if city in cities:
			break

    # get user input for month (all, january, february, ... , june)
	while True:
		month = input('Please choose one of the available months (January, February, March, May, June or All)\n').lower()
		if month in months or month == "all":
			break


    # get user input for day of week (all, monday, tuesday, ... sunday)
	while True:
		day = input('Please choose a day (e.g. Monday, Tuesday, ... , Sunday or All)\n').lower()
		if day in days or day == "all":
			break
	print('-'*40)
	return city, month, day


def load_data(city, month, day):
	"""
	Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
	"""
    # creating a dataframe with the chosen city
	df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
	df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
	df['month'] = df['Start Time'].dt.month
	df['day_of_week'] = df['Start Time'].dt.day_name()
	df['hour'] = df['Start Time'].dt.hour
	# filter by month if applicable
	if month != 'all':
		# use the index of the months list to get the corresponding int
		month = months.index(month) + 1
		# filter by month to create the new dataframe
		df = df[ df['month'] == month ]
	# if day is applicable
	if day != 'all':
		# filter by day of week to create the new dataframe
		df = df[ df['day_of_week'] == day.title()]


	return df


def time_stats(df):
	"""Displays statistics on the most frequent times of travel."""

	print('\nCalculating The Most Frequent Times of Travel...\n')
	start_time = time.time()

    # display the most common month
	print('The most common month is: ',df['month'].value_counts().idxmax())

    # display the most common day of week
	print('The most common day of week is: ',df['day_of_week'].value_counts().idxmax())

    # display the most common start hour
	print('The most commonn hour is: ',df['hour'].value_counts().idxmax())

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def station_stats(df):
	"""Displays statistics on the most popular stations and trip."""

	print('\nCalculating The Most Popular Stations and Trip...\n')
	start_time = time.time()

    # display most commonly used start station
	print('The most common start station is: ',df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
	print('The most common end station is: ',df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
	print('The most frequent combination of start and end: ',df.groupby(['Start Station','End Station']).size().idxmax())

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def trip_duration_stats(df):
	"""Displays statistics on the total and average trip duration."""

	print('\nCalculating Trip Duration...\n')
	start_time = time.time()

    # display total travel time
	print('The total travel time is: ',df['Trip Duration'].sum())

    # display mean travel time
	print('The total travel time is: ',df['Trip Duration'].mean())

	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def user_stats(df):
	"""Displays statistics on bikeshare users."""

	print('\nCalculating User Stats...\n')
	start_time = time.time()

    # Display counts of user types
	print('Counts of user type: ',df['User Type'].value_counts())
    # Display counts of gender and check if Gender is available
	if set(['Gender']).issubset(df.columns):
		print('Counts of gender: ',df['Gender'].value_counts())
	else:
		print('No "Gender" column in this dataset')
    # Display earliest, most recent, and most common year of birth and check if Birth Year is available
	if set(['Birth Year']).issubset(df.columns):
		print('The earliest birth year: ',df['Birth Year'].min())
		print('The most recent birth year: ',df['Birth Year'].max())
		print('The most common birth year: ',df['Birth Year'].value_counts().idxmax())
	else:
		print('No "Birth Year" column in this dataset')
	print("\nThis took %s seconds." % (time.time() - start_time))
	print('-'*40)


def raw_data(df):
	"""Display 5 rows of RAW data and for every "yes" 5 more."""
	rows = 5
	# Display the head (5 first rows) of dataframe
	ask_user = input('Would you like to view the first 5 rows of raw data for the city selected? Enter yes or no:\n').lower()
	if ask_user == 'yes':
		print(df.head())
		# Make it possible for the user to add 5 more rows as long as he wants.		
		while True:
			ask_user_more = input('Would you like to view 5 more rows of raw data for the city selected? Enter yes or no:\n').lower()
			if ask_user_more == 'yes': 
				print(df[rows:(rows+5)])
				rows += 5
			else:
				break

def main():
	while True:
		city, month, day = get_filters()
		df = load_data(city, month, day)

		time_stats(df)
		station_stats(df)
		trip_duration_stats(df)
		user_stats(df)
		raw_data(df)

		restart = input('\nWould you like to restart? Enter yes or no.\n')
		if restart.lower() != 'yes':
			break


if __name__ == "__main__":
	main()
