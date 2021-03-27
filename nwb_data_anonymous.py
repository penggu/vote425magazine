zen_planner = dict(
    login=dict(
        title='Northwest Badminton Academy',
        url='https://northwestbadmintonacademy.sites.zenplanner.com/login.cfm',
        email='user@example.com',
        password='top_secret',
    ),
    bookings=dict(
        url='https://northwestbadmintonacademy.sites.zenplanner.com/calendar.cfm',
        users={'FirstName1 LastName1': 0, 'FirstName2 LastName2': 1, 'FirstName3 LastName3': 2},
        time_slots=dict(
            Monday=['8am'],
            Tuesday=['9am'],
            Sunday=['8pm', '9pm']
        ),
        slot_numbers={
            '8am': 2,  # start of day
            '9am': 3,
            '10am': 4,
            '11am': 5,

            '12pm': 6,
            '1pm': 7,
            '2pm': 8,
            '3pm': 9,
            '4pm': 10,

            '5pm': 11,
            '6pm': 12,
            '7pm': 13,
            '8pm': 14,
            '9pm': 15  # end of day
            },
    ),
)
