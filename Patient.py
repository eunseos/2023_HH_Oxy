import pandas as pd
import statistics


class risk:
    #default low and high thresholds based on: 
    #da Silva, P. L. , Reis, M. E. , Fonseca, T. M. & Fonseca, M. M. (2016). Opioid and Benzodiazepine Withdrawal Syndrome in PICU Patients. Journal of Addiction Medicine, 10 (2), 110-116.
    #Amigoni A, Vettore E, Brugnolaro V, et al. High doses of benzodiazepine predict analgesic and sedative drug withdrawal syndrome in paediatric intensive care patients. Acta Paediatr. 2014;103:e538‐e543.
    #Katz R, Kelly HW, Hsi A. Prospective study on the occurrence of withdrawal in critically ill children who receive fentanyl by continuous infusion. Crit Care Med. 1994;22:763‐767.
    
    #to set new thresholds, input dataframe must have columns: "Study", "Drug", "Units", "Low", "High"

    def __init__(self, input_df_path = None, low_threshold= 0.01672704, high_threshold= 0.102003891):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.input_df_path = input_df_path
        if input_df_path != None:
               self.input_df = pd.read_csv(input_df_path) 


    def set_new_thresholds(self):
        #helper functions
        def convert_unit(from_unit_type, to_unit_type, value):
            units = {
                "kg": 1000,
                "hg": 100,
                "dag": 10,
                "g": 1,
                "dg": 0.1,
                "cg": 0.01,
                "mg": 0.001,
                "mcg": 0.000001
        }
            from_type_units = units[from_unit_type]
            to_type_units = units[to_unit_type]
            new_value = value * (from_type_units / to_type_units)
            return new_value

        def convert_drug(from_drug, value):
            drugs = {
                "Codeine": 0.15,
                "Fentanyl": 0.0576,
                "Hydrocodone": 1,
                "Hydromorphone": 4,
                "Morphine": 1,
                "Oxycodone": 1.5,
                "Oxymorphone": 3
        }
            new_value = value * (drugs[from_drug])
            return new_value

        units = self.input_df['Units']
        drugs = self.input_df['Drug']
        low = self.input_df['Low']
        high = self.input_df['High']
        convertedLow = []
        convertedHigh = []
        for i in range(len(low)):
            convertedLow.append(convert_unit(units[i], "mg", low[i]))
            convertedHigh.append(convert_unit(units[i], "mg", high[i]))
        for i in range(len(convertedLow)):
            convertedLow[i] = convert_drug(drugs[i],  convertedLow[i])
            convertedHigh[i] = convert_drug(drugs[i], convertedHigh[i])

        self.low_threshold = statistics.mean(convertedLow)
        self.high_threshold = statistics.mean(convertedHigh)
        

class Patient:
    def __init__(self, name, medication_df_path, threshold_df_path = None):
        self.name = name 
        self.totalMorphine = 0 
        self.riskLevel = "high" 
        self.medication_df = pd.read_csv(medication_df_path)
        self.lastDose = self.medication_df.tail(1)
        self.totalMorphine = 0
        if threshold_df_path != None:
            self.risk_object = risk(threshold_df_path)
        else:
            self.risk_object = risk()


       
    def get_risk(self):
        low_threshold = self.risk_object.low_threshold
        high_threshold = self.risk_object.high_threshold
        if self.totalMorphine < low_threshold:
            self.riskLevel = "low"
        elif self.totalMorphine >= low_threshold and self.totalMorphine < high_threshold:
            self.riskLevel = "medium"
        else:
            self.riskLevel = "high"
    
    def calcMorph(self):
        #input: csv file containing patient data
        #output: cumulative morphine equivalents for patient

        #import morphonie equlivalent table
        morph_table = morph_table = pd.DataFrame({'Drug' : ['Codeine', 'Fentanyl', 'Hydrocodone', 'Hydromorphone', 'Methadone_1', 'Methadone_2', 'Methadone_3', 'Methadone_4', 'Morphine', 'Oxycodone', 'Oxymorphone'],'Conversion' : [0.15, 2.4, 1, 4, 4, 8, 10, 12, 1, 1.5, 3]})

        #import patient data and remove dates
        input_table = self.medication_df
        input_table = input_table.drop('Date', axis = 1)

        #group drug names in input data frame
        agg_functions =  {'Drug': 'first', 'Dose': 'sum'}
        output_table = input_table.groupby(input_table['Drug']).aggregate(agg_functions)
        output_table = output_table.drop('Drug', axis = 1)

        #add conversions column to new data frame, and create column with corresponding equivalents
        output_table = morph_table.merge(output_table, how = 'right', on = 'Drug')
        output_table['Equivalent'] = output_table['Conversion'] * output_table['Dose']

        #sum 'equivalent' column to get total morphine equivalents
        self.totalMorphine = sum(output_table['Equivalent'])









    
    

    
