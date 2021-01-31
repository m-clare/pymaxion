from pymaxion.constraints.cable import Cable
import pymaxion.helpers as helpers
from numpy import pi
from numpy import array
from numpy import double

# cable properties
E = 21000
A = 100 * pi
rest_length_taut = 0.5
rest_length_slack = 2.0

initial_positions = array([[0,0,0], [1, 0, 0]], dtype=double)
p_sum = array([[0, 0, 0], [0, 0, 0]], dtype=double)
w_sum = array([0, 0], dtype=double)

test_cable_taut = Cable(E, A, rest_length_taut, [0, 1])
test_cable_slack = Cable(E, A, rest_length_slack, [0, 1])

ppos = helpers.create_2d_mv(initial_positions)
pp_sum = helpers.create_2d_mv(p_sum)
strength = helpers.create_1d_mv(w_sum)
print(p_sum)
print(w_sum)

print(test_cable_taut.constraint_n_particles)
# test_cable_taut.pcalculate(ppos)
# test_cable_taut.p_sum_moves(pp_sum, strength)
# print(p_sum)
# print(w_sum)

test_cable_taut.py_calculate(ppos)
test_cable_slack.py_calculate(ppos)
# print(test_cable_taut.move_vectors)
# print(test_cable_taut.strength)
# print(test_cable_slack.move_vectors)
# print(test_cable_slack.strength)

