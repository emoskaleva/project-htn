(define (problem test1)
        (:domain robot)

    (:objects
        r - Robot
        obj - Package
        loc1 loc2 - Room
        d - Room_door
    )

    (:init
        (armempty ?rob)
        (r_in_room ?rob - Robot ?loc1 - Room)
        (in ?obj - Package ?loc2 - Room)
        (door ?loc1 - Room ?loc2 - Room ?d - Room_door)

    )

    (:goal
        (come_back_with_package ?loc1 ?loc2 ?d ?r ?obj)
    )
)