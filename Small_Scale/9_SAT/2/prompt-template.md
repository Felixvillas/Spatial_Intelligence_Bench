You are playing the array addition game. You have to add two arrays by following certain rules. Each array location can be empty (i.e., fully white) or filled with colored circles. Empty locations represent zeros. The colors of the circles mean specific things. 

* Blue circle is a one 
* Red circle is a distrction and must be ignored (i.e., it does not contribute to the array addition) 
* White circle is a two

Array addition works as follows: 

* sum of zeros must be a zero (i.e., an empty array cell) 
* sum of one and zero (or zero and one) must be one (i.e., a blue circle) 
* sum of one and one must be two (i.e., a white circle)

Here is the first array.
<IMAGE OF ARRAY 1> 

Here is the second array.
<IMAGE OF ARRAY 2> 

What is the sum of the two arrays? Pick from one of these four choices.

Choice 1
<IMAGE OF CHOICE 1> 

Choice 2
<IMAGE OF CHOICE 2> 

Choice 3
<IMAGE OF CHOICE 3> 

Choice 4
<IMAGE OF CHOICE 4> 

Think step by step. Then answer your question in the following json format.

```
{
    "answer": <fill in one of 1/2/3/4 integer value>
}
```
