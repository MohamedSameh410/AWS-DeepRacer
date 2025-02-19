import math

def reward_function(params):
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    is_left_of_center = params['is_left_of_center']
    abs_steering = abs(params['steering_angle'])
    speed = params['speed']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    off_track = params['is_offtrack']

    # Calculate distance from the left edge
    if is_left_of_center:
        distance_from_left_side = (track_width / 2) - distance_from_center
    else:
        distance_from_left_side = (track_width / 2) + distance_from_center

    # Ensure non-negative values before applying sqrt
    distance_ratio = max(0, distance_from_left_side / track_width)
    distance_reward = 1 - math.sqrt(distance_ratio)

    steering_ratio = max(0, abs_steering / 30)
    steering_reward = 1 - math.sqrt(steering_ratio)

    speed_reward = (speed / 4.0) ** 2
    progress_reward = progress / 100

    # Combine rewards with weights
    reward = (2 * distance_reward + steering_reward + 2 * speed_reward + 2 * progress_reward) / 7

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward *= 0.5  # to allow going outside the track by sense :)

    # Penalize if the car goes off track
    if off_track:
        reward *= 0.5

    return float(reward)
