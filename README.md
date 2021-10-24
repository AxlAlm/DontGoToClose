# DontGoToClose

DontGoToClose is a tiny little project to visualize path finding algorithms in a setting where the vicinity to an obstacle increase the cost of the path.

For example, take the following problem:

<img src="docs/example1.png" width="400" />

Obviously, the shortest path would be straight through the middle tunnel. However, if we add to the problem a penalty on paths close to obstacles our problem changes. Below we can see these penalties visualized ( darker red meaning more penalty)

<img src="docs/example1_2.png" width="400" />

If we then run the an algorithm to find the shortest path we can see that, given the right penalty, the shortest path will not be between the tunnel!

<img src="docs/example1.gif" width="400" />

We might find problems like this in various areas. For example when we want to navigate through a crowded area with a car, or chose the fastest path to a location given that some roads have different speed limits, traffic jams or whatever, or in a game where we would want our AI to avoid enemies!


# How to run

Note! Currently, there is only support for example1 map and Djikstra algorithm

    python run.py -map example1 -max_distance 5 -show_distance -penalty_cost 5 -algo Djikstra


# Example on a random generated map:

    python run.py -map random -random_seed 9999


<img src="docs/random_map.gif" width="400" />



## TODO

- fix so that start and goal is not "locked" in when generating a random map
- add A*
