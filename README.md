# Metagenome-Centric Algorithm
This project is still a work in progress yet an introduction is necessary.

## Goal of the Project
A central problem in analyzing an environment’s
sample of metagenomes is understanding a specific
gene’s abundance and importance within a sample without relying on unreliable heuristics. One common yet effective approach would be to
see if the gene’s coverage values surpass a benchmark that is found in other identified genes. For
example, a microbiologist could use a heatmap and
determine a gene’s abundance or role from the patterns in coverage values. Unfortunately, this method is susceptible to protean variables that can potentially undermine some of the intrinsic structure.

A machine learning, metgenome-centric classification algorithm that leverages the available data on what is "core" or not is an immediate solution to this problem. With _Anvi'o_, there is an established infrastructure with advanced visualization and analytical resources. In addition to these rich tools, _Anvi’o_ already utilizes a hierarchical
clustering algorithm that leverages a newick-tree format, and in a general sense, clusters related genes. Therefore, the algorithm should primarily focus on the gene’s data, as well as use anvio’s resources to organize and cluster the data.

Ideally, the algorithm should approximate a function that relies on a few inputs and outputs a single string. The outputs are still subject to debate because contemporary research has not yet established the
proper labels for classifying a gene; however, the
inputs should consist of the gene and its associated
coverage values. The name, or even gene itself, is
superfluous to the algorithm’s design, since the function essentially attempts to classify the gene based on its coverage values.

This algorithm should return key classifiers that categorize the gene as "core," "variable," "absent," or "non-specific." Moreover, the
coverage values within a metagenome (as opposed to
a gene) should be properly normalized so a sample’s
read counts are not misrepresented.

## Theory
To put this formally, let $G$ be the set of genes of size $n$, and $M$ be the set of metagenome samples of size $d$. Suppose $C_M$ $\subseteq$ $\mathbb{R}^d$ denotes the set of coverage values and $\Sigma$ is the set of desired, classified strings. Then the machine learning algorithm should be a well-defined function $f: G \times C_M \to \Sigma$ such that if $x_g \in C_M$ denotes the coverage values for a gene $g$, and $s_g \in \Sigma$ is the classified string of $g$, then $f(g, x_g)  =  s_g$
As mentioned before, some of the important strings in $\Sigma$ are "core," "variable," "absent," or "non-specific"; so we would expect $\{\text{"core"}, \text{"variable"}, \text{"absent"}, \text{"non-specific"}\} \subseteq \Sigma$. A key point of emphasis for $f$, however, is that the output is independent of the gene's name. For example, if $g_1 \in G$ and $g_2 \in G$ have the same coverage value $x \in C_M$, then $f(g_1, x) = f(g_2, x)$. Incorporating $g$ into $f$ is just for organizational purposes. 

