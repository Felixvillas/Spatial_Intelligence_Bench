To find the sum of the two arrays:

1. **Sum of Zeros**: Locations with no circles in either array remain empty.
2. **One and Zero (or Zero and One)**: Blue circle in first array remains a blue circle if corresponding cell in second array is empty, and vice versa.
3. **One and One**: Blue circle in both arrays in the same position results in a white circle (two).

Let's go through the arrays:

- Top right corner: Blue + Blue = White
- Second row, rightmost: Blue + Empty = Blue
- Third row, third column: Blue + Empty = Blue
- First column, fifth row: Empty + Blue = Blue

All other locations either contain a red circle (ignored) or remain empty.

Based on this, the correct sum is:

**Choice 2**.