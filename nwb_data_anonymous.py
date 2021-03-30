zen_planner = dict(
    login=dict(
        title='Northwest Badminton Academy',
        url='https://northwestbadmintonacademy.sites.zenplanner.com/login.cfm',
        email='user@example.com',
        password='top_secret',
    ),
    bookings=dict(
        url='https://northwestbadmintonacademy.sites.zenplanner.com/calendar.cfm',
        users={
            'FirstName1 LastName1': 0,
            'FirstName2 LastName2': 1,
            'FirstName3 LastName3': 2
        },
        time_slots=dict(
            Monday=['8am'],
            Tuesday=['9am'],
            Sunday=['8pm']
        ),
        slot_numbers=dict(
            Weekday={
                '2pm': 2, '3pm': 3, '4pm': 4,  # 2pm is start of day
                '5pm': 5, '6pm': 6, '7pm': 7, '8pm': 8, '9pm': 9, '10pm': 10  # 10pm is end of day
            },
            Weekend={
                '8am': 2, '9am': 3, '10am': 4, '11am': 5,  # 8am is start of day
                '12pm': 6, '1pm': 7, '2pm': 8, '3pm': 9, '4pm': 10,
                '5pm': 11, '6pm': 12, '7pm': 13, '8pm': 14, '9pm': 15, '10pm': 16  # 10pm is end of day
            },
        ),
    ),
)
