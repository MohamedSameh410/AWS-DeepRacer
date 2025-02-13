# EdgeAware-SpeedOptimized
**EdgeAware-SpeedOptimized** is a refined version of **CenterTrack-Stable**, designed to improve navigation efficiency. This model introduces edge awareness by rewarding the car for staying closer to the left side of the track rather than just the center. It promotes smoother turns by penalizing high steering angles and optimizes speed using a quadratic function to encourage faster movement while maintaining control. Additionally, it incorporates progress tracking to reward efficient lap completion and applies an adaptive off-track penalty, allowing minor deviations while discouraging excessive ones.

## Action space
This action space differs from the previous **CenterTrack-Stable** model by allowing higher speeds, especially on straight paths. The maximum speed has increased from 2.50 m/s to 3.40 m/s, emphasizing faster lap times. Minimum speeds at extreme steering angles (-30° and 30°) are slightly higher (0.90 m/s vs. 0.80 m/s) to maintain better momentum. This setup aligns with the **EdgeAware-SpeedOptimized** model’s focus on speed optimization while still ensuring control in turns.
| Steering angle (°) | Speed (m/s) |
|-|-|
| -30.0 | 0.90 |
| -30.0 | 1.10 |
| -20.0 | 1.40 |
| -20.0 | 1.60 |
| -10.0 | 1.80 |
| -10.0 | 2.00 |
| 0.0 | 3.40 |
| 0.0 | 2.80 |
| 10.0 | 2.00 |
| 10.0 | 1.80 |
| 20.0 | 1.60 |
| 20.0 | 1.40 |
| 30.0 | 1.10 |
| 30.0 | 0.90 |

## Reward function
The **EdgeAware-SpeedOptimized** reward function enhances **CenterTrack-Stable** by introducing edge awareness, rewarding progress, and optimizing speed using a quadratic function. It smooths steering penalties with square root scaling and applies an adaptive off-track penalty to allow minor deviations. These improvements promote both speed and control for more efficient lap completion.
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
        reward *= 0.3  # to allow going outside the track by sense :)

    return float(reward)
```

## Hyperparameters 
Reduced learning rate so that the optimization can happen close to the optimal point found by the base model.

| Hyperparameter | Value |
|-|-|
| Gradient descent batch size | 64 |
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
| 00:10.069 | 00:31.726 | 0 |

This model achieves superior speed, stability, and overall lap efficiency.
