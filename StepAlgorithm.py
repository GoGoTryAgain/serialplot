
import threading

class StepAlgo(object):

    def __init__(self):
        self.__SrcData = []
        self.__MinBuffLen = 10
        self.__MinHighPeakTemp = 1000
        self.__MinLowPeakTemp = -200
        self.__DataBuffList = []
        self.__diff_v = [0] * (self.__MinBuffLen - 1)
        self.Step = 0
        self.StepThisAdd = 0
        self.__MinStepGate = 5
        self.StepMode = "Wait"
        self.ModeChangeCnt = 0
        self.timerStepUp = threading.Timer(4, self.FunTimer)
        self.timerStepUp.cancel()
        self.Callback = self.funCallBack

        self.__Peak = {'HPeakPos': [], 'LowPeakPos': []}

    def funCallBack(self,data):
        pass


    def FunTimer(self):
        # has step added
        if self.StepThisAdd > 0:
            if self.StepMode == "Wait":
                self.ModeChangeCnt = self.ModeChangeCnt + self.StepThisAdd
                if self.ModeChangeCnt >= self.__MinStepGate:
                    self.ModeChangeCnt = self.__MinStepGate # prevent buffer over
                    self.StepMode = "ADD"
                    self.Step = self.Step + self.StepThisAdd
                    self.StepThisAdd = 0
                # else: # need wait mode change
                #     self.ModeChangeCnt = self.ModeChangeCnt + self.StepThisAdd

            else: #add mode
                self.Step = self.Step + self.ModeChangeCnt
                self.StepThisAdd = 0
            self.Callback(self.Step)
            # self.root.variables['StepCount'].set(value=self.Step)
            self.timerStepUp = threading.Timer(4, self.FunTimer)
            self.timerStepUp.start()
        else:
            self.StepMode = "Wait"
            self.ModeChangeCnt = 0
        # # start timer
        # global timerStepUp
        # timerStepUp = threading.Timer(4, self.FunTimer)
        # timerStepUp.start()





    # 差分计算
    def DiffFigure(self,listSrc):
        for i in range(len(self.__diff_v) - 1):
            if listSrc[i + 1] > listSrc[i]:
                self.__diff_v[i] = 1
            elif listSrc[i + 1] == listSrc[i]:
                self.__diff_v[i] = 0
            else:
                self.__diff_v[i] = -1

    # 对Trend做一次遍历
    def Ergodic(self):
        for i in range(len(self.__diff_v) - 1 ,-1 , -1):
            if(self.__diff_v[i] == 0 and i == len(self.__diff_v) - 1):
                self.__diff_v[i] = 1
            elif self.__diff_v[i] == 0:
                if self.__diff_v[i - 1] >= 0:
                    self.__diff_v[i] = 1
                else:
                    self.__diff_v[i] = -1

    #寻找波峰与波谷
    def FindPeak(self, Newdata):
        self.__DataBuffList.append(Newdata)
        if len(self.__DataBuffList) > self.__MinBuffLen:
            self.__DataBuffList.pop(0)
            self.DiffFigure(self.__DataBuffList)

            for i in range(len(self.__diff_v) - 1):
                if self.__diff_v[i + 1] - self.__diff_v[i] == -2:
                    self.__Peak['HPeakPos'].append(i + 1)
                elif self.__diff_v[i + 1] - self.__diff_v[i] == 2:
                    self.__Peak['LowPeakPos'].append(i + 1)

    #根据波峰时刻的数据大小，来过滤干扰，再根据有效波峰来确定步数
    def GetStep(self):
        for i in range(len(self.__Peak['HPeakPos'])):
            if self.__DataBuffList[self.__Peak['HPeakPos'][i]] >= self.__MinHighPeakTemp:
                print("data = ",self.__DataBuffList[self.__Peak['HPeakPos'][i]],"\n")
                self.StepThisAdd = self.StepThisAdd + 1




    def StepAlgo(self,SrcData,Callback):

        self.FindPeak(SrcData)
        self.GetStep()
        MaxHPeak = 0
        MaxLPeak = 0
        if self.__Peak['HPeakPos']:
            MaxHPeak = max(self.__Peak['HPeakPos'])
        if self.__Peak['LowPeakPos']:
            MaxLPeak = max(self.__Peak['LowPeakPos'])

        if MaxHPeak > MaxLPeak:
            PopLen = MaxHPeak
        else:
            PopLen = MaxLPeak

        for i in range(PopLen):
            if self.__DataBuffList:
                self.__DataBuffList.pop(0)

        self.__Peak['HPeakPos'] = []
        self.__Peak['LowPeakPos'] = []
        self.Callback = Callback
        if not self.timerStepUp.is_alive() :
            self.timerStepUp = threading.Timer(4, self.FunTimer)
            self.timerStepUp.start()
        # return self.Step

