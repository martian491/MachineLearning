from enum import Enum

class BoundaryChange(Enum):
    Nochange = 0
    Upper = 1
    Lower = 2
    Both = 3

class CGSSearch():
    def __init__(self, costfunc, x=0, d=1, eps=0.01):
        self.__FibCoe = 1.618
        self.__x = x
        self.__d = d
        self.__eps = eps
        self.__costfunc = costfunc

    @property
    def FibCoe(self):
        return self.__FibCoe

    @FibCoe.setter
    def FibCoe(self, value):
        self.__FibCoe = value

    @property
    def costfunc(self):
        return self.__costfunc

    @costfunc.setter
    def costfunc(self, costfunc):
        self.__costfunc = costfunc

    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, x):
        self.__x = x    

    @property
    def d(self):
        return self.__d

    @d.setter
    def d(self, d):
        self.__d = d

    @property
    def eps(self):
        return self.__eps

    @eps.setter
    def eps(self, eps):
        self.__eps = eps

    def Phase1(self, index):
        func = self.costfunc
        delta = 0.1

        g_2 = 0.
        g_1 = delta
        g   = 0.   

        fg_2 = func([self.x[i] + g_2 * self.d[i] for i in range(0, len(self.d))], index)
        fg_1 = func([self.x[i] + g_1 * self.d[i] for i in range(0, len(self.d))], index)
        fg   = 0
        
        if (fg_1 >= fg_2):
            return [g_2, g_1, fg_2, fg_1]

        index = 1
        #print('------------Phase 1 Start------------')
        while(True):
            # print('Phase1: ', index)
            if (index == 1):
                g = g_1 + delta * self.FibCoe**index
                fg = func([self.x[i] + g * self.d[i] for i in range(0, len(self.d))],index)
            else:
                g_2 = g_1
                g_1 = g
                g   = g_1 + delta * self.FibCoe**index 
 
                fg_2 = fg_1
                fg_1 = fg
                fg   = func([self.x[i] + g * self.d[i] for i in range(0, len(self.d))],index)
                
                return [g_2, g_1, g, fg_2, fg_1, fg]

            index = index + 1

    def Phase2(self, phase1, index):
        func = self.costfunc
        rho = 0.382

        if (len(phase1) == 4):
            I_Lower = phase1[0]
            I_Upper = phase1[1]    
        else:
            I_Lower = phase1[0]
            I_Upper = phase1[2]

        print('I_Lower:', I_Lower, 'I_Upper: ', I_Upper)
        Interval = I_Upper - I_Lower
        print("Interval: ", Interval)
        if (Interval < self.eps):
            return (I_Upper + I_Lower)/2

        MaxIter = 0
        while(True):
            if ((0.61893**MaxIter) <= (self.eps/Interval)):
                break
            MaxIter += 1

        print('Max Iter: ', MaxIter)

        alpha = 0
        beta = 0
        f_alpha = 0
        f_beta = 0
        bound = BoundaryChange.Nochange

        for index in range(0, MaxIter):
            if (index == 0):
                if (len(phase1) != 4):
                    alpha = phase1[1]
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = phase1[4]
                    f_beta  = func([self.x[i] + beta  * self.d[i] for i in range(0, len(self.d))],index)

                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))],index)
                    f_beta  = func([self.x[i] + beta  * self.d[i] for i in range(0, len(self.d))],index)

            else:
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = I_Lower + (1 - rho) * Interval
                    f_beta  = func([self.x[i] + beta  * self.d[i] for i in range(0, len(self.d))],index)
                elif (bound == BoundaryChange.Upper):
                    beta = alpha 
                    f_beta = f_alpha
                    alpha = I_Lower + rho * Interval
                    f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))],index)
                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))],index)
                    f_beta  = func([self.x[i] + beta  * self.d[i] for i in range(0, len(self.d))],index)
            
            if (f_alpha < f_beta):
                #print('Iter[', index, ']', ' Upper Bound Changed: ', I_Upper, '->', beta)
                I_Upper = beta
                bound = BoundaryChange.Upper
            elif (f_alpha > f_beta):
                #print('Iter[', index, ']', ' Lower Bound Changed: ', I_Lower, '->', alpha)
                I_Lower = alpha
                bound = BoundaryChange.Lower
            else:
                #print('Iter[', index, ']', ' All Bound Changed, Upper: ', I_Upper, '->', beta, ', Lower: ', I_Lower, '->', alpha)
                I_Lower = alpha
                I_Upper = beta
                bound = BoundaryChange.Both
            
            Interval = I_Upper - I_Lower

        return (I_Upper + I_Lower)/2

    def RunSearch(self, index):
        Phase1 = self.Phase1(index)
        X = self.Phase2(Phase1,index)
        return X

