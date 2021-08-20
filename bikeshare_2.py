import time
import numpy as np
import pandas as pd
import datetime as dt


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months=("January","February","March","April","May","June")
days=("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday", "Sunday","All")



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid input
    listCity = str(CITY_DATA.keys())
    inCity=input("Which cities do you like to see ?  (available : "+ listCity + ")" ).lower()
    if inCity not in CITY_DATA:
        print("Wrong Input \n Lets start again! \n\n\n")
        main()

    # get user input for month (all, january, february, ... , june)
    listMonth = str(months)
    inMonth=input("Which months do you like to see ?  (available : "+ listMonth + ")" ).title()

    if inMonth not in months:
        print("Wrong Input \n Lets start again! \n\n\n")
        main()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    listDay = str(days)
    inDay=input("Which Day do you like to see ? Type 'all' for all!  (available : "+ listDay + ")" ).title()

    if inDay not in days:
        print("Wrong Input \n Lets start again! \n\n\n")
        main()


    filterSummary = input("You chose the following filter: \n city: "+inCity+"\n month: " + inMonth + "\n day: " + inDay +"\n Is that correct yes / no " )

    if filterSummary != "yes":
        exit()

    print('-'*40)
    return inCity, inMonth, inDay


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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # add months
    df['Month'] = df['Start Time'].dt.month_name()
    # add day
    df['Day'] = df['Start Time'].dt.day_name()
    # add Start Hour
    df['Start Hour'] = df['Start Time'].dt.hour
    # add Start End combinaton
    df['Start-End'] = (df['Start Station'] + ' - ' + df['End Station'])
    # apply filters
    df = df[df['Month'] == month.title()]
    if day == "all":
        df = df[df['Day'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print("Most common month is: " +
          most_common_month)

    # display the most common day of week
    most_common_day = df['Day'].mode()[0]
    print("Most common day is: " +
          most_common_day)

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print("Most common start hour is: " +
          str(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("Most common start station is: " +
          most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("Most common end statio is: " +
          most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end = str(df['Start-End'].mode()[0])
    print("Most common start-end combination :"
           + most_common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         " days " +
                         str(int((total_travel_time % 86400)//3600)) +
                         " hours " +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         " minutes " +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         " sesconds")
    print("Total travel time is : " +total_travel_time )

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//86400)) +
                         " days " +
                         str(int((mean_travel_time % 86400)//3600)) +
                         " hours " +
                         str(int(((mean_travel_time % 86400) % 3600)//60)) +
                         " minutes " +
                         str(int(((mean_travel_time % 86400) % 3600) % 60)) +
                         " sesconds")
    print("Mean travel time is : " +mean_travel_time )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts().to_string()
    print("Count user types: ")
    print(user_types)


    # Display counts of gender
    try:
        count_gender = df["Gender"].value_counts().to_string()
        print("\nGender Count:")
        print(count_gender)
    except KeyError:
        print("No gender data for your city selection")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_by = str(int(df['Birth Year'].min()))
        print("\nEarliest year of birth: " + earliest_by)
        most_recent_by = str(int(df['Birth Year'].max()))
        print("Most recent year of birth: " + most_recent_by)
        most_common_by = str(int(df['Birth Year'].mode()[0]))
        print("Most common year of birth " + most_common_by)
    except:
        print("No birthday data for your selection")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def showData(df):
    inShowData = input("Do you want to see first 5 rows of data?").lower()
    i = 5
    while inShowData == "yes":
        print(df.head(i))
        i = i + 5
        inShowData = input("Do you want to see 5 more ?").lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        showData(df)

        time_stats(df)
        print("===================================")
        station_stats(df)
        print("===================================")
        trip_duration_stats(df)
        print("===================================")
        user_stats(df)
        print("===================================")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
