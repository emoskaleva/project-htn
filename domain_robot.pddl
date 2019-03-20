    (define (domain robot)
    (:requirements :typing :hierachie)
    (:types
        Package
        Room
        Room_door
        Robot
    )
    (:predicates
        (armempty ?rob)
        (r_in_room ?rob - Robot ?loc - Room)
        (holding ?rob - Robot ?obj - Package)
        (in ?obj - Package ?loc - Room)
        (closed ?d - Room_door)
        (door ?loc1 - Room ?loc2 - Room ?d - Room_door)
    )

    (:action pick_up
        :parameters (?obj - Package  ?rob - Robot  ?loc - Room  )
        :precondition
            (and
                (armempty ?rob)
                (not (holding ?rob ?obj))
                (r_in_room ?rob ?loc)
            )
        :effect
            (and
                (not (armempty ?rob))
                (holding ?rob ?obj)
                (r_in_room ?rob ?loc)
            )
    )

    (:action put_down
        :parameters (?obj - Package  ?rob - Robot  ?loc - Room  )
        :precondition
            (and
                (not (armempty ?rob))
                (holding ?rob ?obj)
                (r_in_room ?rob ?loc)
            )
        :effect
            (and
                (not (holding ?rob ?obj))
                (armempty ?rob)
                (r_in_room ?rob ?loc)

            )
    )

    (:action open
        :parameters (?rob - Robot  ?loc1 - Room  ?loc2 - Room  ?d - Room_door  )
        :precondition
            (and
                (r_in_room ?rob ?loc1)
                (door ?loc1 ?loc2 ?d)
                (closed ?d)
            )
        :effect
            (and
                (not (closed ?d))
                (r_in_room ?rob ?loc1)
                (door ?loc1 ?loc2 ?d)
            )
    )

    (:action move
        :parameters (?rob - Robot  ?loc1 - Room  ?loc2 - Room  ?d - Room_door  )
        :precondition
            (and
                (r_in_room ?rob ?loc1)
                (not (r_in_room ?rob ?loc2))
                (door ?loc1 ?loc2 ?d)
                (not (closed ?d))
            )
        :effect
            (and
                (r_in_room ?rob ?loc2)
                (not (r_in_room ?rob ?loc1))
                (not (closed ?d))
                (door ?loc2 ?loc1 ?d)
            )
    )

    (:task come_w_pack
        :parameters (?loc1 ?loc2 ?d ?rob ?obj)
    )


    (:task move_w_pack
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door ?rob - Robot ?obj - Package)
    )

    (:task come_back
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door ?rob - Robot ?obj - Package)
    )

    (:task move_in
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door ?rob - Robot)
    )


    (:method open_and_move_to_loc2
        :parameters (?rob - Robot  ?loc1 - Room  ?loc2 - Room  ?d - Room_door  )
        :task(move_in ?loc1 ?loc2 ?d ?rob)
        :precondition
            (and
                (r_in_room ?rob ?loc1)
                (door ?loc1 ?loc2 ?d)
                (closed ?d)
                (not (r_in_room ?rob ?loc2))
            )
        :subtasks
		    (and
		        (task0 (open ?loc1 ?loc2 ?d ?rob))
		        (task1 (move ?loc1 ?loc2 ?d ?rob))
		    )
		:ordering
		    (and
			    (task0 < task1)
		    )
    )

    (:method move_with_package_without_door
        :parameters (?obj - Package  ?rob - Robot  ?loc1 - Room  ?loc2 - Room  ?d - Room_door  )
        :task(move_w_pack ?loc1 ?loc2 ?d ?rob ?obj)
        :precondition
            (and
                (armempty ?rob)
                (not (holding ?rob ?obj))
                (r_in_room ?rob ?loc1)
                (not (r_in_room ?rob ?loc2))
                (not (closed ?d))
                (door ?loc1 ?loc2 ?d)
            )
        :subtasks
		    (and
		        (task0 (pick_up ?obj ?rob ?loc1))
		        (task1 (move ?rob ?loc1 ?loc2 ?d))
		        (task2 (put_down ?obj ?rob ?loc2))
		    )
		:ordering
		    (and
			    (task0 < task1)
			    (task1 < task2)
		    )
    )

        (:method move_with_package_with_door
        :parameters (?obj - Package  ?rob - Robot  ?loc1 - Room  ?loc2 - Room  ?d - Room_door  )
        :task(move_w_pack ?loc1 ?loc2 ?d ?rob ?obj)
        :precondition
            (and
                (armempty ?rob)
                (not (holding ?rob ?obj))
                (r_in_room ?rob ?loc1)
                (not (r_in_room ?rob ?loc2))
                (closed ?d)
                (door ?loc1 ?loc2 ?d)
            )
        :subtasks
		    (and
		        (task0 (open ?loc1 ?loc2 ?d ?rob))
		        (task1 (pick_up ?obj ?rob ?loc1))
		        (task2 (move ?rob ?loc1 ?loc2 ?d))
		        (task3 (put_down ?obj ?rob ?loc2))
		    )
		:ordering
		    (and
			    (task0 < task1)
			    (task1 < task2)
		    )
    )

    (:method come_back_with_package
        :parameters (?obj - Package  ?rob - Robot  ?loc1 - Room  ?loc2 - Room  ?d - Room_door  )
        :task(come_w_pack ?loc1 ?loc2 ?d ?rob ?obj)
        :precondition
            (and
                (armempty ?rob)
                (closed ?d)
                (not (holding ?rob ?obj))
                (r_in_room ?rob ?loc1)
                (not (r_in_room ?rob ?loc2))
                (door ?loc1 ?loc2 ?d)
            )
        :subtasks
		    (and
		        (task0 (open ?loc1 ?loc2 ?d ?rob))
		        (task1 (move ?loc1 ?loc2 ?d ?rob))
		        (task2 (pick_up ?obj ?rob ?loc2))
		        (task3 (move ?loc2 ?loc1 ?d ?rob))
		    )
		:ordering
		    (and
			    (task0 < task1)
			    (task1 < task2)
			    (task2 < task3)
		    )
    )

    (:method come_back_w
        :parameters (?obj - Package  ?rob - Robot  ?loc1 - Room  ?loc2 - Room  ?d - Room_door  )
        :task(come_back ?loc1 ?loc2 ?d ?rob ?obj)
        :precondition
            (and
                (armempty ?rob)
                (closed ?d)
                (not (holding ?rob ?obj))
                (r_in_room ?rob ?loc1)
                (not (r_in_room ?rob ?loc2))
                (door ?loc1 ?loc2 ?d)
            )
        :subtasks
		    (and
		        (task0 move_w_pack ?loc1 ?loc2 ?d ?rob ?obj)
		        (task1 (move ?loc2 ?loc1 ?d ?rob))
		    )
		:ordering
		    (and
			    (task0 < task1)
			    (task1 < task2)
			    (task2 < task3)
		    )
    )


    )




