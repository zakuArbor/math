# Introduction

[insert title]

Have you ever wondered where the double angle formulas $\cos2\theta$ and $\sin2\theta$ you learned in Highschool comes from? It just randomly was introduced to you along with many other trig identities. 

[insert wiki, trig proof, and visual proof one after the other but in different angles]

Perhaps you have verified the double angle formula using other trig identities or seen some visual demonstration.

[blank]

[slowly fade in book or video of book recorded on phone with poor quality]

But if you were a normie like me, we never questioned where this formula comes from. My first encounter to the derivation of the formula came 7-8 years later from a novel called Math Girls that I randomly stumbled upon and its approach is an interesting one as well. The derivation is both simple and elegant but requires some exposure to linear algebra.

# Rotation

Here's a 2x2 matrix that represents the rotation of a 2d vector:

[insert rotation matrix]

To avoid the rabbit hole, take this fact face valued but to convince you, let's go over a quick example how to rotate a vector in a 2D plane.

Here we have a unit vector lying on the axis whose point is (1,0) and we wish to rotate the vector 
180 degree or pi radians counterclockwise to the point (-1,0).

[show rotation in graph]

The way to represent this rotating using matrices is the following:

[insert matrix multiplication]

And if we compute the matrix multiplication, we get that x = -1 and y = 0 as desired.

# What Does Rotation Have to Do with Double Angles

[insert double angles with 2\theta underlined or different text size or different colors]

Notice how the double angle formulas are rotating θ twice. How would one represent this using matrices? The simple way to rotate the matrix twice is to simply multiply the angle by 2 just like how the double angle formula does:

[insert 2 rotation matrix]

But there is also another way to rotate a matrix multiple times. One property of the rotation matrix is that a matrix multiplied by another matrix produces another rotation matrix. As the book puts it “Two rotations by θ are equivalent to squaring the matrix”

[insert rotation matrix squared]

[SHOULD I illustrate this, previously we rotated to pi but if we multiply by pi again, it goes to 2pi]

You rightfully are probably asking what does matrix rotation have to do with double angles? What is the purpose of showing these two representation of rotating a matrix twice.

Astute viewers may have noticed the matrix on right looks oddly similar to the double angles. If you realize this, good on you because if we equate both representation of the rotation matrix rotating twice together, we get the following:

[insert animation visualizing this]

where cos2\theta is equal to cos^2theta - sin^2theta and sin2theta is 2sintheta costheta

# Conclusion

So the next time you have trouble remembering the double angle formula, this is one simple way to derive the formula on the spot.