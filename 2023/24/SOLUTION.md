The second part of this problem admits a purely geometric solution. Because we
need to find a starting point and a velocity vector, we have a total of 6
unknowns. The two vectors we are after must satisfy the equations

$$\begin{align*}
\mathbf{r} + t_1\mathbf{v} &= \mathbf{r}_1 + t_1\mathbf{v}_1 \\
\mathbf{r} + t_2\mathbf{v} &= \mathbf{r}_2 + t_2\mathbf{v}_2 \\
&\vdots \\
\mathbf{r} + t_n\mathbf{v} &= \mathbf{r}_n + t_n\mathbf{v}_n \\
\end{align*}$$

Every vector equation gives us three scalar equations, _but_ intrduces a new
unknown, i.e. the time $t_i$. Effectively, every new equation reduces the number
of degrees of freedom by 2. Since we started with 6 degrees of freedom, we see
that we need exactly 3 _independent_ equations to solve the problem. Therefore,
it is enough to consider only 3 hailstones with independent velocity vectors.
Let us assume that we have found 3 hailstones for which
$\mathbf{v_1}\cdot(\mathbf{v_2}\times\mathbf{v_3})\neq 0$. The three vector
equations that we have to solve are not linear, so they are not trivial to
solve. However, we can just rely on geometric considerations to find the
solution. The first step is to rewrite the equations to isolate $\mathbf{r}$:

$$\begin{align*}
\mathbf{r} &= \mathbf{r}_1 + t_1(\mathbf{v}_1-\mathbf{v}) \\
\mathbf{r} &= \mathbf{r}_2 + t_2(\mathbf{v}_2-\mathbf{v}) \\
\mathbf{r} &= \mathbf{r}_3 + t_3(\mathbf{v}_3-\mathbf{v}) \\
\end{align*}$$

We now have the equivalent problem of finding lines with direction vector
$\mathbf{v}_i-\mathbf{v}$ that pass through the same point $\mathbf{r}$. So,
once we find $\mathbf v$, we can solve for the intersection of any of two lines
from the three above, compute $\mathbf r$ and use its component to find the
solution to the problem.

So the next step now is to find $\mathbf v$. We can do so by imposing the
condition that the three lines have mutual intersections. This can happen if
their distance is zero. In 3D space, the formula for the distance between two
lines of the form $\mathbf r_1 + t\mathbf v_1$ and $\mathbf r_2 + s\mathbf v_2$
is

$$|(\mathbf r_1-\mathbf r_2)\cdot(\mathbf v_1\times\mathbf v_2)|$$

Therefore, one of the conditions on the vector $\mathbf v$ from our problem is

$$(\mathbf r_2 - \mathbf r_1)
    \cdot[(\mathbf v_1-\mathbf v)\times(\mathbf v_2-\mathbf v)] = 0$$

and similarly for the other two combinations of lines. This is a linear equation
in $\mathbf v$, which can be brought in the equivalent form

$$\mathbf v\cdot[(\mathbf r_2-\mathbf r_1)\times(\mathbf v_2-\mathbf v_1)]
    =(\mathbf r_2-\mathbf r_1)\cdot(\mathbf v_2\times\mathbf v_1)$$

by means of basic vector identities. We now set

$$\begin{align*}
\mathbf m_1 &= (\mathbf r_3-\mathbf r_2)\times(\mathbf v_3-\mathbf v_2) \\
\mathbf m_2 &= (\mathbf r_1-\mathbf r_3)\times(\mathbf v_1-\mathbf v_3) \\
\mathbf m_3 &= (\mathbf r_2-\mathbf r_1)\times(\mathbf v_2-\mathbf v_1) \\
\end{align*}$$

and

$$\begin{align*}
a_1 &= (\mathbf r_3-\mathbf r_2)\cdot(\mathbf v_3\times\mathbf v_2) \\
a_2 &= (\mathbf r_1-\mathbf r_3)\cdot(\mathbf v_1\times\mathbf v_3) \\
a_3 &= (\mathbf r_2-\mathbf r_1)\cdot(\mathbf v_2\times\mathbf v_1) \\
\end{align*}$$

so that we can write the full system of equations as

$$\mathbf v\cdot\mathbf m_i = a_i$$

for $i=1,2,3$. If we denote by $M$ the matrix with rows given by the vectors
$\mathbf m_i$, we can write the system in matrix form as

$$M\mathbf v = \mathbf a$$

where $\mathbf a$ is the vector with components $a_i$. The inverse of the matrix
$M$ can be computed trivially as the matrix with columns given by the vectors

$$\frac{\mathbf m_2\times\mathbf m_3}{\mathbf m_1\cdot(\mathbf m_2\times\mathbf m_3)},
\frac{\mathbf m_3\times\mathbf m_1}{\mathbf m_1\cdot(\mathbf m_2\times\mathbf m_3)},
\frac{\mathbf m_1\times\mathbf m_2}{\mathbf m_1\cdot(\mathbf m_2\times\mathbf m_3)}.$$

Therefore, the vector $\mathbf v$ can now be computed as

$$\mathbf v = \frac{a_1\mathbf m_2\times\mathbf m_3+a_2\mathbf m_3\times\mathbf m_1+a_3\mathbf m_1\times\mathbf m_2}
{\mathbf m_1\cdot(\mathbf m_2\times\mathbf m_3)}$$

We can now use the intersection of the first two lines, that is the equation

$$\mathbf r_1 + t_1(\mathbf v_1 - \mathbf v) = \mathbf r_2 + t_2(\mathbf v_2 - \mathbf v)$$

to find the values of $t_1$ and $t_2$ (this is the solution to part one) and
then compute the intersection point, using e.g. the value of $t_1$ in the first
equation. Taking the sum of the three components of $\mathbf r$ thus computed
gives the answer to part two.
