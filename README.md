#Implementing Quine Mc'Clusky Algorithm by python programming language



Author : Kunjan Gevariya

Roll No. : 1903116



##Abstract
In this report approach of writing python program for implementation of Quine Mc'Clusky Algorithm is described along with the sample output. This algorithm is widely used in simplifying large boolean expressions. However it is advised that following approach should not be used when number of variables in boolean expression is very large.

Step by step approach
We will use following sample input:

Variables: ['A', 'B', 'C', 'D', 'E', 'F', 'G']

Minterms: [0, 2, 3, 5, 7, 8, 9, 10, 11, 13, 15]

Don't cares: [100, 121, 123, 124, 127]


##Step 1: Accepting input from user and validating problem instance :

In this step, we accept input from user and form 3 lists named var_names, minterms and dont_care. Then we validate problem instance. If any minterm or don't care is out of range (range is from 0 to 2^n-1 where n is total number of variables) or lists of minterms and don't cares are not sorted, then we throw error. If the problem instance is valid then we move onto next step where we divide minterms and don't cares in different groups.
 
##Step 2: Classifying minterms and don't cares according to ones in binary representation :
In this step we define class named Term which is initialized by number of variables and minterm or don't care. The object of class type Term has properties like was_combined (indicating if the term was combined from two terms), binary (binary representation of term), minterms_covered (minterms covered by a term). I have used format function to represent minterm in binary form. I have defined a function named find_prime_implicants in which I have classified all terms(minterms and dont cares) according to the number of 1's present in binary form in different groups. Group 0 contains terms with 0 1's, group 1 contains terms with 1 1's and so on. e.g group 0=m0 (0000000), group1= m2 (0000010), m8(0001000) etc.

##Step 3: Combing terms of adjacent groups and identifying prime implicants:

In this step we combine two terms of adjacent groups if they differ in only one bit in binary representation. To check if two terms can combine I have defined function named can_combine as property of class Term. We put '-' in binary form of combined term at the position of bit that differs. And we set the was_combined property of two terms to True. Combined term is obtained by function named combine which is property of class Term. At the end of this operation on all groups(we will call it pass), the terms that were not combined throughout the pass are appended to the list of prime implicants. e.g m0(0000000) will combine with m2(0000010) and form {m0,m2}(00000-0), m8(0001000) will combine with m10(0001010) and form {m8,m10}(00010-0), m100(1100100) will not combine with any term so it is prime implicant.

##Step 4: Further combining terms obtained from step 2:

We store the combined terms obtained from step 2 in the list named group_next. This will become input for another pass. For that we swap the lists group and group_next and then make group_next empty(so that it can store results of pass 2). We will combine two terms of adjacent groups only if they have '-' at the same position and they differ exactly in one bit. We set the bit that differs to '-' and was_combined property of two terms to True. And identify prime implicants just like step 3. e.g. {m0,m2}(00000-0) will combine with {m8,m10}(00010-0) and form {0,2,8,10} (000-0-0).
 
##Step 5: Repeating step 4 until no more combination is possible

We will repeat step 3 through while loop until no more terms can be combined. We will identify this scenario when we get an empty list as group_next at the end of the pass. In this case all terms in group will fall into prime implicants. After appending this terms to prime_implicants list we get final list of prime implicants.

##Step 6: Identifying essential prime implicants:

If a particular minterm is covered by only one prime implicant then that prime implicant is called essential prime implicant. I have defined a function named find_essential_prime_implicatns which iterate through every minterm and count how many prime implicants includes that minterm. If the count is 1 then that particular prime implicant is classified as essential prime implicant. Prime implicants that are not essential are stored in nonessential_prime_implicants. By replacing 1 with related variable and 0 with NOT of related variable we get essential and non-essential prime implicants in variable form.(Here the function print_implicant is doing this conversion in program.) e.g minterm m0 is covered by only {0,2,8,10} (000-0-0) prime implicant so it is classified as essential prime implicant and represented as A'B'C'E'G' in variable form.
Similarly A'B'C'EG is also essential prime implicant as m5 is covered by only this prime implicant.

##Step 7: Finding smallest subset of non essential prime implicant that covers remaining minterms:
The minterms that are not covered by essential prime implicants are stored in remaining_minterms list. Now we iterate through every subset(starts with 1 member subsets and then 2 members,3,4 and so on..) of non essential prime implicants and find minterms covered by the subset. If it includes all the remaining minterms then it is identified as smallest subset. If we find two such subsets then the set which has minimum number of literals in expansion is considered smallest subset.(This is achieved by function count_literal.) I have defined function named find_minset which do the above procedure. If we don't find smallest subset then it means that all minterms are covered by essential prime implicants. Here smallest set is {A'B'C'FG, A'B'C'DG} which covers remaining minterms {3,9,11} because {0,2,3,5,7,8,10,13,15} are covered by essential prime implicants which are A'B'C'E'G', A'B'C'EG.
 
##Conclusion
At the end of the whole program we get essential prime implicants and smallest set of non essential prime implicants that covers remaining minterms. By taking OR of every term of above two list we get simplified form of given boolean expression.
