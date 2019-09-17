#!/usr/bin/python
# -*- coding: utf-8 -*-

"""assignment2.py: IS 211 Assignment 2."""

__author__ = 'Adam Volin'
__email__ = 'Adam.Volin56@spsmail.cuny.edu'

import sys
import argparse
import datetime
import logging
import urllib.request as request
import urllib.error
import csv


def downloadData(url):
    """Accepts a URL as a string and opens it.

    Parameters:
        url (string): the url to be opened

    Example:
        >>> downloadData(
            'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv')
    """

    response = request.urlopen(url)
    return response.read().decode('utf-8').splitlines()

def processData(data):
    """Processes data from the contents of a CSV file line by line.

    Parameters:
        data - the contents of the CSV file

    Returns:
        dict: A dictionary mapping a person ID to a tuple with
              a format of (name, birthdate)

    Example:
        >>> processData(downloadedData)
    """

    people = {}
    logger = logging.getLogger('assignment2')

    for (line, col) in enumerate(csv.reader(data)):
        try:
            people[col[0]] = (col[1],
                              datetime.datetime.strptime(col[2],
                              '%d/%m/%Y').date())
        except:
            logger.error('Error processing line #{} for ID #{}'.format(line,
                         col[0]))

    return people


def displayPerson(id, personData):
    """Displays a person's information

    Parameters:
        id (int): A user's ID
        personData (dict): The dictionary containing member information

    Example:
        >>> displayPerson(1, peopleData)
        'Person #1 is John Smith with a birthday of 2019-09-09'
    """

    id = str(id)

    if id not in personData.keys():
        print('No user found with that id')
    else:
        print('Person #{} is {} with a birthday of {}'.format(id,
                personData[id][0], personData[id][1].strftime('%Y-%m-%d'
                )))


def main():
    """The function that runs when the program is executed."""

    parser = argparse.ArgumentParser()
    parser.add_argument('--url',
                        help='The URL of the CSV file to download and parse.'
                        )
    args = parser.parse_args()
    logging.basicConfig(filename='errors.log', level=logging.ERROR)

    if args.url:
        try:
            csvData = downloadData(args.url)
        except (urllib.error.URLError, urllib.error.HTTPError):
            print('There was an error retrieving the data from the provided URL. Please try a different URL.')
            sys.exit()

        personData = processData(csvData)

        try:
            id = int(input('Enter a user ID: '))
            if id <= 0:
                print('Received entry of a number <= 0. Exiting program.')
                sys.exit()
            else:
                displayPerson(id, personData)
                main()
        except ValueError:
            print('Please enter a valid numerical user ID')
            main()
    else:
        print('The --url parameter is required.')
        sys.exit()


if __name__ == '__main__':
    main()