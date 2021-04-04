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
            'Firstname1 Lastname1': 0,
            'Firstname2 Lastname2': 1,
        },
        time_slots=dict(
            Monday=['8:00 am'],
            Tuesday=['9:00 am'],
            Sunday=['8:00 pm']
        ),
        slot_numbers=dict(
            Weekday={
                '2:00 pm': 2, '3:00 pm': 3, '4:00 pm': 4,  # 2:00 pm is start of day
                '5:00 pm': 5, '6:00 pm': 6, '7:00 pm': 7, '8:00 pm': 8, '9:00 pm': 9, '10:00 pm': 10  # 10:00 pm is end of day
            },
            Weekend={
                '8:00 am': 2, '9:00 am': 3, '10:00 am': 4, '11:00 am': 5,  # 8:00 am is start of day
                '12:00 pm': 6, '1:00 pm': 7, '2:00 pm': 8, '3:00 pm': 9, '4:00 pm': 10,
                '5:00 pm': 11, '6:00 pm': 12, '7:00 pm': 13, '8:00 pm': 14, '9:00 pm': 15, '10:00 pm': 16  # 10:00 pm is end of day
            },
        ),
    ),
)
