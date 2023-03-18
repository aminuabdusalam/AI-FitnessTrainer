def get_calories_burned(exercise, body_weight, count):
    if exercise == "curls":
        MET_value, average_time = 3,2
    elif exercise == "squats":
        MET_value, average_time = 5.8, 3
    elif exercise == "pushups":
        MET_value, average_time = 8.0, 3

    duration = (average_time / 60) * count
    
    calories_burned = ((MET_value * 3.5 * body_weight)/200) * (duration)
    return calories_burned,duration 


calories_burned, duration = get_calories_burned('curls', 68, 13)

print(calories_burned)