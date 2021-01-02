print("Enter variables names seperated by space : ",end='')
var_names=input().split()
print("Enter minterms seperated by space : ",end='')
minterms=list(map(lambda x:int(x),input().split()))
print("Enter don't cares seperated by space : ",end='')
dont_cares=list(map(lambda x:int(x),input().split()))
n=len(var_names)

print("Checking problem instance....")
def check_problem_instance(N,minterms,dont_cares):
    # A function to check if the minterms and dont_cares lists are valid
    # The list should have no duplicates, be in ascending order,
    # and each entry should be between 0 and 2^N -1.
    print("Problem Instance:")
    print("---------------------------")
    print("Variables:",var_names)
    print("Minterms:",minterms)
    print("Don't cares:",dont_cares)
    print("---------------------------")
    print("Checking problem instance...",end='')
    m1 = [x for x in sorted(set(minterms)) if (x>=0 and x<(2**N))]
    d1 = [x for x in sorted(set(dont_cares)) if (x>=0 and x<(2**N))]
    assert(minterms == m1), "ERROR: The minterm list is Invalid."
    assert(dont_cares == d1), "ERROR: The dont_cares list is invalid."
    assert (not (set(minterms)&set(dont_cares))), "ERROR: The minterms list and dont_cares list have some common elements."
    print("OK.")
check_problem_instance(n,minterms,dont_cares)
print()

def binary(x,n):
    # convert x to binary (a list of 0s and 1s)
    # Example: convert_to_binary(6,5) returns [0,0,1,1,0]
    return list(format(x,'0'+str(n)+'b'))

import copy
class Term(object):
    """
    A class to model each term in the QM algorithm.
    A term can be a minterm (eg. [1,0,1,1,])
    or a combined term (eg. [1,0,1,'-'])
    """
    # Initializing a Term from a minterm (integer)
    def __init__(self,n,minterm):
        self.n=n
        self.minterms_covered=set([minterm])    # the set of minterms that are covered by this term
        self.binary=binary(minterm,n)           # the binary representation of a term. Eg. ['0','0','1','-']
        self.was_combined=False                 # a boolean variable indicating whether this Term was combined.

    #Function that check if two terms can combine
    #Return True if possible else return Falsw
    def can_combine(self,other):
        sbinary=self.binary
        obinary=other.binary
        count=0
        
        for i in range(self.n):
            if (sbinary[i]=='-' and obinary[i]!='-') or (sbinary[i]!='-' and obinary[i]=='-'):
                return False       # can't be combined as the '-' term is not matching

            if sbinary[i]!=obinary[i]:
                count+=1
            if count>1:             
                return False       # Cannot combine as more than two charcters in binary representation differ
        return True
    
    #Function that combine two terms
    def combine(self,other):
        combined_term=copy.deepcopy(self)
        n=self.n
        sbinary=self.binary
        obinary=other.binary

        for i in range(n):
            if sbinary[i]!=obinary[i]:
                combined_term.binary[i]='-'
        
        self.was_combined=True
        other.was_combined=True
        combined_term.was_combined=False
        combined_term.minterms_covered=self.minterms_covered.union(other.minterms_covered)

        return combined_term

# here's the main routine to find all prime implicants:
def find_prime_implicants(minterms,dont_cares,n):
    # we finally need to populate this list of prime implicants
    prime_implicants=[]
    
    # First, lets create a list group where we shall store the terms, grouped on the basis of number of 1s contained in the term.
    group=[[] for _ in range(n+1)]
    #group[0] should contain all terms with no '1',
    #group[1] should contain terms with exactly one '1'
    #group[2] should contain terms with exactly two '1's
    #and so on...
    
    for i in minterms+dont_cares:
        x=Term(n,i)
        count1=x.binary.count('1')
        group[count1].append(x)

    #Function that prints this group
    def print_group(group):
        gno=0
        for i in group:
            print("Group "+str(gno)+" ----------------")
            for j in i:
                if j.was_combined:
                    print(str(j.minterms_covered)+"  "+str(list(j.binary))+u'\u2713')
                else:
                    print(str(j.minterms_covered)+"  "+str(list(j.binary)))
            gno+=1
        print()

    print("Grouping the minterms and don't care terms based on the number of ones:")
    print_group(group)
    print()
    print("Combining terms in adjacent groups...")
    
    # similarly, lets have another list for storing the results of one pass, serving as input to the next pass
    group_next=[[] for _ in range(n+1)]
    
    #One pass
    n_iter=0
    converged=False
    
    #This loop will try combining terms of adjacent groups and identify prime implicants at the end of each pass 
    #until no more terms can be combined.
    while(not converged):
        n_iter+=1
        print("\n================================\nPass{n}\n================================".format(n=n_iter))
        
        for i in range(n):      #iterate over each group
            g1=group[i]
            g2=group[i+1]
            for j in g1:        #iterate over each element of group
                for k in g2:        #iterate over each element of next group
                    if j.can_combine(k):
                        combined=j.combine(k)
                        allowed=True
                        for t in group_next[i]:     #check if we are not adding same term again
                            if combined.minterms_covered==t.minterms_covered:
                                allowed=False
                        if allowed:
                            group_next[i].append(combined)
        
        
        print_group(group)
        
        empty=True
        for i in group_next:        #check if group_next is empty.
                if len(i)!=0:
                    empty=False
                    break
        if empty:                   #if group_next is empty that means no terms can combine togather 
            converged=True
            for i in group:         #As no more terms can combine, terms remaining in group are all prime implicants.
                for j in i:         
                    prime_implicants.append(j)
        else:
            for i in group:
                for j in i:
                    if not j.was_combined:      #if the term was not combined then it will be identified as prime implicant.
                        prime_implicants.append(j)

        print("Prime implicants identified by the end of this pass:")
        for i in prime_implicants:
            print(str(i.minterms_covered)+"  "+str(i.binary))    
        
        group,group_next=group_next,group       #swap group and group_next
        group_next=[[] for i in range(n+1)]     #making group_next empty
    
    return prime_implicants

