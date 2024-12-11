**USER:** You are a sentient living creature capable navigating in mazes, planning, and spatial reasoning. You are playing a Pacman-style maze game. You start at some random position in the maze. You must escape the maze as quickly as possible to reach the goal. You are given the game screen that shows the following: 

* maze structure - black is obstacle space, blue is navigable space. You can only move on blue spaces. You cannot move through black spaces. 
* your current position - left up corner 
* goal position - right bottom corner

Below the screen, a status message might appear indicating that you collided into a wall after your previous action.
Actions available: You can take five possible actions. 

* left - move left from your current position by one step 
* right - move right from your current position by one step 
* up - move up from your current position by one step 
* down - move down from your current position by one step 
* stop - issue this action only after you have reached the goal position. If you execute it prematurely, you will fail. If you do not execute it after reaching the goal, you will again fail.

Response format: Respond in the following format.
<text explanation string - explain your reasoning concisely>
<next, provide a json formatted output with the next action>

```
{
    "action": "<action>"
}
```

**ASSISTANT:** ...
**USER:** Here is the current state of the maze.
<IMAGE OF MAZE>
Think step-by-step about how to reach the goal. What action do you take next?
**ASSISTANT:** ...
**USER:** Here is the current state of the maze.
<IMAGE OF MAZE>
Think step-by-step about how to reach the goal. What action do you take next?
.
.
.