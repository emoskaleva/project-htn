(define (problem test1)
        (:domain robot)

    (:objects
        r - Robot
        obj1 - Package
        loc1 - Room
        loc2 - Room
        loc3 - Room
        d - Room_door
    )

    (:init
        (armempty ?r)
        (not (holding ?r ?obj1))
        (r_in_room ?r ?loc2)
        (not (r_in_room ?r ?loc3))
        (closed ?d)
        (door ?loc2 ?loc3 ?d)
    )

    (:goal
        (come_back loc2 loc3 d r obj1)
    )
)
