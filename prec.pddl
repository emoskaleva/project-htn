:Name
move_2 loc1 loc2 d r obj1 obj2

:Init
armempty r
not closed d
not holding r obj1
not holding r obj2
r_in_room r loc1
not r_in_room r loc2
door loc1 loc2 d

:Effect
not holding r obj2
not r_in_room r loc2
not closed d
door loc1 loc2 d
not armempty r
holding r obj1
r_in_room r loc1



