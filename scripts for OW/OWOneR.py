"""
<name>OneR</name>
<description>Applies 1R algorithm to dataset.</description>
<icon>./icon_1R_classifier.png</icon>
<contact>fallens4e@gmail.com</contact>
<priority>1</priority>
"""

import Orange.feature
from OWWidget import *
import OWGUI

# To change this template, choose Tools | Templates
# and open the template in the editor.

import Orange as DM


class StringBuilder():
    def __init__(self, initStr=''):
        self.strList = [initStr]
    
    def append(self, string = ''):
        self.strList.append(string+'\n')
        
    def getText(self):
        return ''.join(self.strList)


class OWOneR(OWWidget):
    
    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, 'SampleDataA')
        
        self.inputs = [("Data", ExampleTable, self.oneR)]
        self.outputs = [("Sampled Data", ExampleTable)]

        # GUI
        box = OWGUI.widgetBox( self.controlArea, "Info" )
        self.infoa = OWGUI.widgetLabel( box, 'No input data; waiting for the input signal (A).' )
        self.infob = OWGUI.widgetLabel( box, '' )
        self.resize( 100, 50 )
#        
#    def data(self, dataset):
#        if dataset:
#            self.infoa.setText('%d instances in input data set' % len(dataset))
#            indices = orange.MakeRandomIndices2(p0=0.1)
#            ind = indices(dataset)
#            sample = dataset.select(ind, 0)
#            self.infob.setText('%d sampled instances' % len(sample))
#            self.send("Sampled Data", sample)
#        else:
#            self.infoa.setText('No data on input yet, waiting to get something.')
#            self.infob.setText('')
#            self.send("Sampled Data", None)
#            
    def load(self, fileName ):
        try:
            dataset = DM.data.Table( fileName )
        except:
            sb.append( "--->>> error - can not open the file: %s" % fileName )
            exit()
        return dataset
    
    def printRules(self, pred, dataset, sb):
        accs = {} #accuracies
        for feature in dataset.domain.features:
            cm = DM.statistics.contingency.VarClass( feature.name, dataset )
            accs.update({feature.name: (0, 0)})
    #        acc[feature.name]
            for value, distribution in cm.items():
                total = sum(distribution)
                minErrIdx = 0
                errorBest = total - distribution[ 0 ]
                for index in range( len (distribution ) ):
                    error = total - distribution[ index ]
                    if (error < errorBest):
                        errorBest = error
                        minErrIdx = index
                class_value = DM.data.Value( cm.class_var, minErrIdx )
                if (pred(feature.name)):
                    sb.append( "('%s', '%s', '%s'): (%s, %s)" % ( feature.name, value, class_value, errorBest, total ))
                accs.update({feature.name : (accs[feature.name][0] + errorBest, total)})
        return accs
    
    def oneR( self , dataset ):
        if dataset:
            self.infoa.clear()
            sb = StringBuilder()
            sb.append('Amount of instances in the dataset: ' + `len(dataset)`)
            #attr value count
            sb.append("attr value target count:")
            sb.append( "(attr, value, target)")
            for feature in dataset.domain.features:
                cm = DM.statistics.contingency.VarClass( feature.name, dataset )
                for value, distribution in cm.items():
                    for index in range( len (distribution ) ):
                        class_value = DM.data.Value( cm.class_var, index )
                        sb.append( "('%s', '%s', '%s'): %s" % 
                                ( feature.name, value, class_value, distribution[ index ] ))
        
            sb.append()
            sb.append( "Hypotheses:" )
            sb.append( "(attr, valueAttr, valueTarget) : (error, total)")
            accs = self.printRules(lambda x: True, dataset, sb)
        
            sb.append()
            sb.append( "OneR:")
            sb.append( "attr: (error, total, error/total)")
            numRow = len (dataset)
            for (k, (err, total)) in accs.items():
                sb.append( "%s: (%s, %s, %s)" % (k, err, numRow, err / numRow))
        
            t = map((lambda fName, (x,y): (x/y, fName)),
                        accs.keys(),
                        accs.values())
            (_, fName) = sorted(t)[0]
        
            sb.append()
            sb.append( "result  = '%s', values:" % fName)
            
            self.printRules(lambda f: f == fName, dataset, sb)
            self.infob.setText(sb.getText())
            return 
        else:
            self.infoA.setText( 'No input data; waiting for the input signal (B).' )
            self.infoB.setText( '' )
            self.send( "Sampled Data", None )   
            return ''
            
        

if __name__=="__main__":
    appl = QApplication(sys.argv)
    ow = OWOneR()
    ow.show()
    fileName = "G:\\sting\\univer\\master 2\\data mining\\ModuleOfPractice5\\dataset\\lenses.tab"
        #fileName = "D:\\projects\\edu\\DataMining\\ModuleOfPractice5\\dataset\\lenses.tab"
    dataset = ow.load( fileName )
    ow.oneR(dataset)
    appl.exec_()

    



"""
python shell log:

import Orange as DM
fileName = "D:\\projects\\edu\\DataMining\\ModuleOfPractice5\\dataset\\lenses.tab"
dataset = DM.data.Table( fileName )

sb.append( dataset.domain
sb.append( dataset.domain.features

feature = dataset.domain.features[0] # features are variables(all fields) - class_var

feature.vat_type
feature.values
feature.name

dataset
dataset[0]
dataset[0][0]

contingencyMatrix = DM.statistics.contingency.VarClass( feature.name, dataset )
cm = contingencyMatrix

cm.items() # all the values of the feature and distribution of the class values with that values of the feature

cm.items() # [('pre-presbyopic', <5.000, 1.000, 2.000>), ('presbyopic', <6.000, 1.000, 1.000>), ('young', <4.000, 2.000, 2.000>)]

cm.items()[0] # ('pre-presbyopic', <5.000, 1.000, 2.000>)
cm.items()[0][1] # <5.000, 1.000, 2.000>
cm.items()[0][1][0] # 5.0  - value of an element with index 0 which is <orange.Value 'lenses'='none'>

cm.class_var # all the values of the class
DM.data.Value( cm.class_var, 0 ) # returns value of the 0th values of the class


"""