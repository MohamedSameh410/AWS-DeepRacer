# AdaptivePathOptimizer-Speed-V2
This model, **AdaptivePathOptimizer-Speed-V2**, is cloned from the previous model, **AdaptivePathOptimizer-Speed**. It enhances track alignment and speed control for improved performance.
## Action space
Encourage the model to be faster.
| Steering angle (°) | Speed (m/s) |
|-|-|
| -30.0 | 1.40 |
| -30.0 | 1.60 |
| -20.0 | 1.90 |
| -20.0 | 2.20 |
| -10.0 | 2.40 |
| -10.0 | 2.60 |
| 0.0 | 4.00 |
| 0.0 | 3.30 |
| 10.0 | 2.60 |
| 10.0 | 2.40 |
| 20.0 | 2.20 |
| 20.0 | 1.90 |
| 30.0 | 1.60 |
| 30.0 | 1.40 |

## Reward function
No Changes from the previous model.
```python
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

    # Waypoints data
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

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

    # Track direction alignment using waypoints
    wp1 = waypoints[closest_waypoints[0]]
    wp2 = waypoints[closest_waypoints[1]]

    track_direction = math.atan2(wp2[1] - wp1[1], wp2[0] - wp1[0]) * 180.0 / math.pi
    direction_diff = abs(track_direction - heading)

    # Normalize direction reward (similar to other rewards)
    direction_ratio = min(direction_diff / 30, 1)  # Normalize to 0-1 range
    direction_reward = 1 - math.sqrt(direction_ratio)  # Similar transformation

    # Adjust speed based on upcoming waypoints
    if direction_diff < 10:
        speed_bonus = speed / 4.0  # Encourage speed on straight paths
    else:
        speed_bonus = (4.0 - speed) / 4.0  # Encourage slowing down on turns

    # Combine rewards with weights
    reward = (2 * distance_reward + steering_reward + 2 * speed_reward +
              2 * progress_reward + 2 * direction_reward + speed_bonus) / 10

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward *= 0.5  # Allow minor track deviation

    if off_track:
        reward *= 0.5  # Strong penalty for completely going off track

    return float(reward)
```

## Hyperparameters 

| Hyperparameter | Value |
|-|-|
| Gradient descent batch size | 128 |
| Entropy | 0.01 |
| Discount factor | 0.999 |
| Loss type | Huber |
| Learning rate | 0.00001 |
| Episodes between each iteration | 18 |
| Number of epochs | 10 |

## Model Performance

### Training:
I trained the model with a maximum time of 45 minutes.

### Results:
This model obtained the following performance:
| Best lab time | Total time | Off-track |
|-|-|-|
| 00:08.602 | 00:27.259 | 0 |
