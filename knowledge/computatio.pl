:- consult('knowledge/valorem.pl').

step_func(1, X) :- X > 0, !.
step_func(0, 0).

weight(H, X, Y, Z) :- step_func(A, X), step_func(B, Y), step_func(C, Z), H is A + B + C.

o_value_achieved(Line, Col, Value) :- o(Line, Col), value_at_position(Line, Col, Value), !.
o_value_achieved(_, _, 0).

x_value_achieved(Line, Col, Value) :- x(Line, Col), value_at_position(Line, Col, Value), !.
x_value_achieved(_, _, 0).

o_value_achieved_at_a_vertical_line(N, R, H) :-
    o_value_achieved(0, N, X),
    o_value_achieved(1, N, Y),
    o_value_achieved(2, N, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

x_value_achieved_at_a_vertical_line(N, R, H) :-
    x_value_achieved(0, N, X),
    x_value_achieved(1, N, Y),
    x_value_achieved(2, N, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 2) * S.

o_value_achieved_at_an_horizontal_line(N, R, H) :-
    o_value_achieved(N, 0, X),
    o_value_achieved(N, 1, Y),
    o_value_achieved(N, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

x_value_achieved_at_an_horizontal_line(N, R, H) :-
    x_value_achieved(N, 0, X),
    x_value_achieved(N, 1, Y),
    x_value_achieved(N, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 2) * S.

o_value_achieved_at_the_left_right_diagonal(R, H) :-
    o_value_achieved(0, 0, X),
    o_value_achieved(1, 1, Y),
    o_value_achieved(2, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

x_value_achieved_at_the_left_right_diagonal(R, H) :-
    x_value_achieved(0, 0, X),
    x_value_achieved(1, 1, Y),
    x_value_achieved(2, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 2) * S.

o_value_achieved_at_the_right_left_diagonal(R, H) :-
    o_value_achieved(0, 2, X),
    o_value_achieved(1, 1, Y),
    o_value_achieved(2, 0, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

x_value_achieved_at_the_right_left_diagonal(R, H) :-
    x_value_achieved(0, 2, X),
    x_value_achieved(1, 1, Y),
    x_value_achieved(2, 0, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 2) * S.

best_vertical_point_to_play(N, L, C, Value) :-
    C is N,
    value_at_position(L, C, Value),
    not(o(L, C)),
    not(x(L, C)).

best_horizontal_point_to_play(N, L, C, Value) :-
    L is N,
    value_at_position(L, C, Value),
    not(o(L, C)),
    not(x(L, C)).

best_left_right_diagonal_point_to_play(L, C, Value) :-
    not(o(0, 0)),
    not(x(0, 0)),
    L is 0, C is 0,
    value_at_position(L, C, Value),
    !.

best_left_right_diagonal_point_to_play(L, C, Value) :-
    not(o(1, 1)),
    not(x(1, 1)),
    L is 1, C is 1,
    value_at_position(L, C, Value),
    !.

best_left_right_diagonal_point_to_play(L, C, Value) :-
    not(o(2, 2)),
    not(x(2, 2)),
    L is 2, C is 2,
    value_at_position(L, C, Value),
    !.

best_right_left_diagonal_point_to_play(L, C, Value) :-
    not(o(0, 2)),
    not(x(0, 2)),
    L is 0, C is 2,
    value_at_position(L, C, Value),
    !.

best_right_left_diagonal_point_to_play(L, C, Value) :-
    not(o(1, 1)),
    not(x(1, 1)),
    L is 1, C is 1,
    value_at_position(L, C, Value),
    !.

best_right_left_diagonal_point_to_play(L, C, Value) :-
    not(o(2, 0)),
    not(x(2, 0)),
    L is 2, C is 0,
    value_at_position(L, C, Value),
    !.
