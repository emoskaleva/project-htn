(define (problem test1)
        (:domain robot)

    (:objects
        r - Robot
        obj1 - Package
        obj2 - Package
        loc1 - Room
        loc2 - Room
        loc3 - Room
        d - Room_door
    )

    (:init
    (armempty ?r)
    (not (closed ?d))
    (not (holding ?r ?obj1))
    (r_in_room ?r ?loc1)
    (not (r_in_room ?r ?loc2))
    (door ?loc1 ?loc2 ?d)
    )

    (:goal
        (come_back ?loc1 ?loc2 ?d ?r ?obj1)
    )
)