class CFiSearch(CGSSearch):
    def __init__(self, costfunc, x=0, d=1, eps=0.01):
        super(CFiSearch, self).__init__(costfunc, x, d, eps)

    def FibSequence(self,n):
        if n < 2:
            return 1
        else:
            return self.FibSequence(n-1) + self.FibSequence(n-2)

    def Phase2(self, phase1,index):
        #print('CFiSearcch Phase 2 Start')
        func = self.costfunc
        I_Lower = phase1[0]
        I_Upper = phase1[2]
        Interval = I_Upper - I_Lower
        # print('Lower:', I_Lower, 'Upper:', I_Upper)
        # print('Interval: ', Interval, 'eps: ', self.eps)
        if (Interval < self.eps):
            return (I_Upper + I_Lower)/2

        MaxIter = 0
        while(True):
            if ((0.61893**MaxIter) <= (self.eps/Interval)):
                break
            MaxIter += 1
        # print('Max Iter: ', MaxIter)

        Fibsqeuence = [self.FibSequence(i) for i in range(0, MaxIter+1)]

        alpha = 0
        beta = 0
        f_alpha = 0
        f_beta = 0
        bound = BoundaryChange.Nochange

        for index in range(0, MaxIter):
            if (index == 0):
                rho = 1 - Fibsqeuence[MaxIter-1]/ Fibsqeuence[MaxIter]
                alpha = I_Lower + rho * Interval
                beta = I_Lower + (1 - rho) * Interval
                f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))])
                f_beta = func([self.x[i] + beta * self.d[i] for i in range(0, len(self.d))])

            elif (index == (MaxIter-1)):
                rho = 0.5 - self.eps
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = I_Lower + (1 - rho) * Interval
                    f_beta = func([self.x[i] + beta * self.d[i] for i in range(0, len(self.d))])

                elif (bound == BoundaryChange.Upper):
                    beta = alpha 
                    f_beta = f_alpha
                    alpha = I_Lower + rho * Interval
                    f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))])

                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))])
                    f_beta = func([self.x[i] + beta * self.d[i] for i in range(0, len(self.d))])

            else:
                rho = 1 - (Fibsqeuence[MaxIter-index-1]/ Fibsqeuence[MaxIter-index])
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = I_Lower + (1 - rho) * Interval
                    f_beta = func([self.x[i] + beta * self.d[i] for i in range(0, len(self.d))])

                elif (bound == BoundaryChange.Upper):
                    beta = alpha 
                    f_beta = f_alpha
                    alpha = I_Lower + rho * Interval
                    f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))])

                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func([self.x[i] + alpha * self.d[i] for i in range(0, len(self.d))])
                    f_beta  = func([self.x[i] + beta  * self.d[i] for i in range(0, len(self.d))])

            if (f_alpha < f_beta):
                #print('Iter[', index, ']', ' Upper Bound Changed: ', I_Upper, '->', beta)
                I_Upper = beta
                bound = BoundaryChange.Upper
            elif (f_alpha > f_beta):
                #print('Iter[', index, ']', ' Lower Bound Changed: ', I_Lower, '->', alpha)
                I_Lower = alpha
                bound = BoundaryChange.Lower   
            else:
                #print('Iter[', index, ']', ' All Bound Changed, Upper: ', I_Upper, '->', beta, ', Lower: ', I_Lower, '->', alpha)
                I_Lower = alpha
                I_Upper = beta
                bound = BoundaryChange.Both

            Interval = I_Upper - I_Lower

        return (I_Lower + I_Upper) / 2

    def RunSearch(self,index):
        Phase1 = self.Phase1(index)
        #print('CFiSearch Phase 1 Upper: ', Phase1[0], 'Lower: ', Phase1[2])
        X = self.Phase2(Phase1,index)
        Phase1.clear()
        return X

