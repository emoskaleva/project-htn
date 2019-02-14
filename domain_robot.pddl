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
        (holding ?obj - Package ?rob - Robot)
        (in ?obj - Package ?loc - Room)
        (closed ?d - Room_door)
        (door ?loc1 - Room ?loc2 - Room ?d - Room_door)
    )

    (:action pick_up
        :parameters (?obj - Package ?rob - Robot, ?loc - Room)
        :precondition
            (and
                (armempty ?rob)
                (not (holding ?obj ?rob))
                (r_in_room ?rob ?loc)
                (in ?obj ?loc)
            )
        :effect
            (and
                (not (armempty ?rob))
                (not (in ?obj ?loc))
                (holding ?obj)
            )
    )

    (:action put_down
        :parameters (?obj - Package ?rob - Robot, ?loc - Room)
        :precondition
            (and
                (not (armempty))
                (holding ?obj)
                (not (in ?obj ?loc))
                (r_in_room ?rob ?loc)
            )
        :effect
            (and
                (not (holding ?obj))
                (armempty)
                (in ?obj ?loc)
            )
    )

    (:action open
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door, ?rob - Robot)
        :precondition
            (and
                (r_in_room ?rob ?loc1)
                (door ?loc1 ?loc2 ?d)
                (closed ?d)
            )
        :effect
            (and
                (not (closed ?d))
            )
    )

    (:action move
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door, ?rob - Robot)
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
            )
    )

    (:task move_w_pack_w_door
        :parameters (?loc1 ?loc2 ?d ?rob ?obj)
    )


    (:task move_w_pack
        :parameters (?loc1 - Room ?loc2 - Room ?rob - Robot, ?obj - Package)
    )

    (:task open_move
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door ?rob - Robot)
    )


    (:method open_and_move_to_loc2
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door, ?rob - Robot)
        :task(open_move ?loc1 ?loc2 ?d ?rob)
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
        :parameters (?loc1 - Room ?loc2 - Room ?rob - Robot, ?obj - Package)
        :task(move_w_pack_w_door ?loc1 ?loc2 ?rob ?obj)
        :subtasks
		    (and
		        (task0 (pick_up ?obj ?rob ?loc1))
		        (task1 (move ?loc1 ?loc2 ?d ?rob))
		        (task2 (put_down ?obj ?rob ?lock2))
		    )
		:ordering
		    (and
			    (task0 < task1)
			    (task1 < task2)
		    )
    )

    (:method come_back_with_package
        :parameters (?loc1 - Room ?loc2 - Room ?d - Room_door, ?rob - Robot, ?obj - Package)
        :task(move_w_pack ?loc1 ?loc2 ?d ?rob ?obj)
        :subtasks
		    (and
		        (task0 (move ?loc1 ?loc2 ?d ?rob))
		        (task1 (open ?loc1 ?loc2 ?d ?rob)
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




