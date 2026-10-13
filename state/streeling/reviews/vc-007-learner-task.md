# VC-007 learner transfer task

Give this page to a learner without the review brief or course answer blocks. There is no recorded attempt yet.

## New sample

A simplified plain-weave program has a 3-warp by 2-weft base tile. Repeat it twice horizontally and twice vertically. At global crossing `(x, y)`, warp is above weft when `(x + y) % 2 == 0`; otherwise weft is above warp. An alternate compiler instead restarts parity at each tile using `(x % 3 + y % 2) % 2`. Each crossing has a global ID `w<x>-f<y>`. A future Godot scene would render the compiled crossings, but no scene or screenshot is supplied here.

1. Give the final warp and weft counts, total crossings, and the first row's over/under sequence under global parity.
2. Find one adjacent pair at a tile seam where the restarted compiler differs from global parity. Count horizontal and vertical seam violations across the complete sample, and explain your count.
3. Specify the minimum fields you would keep in a manifest so a Godot import can be checked against the source program. Explain why crossing IDs should remain stable.
4. Describe one semantic check, one geometry check, and one perception check for a future scene. Which of these can you perform from the supplied equations alone?
5. Compare a woven 3D scene with a labeled 2D grid for a learner who must identify the thread above a target crossing. State one result that would make you reject or revise the 3D scene even if it looked attractive.

Record your reasoning and any uncertainty. No rendering expertise or real weaving experience is assumed.
