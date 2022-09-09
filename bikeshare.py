import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter the name of the city you are looking for (chicago, new york city or washington)')
    city = city.lower()
    while city not in CITY_DATA:
        city = input('Invalid input! Please try again!')
        city = city.lower()

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Please enter the month (from januray to june, or all)')
    month = month.lower()
    while month not in months:
        month = input('Invalid input for month! Please try again!')
        month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Please enter the day of week (from monday to saturday, or all)')
    day = day.lower()
    while day not in days:
        day = input('Invalid input for day! Please try again!')
        day = day.lower()

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
    # Load data as dataframe using read_csv for specific city
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column using to_datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new DataFrame
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new DataFrame
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # First of all, we still need to convert Start Time column using to_datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # (1). display the most common month
    # Extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # Find the most popular month (index from 1 to 12)
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Popular Month: ', months[popular_month - 1])  # Remember to -1

    # (2). display the most common day of week
    # Extract day of week from the Start Time column to create a day_of_week column
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    # Find the most popular day of week (index from 0 to 6)
    popular_day_of_week = df['day_of_week'].mode()[0]
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('Most Popular Day of Week: ', days_of_week[popular_day_of_week])


    # (3). display the most common start hour
    # Extract hour from Start Time column to create a hour column
    df['hour'] = df['Start Time'].dt.hour
    # Find the most popular hour (index from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print('Most Popular hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # (1). display most commonly used start station
    print('Most Popular Start Station: ', df['Start Station'].mode()[0])

    # (2). display most commonly used end station
    print('Most Popular End Station: ', df['End Station'].mode()[0])

    # (3). display most frequent combination of start station and end station trip
    print('Most Frequent Combination of Start Station and End Station: ', \
          df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # (1). display total travel time
    print('Total Travel Time: ', df['Trip Duration'].sum())

    # (2). display mean travel time
    print('Mean Travel Time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # (1). Display counts of user types
    print('The Count of User types: ', df['User Type'].value_counts())

    # (2). Display counts of gender
    if 'Gender'  in df.columns:
        print('The Count of Gender', df['Gender'].value_counts())
    else:
        print('No Gender column in current dataframe')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', df['Birth Year'].min())
        print('Most Recent year of Birth:', df['Birth Year'].max())
        print('Most Common year of Birth:', df['Birth Year'].mode()[0])
    else:
        print('No Birth Year column in current dataframe')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # After those four functions above, prompt user whether they would like
        # to see the raw data
        enter = ['yes', 'no']
        user_input = input('Would you like to see raw data? (yes, or no)')
        while user_input.lower() not in enter:
            user_input = input('Wrong input! Please enter yes or no')
            user_input = user_input.lower()

        # Pointer for the "position" of raw data
        i = 0
        while True:
            if user_input.lower() == 'yes':
                print(df.iloc[i : (i + 5)])
                i = i + 5
                user_input = input('Would you like to continue to see raw data? (yes, or no)')
                while user_input.lower() not in enter:
                    user_input = input('Wrong input! Please enter yes or no')
                    user_input = user_input.lower()
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
