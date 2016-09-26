import math
class TCurve(object):

# outward facing methods
    def __init__(self, n=None):
        functionName = "TCurve.__init__: "
        if(n == None):
            raise ValueError(functionName + "invalid n")
        if(not(isinstance(n, int))):
            raise ValueError(functionName + "invalid n")
        if((n < 2) or (n >= 30)):
            raise ValueError(functionName + "invalid n")
        self.n = n

    
    def p(self, t=None, tails=1):
        functionName = "TCurve.p: "
        if(t == None):
            raise ValueError(functionName + "missing t")
        if(not(isinstance(t, float))):
            raise ValueError(functionName + "invalid t")
        if(t < 0.0):
            raise ValueError(functionName + "invalid t")
        
        if(not(isinstance(tails, int))):
            raise ValueError(functionName + "invalid tails")
        if((tails != 1) & (tails != 2)):
            raise ValueError(functionName + "invalid tails")
        
        constant = self. calculateConstant(self.n)
        integration = self.integrate(t, self.n, self.f)
        if(tails == 1):
            result = constant * integration + 0.5
        else:
            result = constant * integration * 2
            
        if(result > 1.0):
            raise ValueError(functionName + "result > 1.0")
        
        return result
        
# internal methods
    def gamma(self, x):
        if(x == 1):
            return 1
        if(x == 0.5):
            return math.sqrt(math.pi)
        return (x - 1) * self.gamma(x - 1)
    
    def calculateConstant(self, n):
        n = float(n)
        numerator = self.gamma((n + 1.0) / 2.0)
        denominator = self.gamma(n / 2.0) * math.sqrt(n * math.pi)
        result = numerator / denominator
        return result
    
    def f(self, u, n):
        n = float(n)
        base = (1 + (u ** 2) / n)
        exponent = -(n + 1.0) / 2
        result = base ** exponent
        return result
    
    def integrate(self, t, n, f):     
        epsilon = 0.001  # Declaring epsilon
        simpsonOld = 0.0
        simpsonNew = epsilon  # Assigning epsilon
        lowBound = 0  # Low bound
        highBound = t  # High bound
        w=0.0
        s = 4  # No of slices of our choice
        while (abs((simpsonNew - simpsonOld) / simpsonNew) > epsilon):
            simpsonOld = simpsonNew 
            sArea = (highBound - lowBound)  # Get high bound           
            w = (sArea) / s
            sOne = f(lowBound, n)  # Finding first term
            
            sMiddle = 0.0 # Add all middle terms
            
            sStart = 1
            sEO = "O"
            
            while(sStart < s): # Starting loop along with no of slices
                if(sEO == "O"):
                    sMiddle += self.getTerm(n, lowBound, sStart, w, sEO,f) # Get the odd values                    
                    sEO = "E"    
                    sStart = sStart + 1     
                else:
                    sMiddle += self.getTerm(n, lowBound, sStart, w, sEO,f)  # Get the even values
                    sEO = "O" 
                    sStart = sStart + 1 # Increment values
                
            sEnd = f(highBound, n)  # Finding last term
            sAll = 0
            sAll = sOne + sMiddle + sEnd
            simpsonNew = sAll * (w / 3.0)  # simpsons rule integration
            s = s * 2  # doubles the number of slices   
        
        return simpsonNew         
    
    # Get the odd and even values
        
    def getTerm(self, n, lowBound, i, w, term,f):
        sOdd=0.0
        if(term == "O"):  # If odd          
            sOdd = (i * w)
            sTerm = (4.0 * f(sOdd, n)) # Multiply with 4 for odd terms
        else: # If even
            sEven = (i * w)
            sTerm = (2.0 * f(sEven, n)) # Multiply with 4 for even terms
        return sTerm    
        
    
        
            
        
