'''
2023 Health Hackathon
Generate Data
'''

import numpy as np
import pandas as pd
import datetime
import random

class Patient:
    def __init__(self, dosing_path):
        self.dosing_df = pd.read_csv(dosing_path, header = 0, index_col = 0)

        self.p1_days = self.get_p1_days()
        self.p2_days = self.get_p2_days()
        self.p1_drug = self.get_p1_drug()
        self.p2_drug = self.get_p2_drug()

        self.p1_doses = self.get_dose(1)
        self.p2_doses = self.get_dose(2)

        self.dose_schedule = self.make_schdeule_df()

    def __repr__(self):
        p1_str = f"Phase 1: {self.p1_days} days on {self.p1_drug}"
        p2_str = f"Phase 2: {self.p2_days} days on {self.p2_drug}"
        return "\n".join([p1_str, p2_str])

    # Output number of days in NICU
    def get_p1_days(self):
        retain_prob = np.array([1, 0.88, 0.58, 0.18, 0.09, 0.04, 0.01, 0.001])
        prob_dist = retain_prob / np.sum(retain_prob)
        days = np.random.choice(np.arange(7, -1, -1), p = prob_dist)
        return days

    # Output number of days in hospital after NICU
    def get_p2_days(self):
        days = np.random.normal(9.1, 4.4)
        while (days < 14 and days > 21):
            days = np.random.normal(9.1, 4.4)
        return round(days)
    
    # Output type of drug taken in phase 1
    def get_p1_drug(self):
        drug = np.random.choice(["Morphine", "Hydromorphone", "Oxymorphone"],\
                                 p = [0.4, 0.4, 0.2])
        return drug

    # Output type of drug taken in phase 2
    def get_p2_drug(self):
        drug = np.random.choice(["Codeine", "Hydrocodone", "Oxycodone"])
        return drug

    # Output doses for drugs taken in phase 1 or phase 2
    def get_dose(self, phase):
        if phase == 1:
            dose_min = self.dosing_df.loc[self.p1_drug, 'Dose_min']
            dose_max = self.dosing_df.loc[self.p1_drug, 'Dose_max']
            # Random vector for possible fluctuations in dosage
            dose_fluct = np.random.uniform(0.7, 1.3, self.p1_days)
            # Number of doses per day
            dose_num = 24 / self.dosing_df.loc[self.p1_drug, 'Time']
            # Unit dose per administration
            unit_dose = np.random.uniform(dose_min, dose_max)
            doses = np.full((self.p1_days, ), unit_dose) * dose_fluct * dose_num
        elif phase == 2:
            dose_min = self.dosing_df.loc[self.p2_drug, 'Dose_min']
            dose_max = self.dosing_df.loc[self.p2_drug, 'Dose_max']
            dose_fluct = np.random.uniform(0.7, 1.3, self.p2_days)
            dose_num = 24 / self.dosing_df.loc[self.p2_drug, 'Time']
            unit_dose = np.random.uniform(dose_min, dose_max)
            doses = np.full((self.p2_days, ), unit_dose) * dose_fluct * dose_num
        return doses.tolist()

    def make_schdeule_df(self):
        start_date = datetime.date(2015, 1, 1)
        end_date = start_date + datetime.timedelta(days = 7 * 365)
        p1_start_date = start_date + (end_date - start_date) * random.random()
        p2_end_date = p1_start_date + \
            datetime.timedelta(days = int(self.p1_days) + int(self.p2_days) - 1)

        date_col = pd.date_range(p1_start_date, p2_end_date, freq = 'd')
        drug_col = [self.p1_drug for i in range(self.p1_days)] + \
                   [self.p2_drug for i in range(self.p2_days)]
        dose_col = self.p1_doses + self.p2_doses

        # add row for fentanyl during surgery
        fent_dose = np.random.uniform(self.dosing_df.loc["Fentanyl", "Dose_min"], \
                                      self.dosing_df.loc["Fentanyl", "Dose_max"]) / 1000
        fent_row = pd.DataFrame({"Date" : start_date - datetime.timedelta(days = 1), "Drug" : "Fentanyl", "Dose" : fent_dose}, index = [0])
        dose_schedule = pd.concat([fent_row, pd.DataFrame({"Date" : date_col, "Drug" : drug_col, "Dose" : dose_col})])
        return dose_schedule

def main():
    for i in range(20):
        save_path = f"sample_data/patient_sample_{i}.csv"
        sample_df = Patient("Dosing_Data.csv").dose_schedule
        sample_df.to_csv(save_path, index = False)

if __name__ == "__main__":
    main()
    