prime_implicants=find_prime_implicants(minterms,dont_cares,n)

#Function that print prime implicants in variable form
def print_implicants(implicants,n,var_names):
    for i in implicants:
        bin=i.binary
        str=""
        for j in range(n):
            if bin[j]=='0':
                str=str+var_names[j]+"'"
            elif bin[j]=='1':
                str+=var_names[j]
        print(str,end="  ")

print("\nPrime implicants")
print_implicants(prime_implicants,n,var_names)
print()

#Function that find essential prime implicants
def find_essential_prime_implicatns(prime_implicants,minterms):
    essential_prime_implicants=[]
    nonessemtial_prime_implicants=[]

    for i in minterms:      #iterate over each minterm
        count=0         #counter that count occurence of minterms in prime implicants
        for j in prime_implicants:      #iterate over each prime implicants
            if i in j.minterms_covered:
                epi=j       #keeping track of prime implicant so that we can add it to the related list if it is essential pi.
                count+=1
            if count>1:
                break
        if count==1 and not epi in essential_prime_implicants:      #condition that verify if it is essential and not already in the list
            essential_prime_implicants.append(epi)
    
    for i in prime_implicants:      #find non essential prime implicants
        if not (i in essential_prime_implicants):
            nonessemtial_prime_implicants.append(i)

    return essential_prime_implicants,nonessemtial_prime_implicants

essential_prime_implicants, nonessemtial_prime_implicants = find_essential_prime_implicatns(prime_implicants,minterms)

print("\nEssential prime implicants")
print_implicants(essential_prime_implicants,n,var_names)
print()

print("\nNonessential prime implicants")
print_implicants(nonessemtial_prime_implicants,n,var_names)
print()


#Function that return set of minterms covered by given list of prime implicants
def minterms_coveredby_pi(prime_implicants):
    minterms_covered=set([])
    for i in prime_implicants:
        minterms_covered=minterms_covered.union(i.minterms_covered-set(dont_cares))
    return minterms_covered

#minterms that are not covered by essential prime implicants
remaining_minterms=set(minterms)-minterms_coveredby_pi(essential_prime_implicants)

import itertools
#Function that find smallest set of prime implicants that covers the remaining minterms
def find_minset(remaining_minterms,prime_implicants,n):
    len_pi=len(prime_implicants)
    
    #Function that will count the total literals in the given list of terms
    def literal_count(terms):
        count=0
        for term in terms:
            count=count+(n-term.binary.count('-'))
        return count

    #This loop will iterate through every subset of given prime implicants until it find smallest set that cover
    #remianing min terms.
    for i in range(1,n+1):
        combinations=itertools.combinations(range(len_pi),i)    #list of tuples of length i which are subsets of range(len_pi)
        minset=False
        min_literals=False
        
        for j in combinations:      #iterate over each set of indices
            pi=list(map(prime_implicants.__getitem__,j))    #return list of prime implicants with indices j
            minterms_covered=minterms_coveredby_pi(pi)
            
            #check if minterms covered by a set of prime implicants include all remaining minterms
            if remaining_minterms.issubset(minterms_covered):   
               if not min_literals:
                   min_literals=literal_count(pi)
               elif literal_count(pi)<=min_literals:    #identify set with smallest number of literals
                   minset=pi
                   min_literals=literal_count(pi)
        
        if minset:
            return minset
    return minset

minset=find_minset(remaining_minterms,nonessemtial_prime_implicants,n)

if not minset:
    print("\nAll minterms are covered by essential prime implicants so we don't need any non essential prime implicant.")
else:
    print("\nSmallest set of Non-Essential Prime Implicants for covering the remaining minterms are: ")
    print_implicants(minset,n,var_names)

    












