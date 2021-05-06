# ROS simulations for EchoSLAM

## What is EchoSLAM?

The goal of EchoSLAM is to use time-of-arrival measurements of acoustic pulses to aid in the relative localisation of a team of robots, while using the same acoustic transmitters to detect obstacles by analysing reflected echoes. Thus we plan to implement Simultaneous Localisation and Mapping (SLAM) solely using acoustic transceivers.

## Running the Code

We'll be testing our localisation algorithms in a ROS environment. 

To launch a sample simulation of n bots
* Clone this package into your workspace
* Build this package
* Source you current workspace in your working terminals
* Launch the `team.launch` with `n` bots using (assume `n` = 4)

  ```roslaunch echoslam_ROS team.launch teamsize:=4```
