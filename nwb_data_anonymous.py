zen_planner = dict(
    login=dict(
        title='Northwest Badminton Academy',
        url='https://northwestbadmintonacademy.sites.zenplanner.com/login.cfm',
        email='user@example.com',
        password='top_secret',
    ),
    bookings=dict(
        action='reserve',  # either 'reserve' or 'cancel'
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
    ),
)
