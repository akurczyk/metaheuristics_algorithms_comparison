from classes import State

states = [
    State('Alabama', 'Montgomery', 9),
    State('Alaska', 'Juneau', 3),
    State('Arizona', 'Phoenix', 11),
    State('Arkansas', 'Little Rock', 6),
    State('California', 'Sacramento', 55),
    State('Colorado', 'Denver', 9),
    State('Connecticut', 'Hartford', 7),
    State('D.C.', 'Washington', 3),
    State('Delaware', 'Dover', 3),
    State('Florida', 'Tallahassee', 29),
    State('Georgia', 'Atlanta', 16),
    State('Hawaii', 'Honolulu', 4),
    State('Idaho', 'Boise', 4),
    State('Illinois', 'Springfield', 20),
    State('Indiana', 'Indianapolis', 11),
    State('Iowa', 'Des Moines', 6),
    State('Kansas', 'Topeka', 6),
    State('Kentucky', 'Frankfort', 8),
    State('Louisiana', 'Baton Rouge', 8),
    State('Maine', 'Augusta', 4),
    State('Maryland', 'Annapolis', 10),
    State('Massachusetts', 'Boston', 11),
    State('Michigan', 'Lansing', 16),
    State('Minnesota', 'Saint Paul', 10),
    State('Mississippi', 'Jackson', 6),
    State('Missouri', 'Jefferson City', 10),
    State('Montana', 'Helena', 3),
    State('Nebraska', 'Lincoln', 5),
    State('Nevada', 'Carson City', 6),
    State('New Hampshire', 'Concord', 4),
    State('New Jersey', 'Trenton', 14),
    State('New Mexico', 'Santa Fe', 5),
    State('New York', 'Albany', 29),
    State('North Carolina', 'Raleigh', 15),
    State('North Dakota', 'Bismarck', 3),
    State('Ohio', 'Columbus', 18),
    State('Oklahoma', 'Oklahoma City', 7),
    State('Oregon', 'Salem', 7),
    State('Pennsylvania', 'Harrisburg', 20),
    State('Rhode Island', 'Providence', 4),
    State('South Carolina', 'Columbia', 9),
    State('South Dakota', 'Pierre', 3),
    State('Tennessee', 'Nashville', 11),
    State('Texas', 'Austin', 38),
    State('Utah', 'Salt Lake City', 6),
    State('Vermont', 'Montpelier', 3),
    State('Virginia', 'Richmond', 13),
    State('Washington', 'Olympia', 12),
    State('West Virginia', 'Charleston', 5),
    State('Wisconsin', 'Madison', 10),
    State('Wyoming', 'Cheyenne', 3),
]

#
# COORDINATES
#

print('Loading states capitals coordinates...')

for state in states:
    state.get_coordinates()

#
# SERIALIZING
#

print('Serializing and saving states to a binary file...')

State.save(states)
