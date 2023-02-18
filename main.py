from Patient import Patient
from Patient import risk


test_patient = Patient("test", "/Users/Caden/Downloads/patient_sample_0.csv")
test_patient.get_risk()
test_patient.calcMorph()
print(test_patient.medication_df)
print(test_patient.lastDose)
print("Patient total cumulative morphine: ", test_patient.totalMorphine)
print("Patient risk level: ",test_patient.riskLevel)

