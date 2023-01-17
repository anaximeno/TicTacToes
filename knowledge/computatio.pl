% I will probably not remember what I made here though... :-)

:- consult('knowledge/valorem.pl').

h(1, X) :- X > 0, !.
h(0, 0).

weight(H, X, Y, Z) :- h(A, X), h(B, Y), h(C, Z), H is A + B + C.

praeventionis_cc_value(Line, Col, Value) :- o(Line, Col), value(Line, Col, Value), !.
praeventionis_cc_value(_, _, 0).

quaestum_cc_value(Line, Col, Value) :- x(Line, Col), value(Line, Col, Value), !.
quaestum_cc_value(_, _, 0).

praeventionis_rvline(N, R, H) :-
    praeventionis_cc_value(0, N, X),
    praeventionis_cc_value(1, N, Y),
    praeventionis_cc_value(2, N, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

quaestum_rvline(N, R, H) :-
    quaestum_cc_value(0, N, X),
    quaestum_cc_value(1, N, Y),
    quaestum_cc_value(2, N, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 1) * S.

praeventionis_rhline(N, R, H) :-
    praeventionis_cc_value(N, 0, X),
    praeventionis_cc_value(N, 1, Y),
    praeventionis_cc_value(N, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

quaestum_rhline(N, R, H) :-
    quaestum_cc_value(N, 0, X),
    quaestum_cc_value(N, 1, Y),
    quaestum_cc_value(N, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 1) * S.

praeventionis_rdline_l(R, H) :-
    praeventionis_cc_value(0, 0, X),
    praeventionis_cc_value(1, 1, Y),
    praeventionis_cc_value(2, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

quaestum_rdline_l(R, H) :-
    quaestum_cc_value(0, 0, X),
    quaestum_cc_value(1, 1, Y),
    quaestum_cc_value(2, 2, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 1) * S.

praeventionis_rdline_r(R, H) :-
    praeventionis_cc_value(0, 2, X),
    praeventionis_cc_value(1, 1, Y),
    praeventionis_cc_value(2, 0, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is R * S.

quaestum_rdline_r(R, H) :-
    quaestum_cc_value(0, 2, X),
    quaestum_cc_value(1, 1, Y),
    quaestum_cc_value(2, 0, Z),
    weight(S, X, Y, Z),
    R is X + Y + Z,
    H is (R + 1) * S.

compute_vert(N, L, C, Value) :-
    C is N,
    value(L, C, Value),
    not(o(L, C)),
    not(x(L, C)).

compute_horiz(N, L, C, Value) :-
    L is N,
    value(L, C, Value),
    not(o(L, C)),
    not(x(L, C)).

compute_diag_l(L, C, Value) :-
    not(o(0, 0)),
    not(x(0, 0)),
    L is 0, C is 0,
    value(L, C, Value),
    !.

compute_diag_l(L, C, Value) :-
    not(o(1, 1)),
    not(x(1, 1)),
    L is 1, C is 1,
    value(L, C, Value),
    !.

compute_diag_l(L, C, Value) :-
    not(o(2, 2)),
    not(x(2, 2)),
    L is 2, C is 2,
    value(L, C, Value),
    !.

compute_diag_r(L, C, Value) :-
    not(o(0, 2)),
    not(x(0, 2)),
    L is 0, C is 2,
    value(L, C, Value),
    !.

compute_diag_r(L, C, Value) :-
    not(o(1, 1)),
    not(x(1, 1)),
    L is 1, C is 1,
    value(L, C, Value),
    !.

compute_diag_r(L, C, Value) :-
    not(o(2, 0)),
    not(x(2, 0)),
    L is 2, C is 0,
    value(L, C, Value),
    !.