-- Insert Sample Data for Hospital Database
USE drqueryDB;

-- Insert Departments
INSERT INTO departments (department_name, location) VALUES
('Cardiology', 'Building A, Floor 2'),
('Neurology', 'Building B, Floor 3'),
('Pediatrics', 'Building C, Floor 1'),
('Emergency', 'Building A, Floor 1'),
('Orthopedics', 'Building B, Floor 2'),
('Radiology', 'Building A, Floor 3'),
('Surgery', 'Building B, Floor 4'),
('Internal Medicine', 'Building C, Floor 2');

-- Insert Doctors
INSERT INTO doctors (first_name, last_name, specialization, phone, email, license_number, department_id, hire_date) VALUES
('Sarah', 'Johnson', 'Cardiologist', '555-0101', 'sarah.johnson@hospital.com', 'MD001', 1, '2020-03-15'),
('Michael', 'Chen', 'Neurologist', '555-0102', 'michael.chen@hospital.com', 'MD002', 2, '2019-07-22'),
('Emily', 'Davis', 'Pediatrician', '555-0103', 'emily.davis@hospital.com', 'MD003', 3, '2021-01-10'),
('Robert', 'Wilson', 'Emergency Physician', '555-0104', 'robert.wilson@hospital.com', 'MD004', 4, '2018-11-05'),
('Lisa', 'Anderson', 'Orthopedic Surgeon', '555-0105', 'lisa.anderson@hospital.com', 'MD005', 5, '2020-09-18'),
('David', 'Martinez', 'Radiologist', '555-0106', 'david.martinez@hospital.com', 'MD006', 6, '2019-04-12'),
('Jennifer', 'Taylor', 'General Surgeon', '555-0107', 'jennifer.taylor@hospital.com', 'MD007', 7, '2021-06-30'),
('James', 'Brown', 'Internal Medicine', '555-0108', 'james.brown@hospital.com', 'MD008', 8, '2020-12-03'),
('Maria', 'Garcia', 'Cardiologist', '555-0109', 'maria.garcia@hospital.com', 'MD009', 1, '2022-02-14'),
('Thomas', 'Miller', 'Pediatrician', '555-0110', 'thomas.miller@hospital.com', 'MD010', 3, '2021-08-25');

-- Update department heads
UPDATE departments SET head_doctor_id = 1 WHERE department_id = 1;
UPDATE departments SET head_doctor_id = 2 WHERE department_id = 2;
UPDATE departments SET head_doctor_id = 3 WHERE department_id = 3;
UPDATE departments SET head_doctor_id = 4 WHERE department_id = 4;
UPDATE departments SET head_doctor_id = 5 WHERE department_id = 5;
UPDATE departments SET head_doctor_id = 6 WHERE department_id = 6;
UPDATE departments SET head_doctor_id = 7 WHERE department_id = 7;
UPDATE departments SET head_doctor_id = 8 WHERE department_id = 8;

-- Insert Patients
INSERT INTO patients (first_name, last_name, date_of_birth, gender, phone, email, address, emergency_contact, emergency_phone, registration_date) VALUES
('John', 'Smith', '1985-06-15', 'M', '555-1001', 'john.smith@email.com', '123 Main St, City', 'Jane Smith', '555-1002', '2023-01-15'),
('Mary', 'Johnson', '1992-03-22', 'F', '555-1003', 'mary.johnson@email.com', '456 Oak Ave, City', 'Bob Johnson', '555-1004', '2023-02-10'),
('William', 'Brown', '1978-11-08', 'M', '555-1005', 'william.brown@email.com', '789 Pine St, City', 'Susan Brown', '555-1006', '2023-01-28'),
('Elizabeth', 'Davis', '1990-09-12', 'F', '555-1007', 'elizabeth.davis@email.com', '321 Elm St, City', 'Michael Davis', '555-1008', '2023-03-05'),
('James', 'Wilson', '2010-04-18', 'M', '555-1009', 'parent@email.com', '654 Maple Ave, City', 'Linda Wilson', '555-1010', '2023-02-20'),
('Patricia', 'Miller', '1965-12-03', 'F', '555-1011', 'patricia.miller@email.com', '987 Cedar St, City', 'Robert Miller', '555-1012', '2023-01-08'),
('Robert', 'Garcia', '1988-07-25', 'M', '555-1013', 'robert.garcia@email.com', '147 Birch Ave, City', 'Maria Garcia', '555-1014', '2023-03-12'),
('Jennifer', 'Martinez', '1995-01-30', 'F', '555-1015', 'jennifer.martinez@email.com', '258 Spruce St, City', 'Carlos Martinez', '555-1016', '2023-02-18'),
('Michael', 'Anderson', '1982-08-14', 'M', '555-1017', 'michael.anderson@email.com', '369 Willow Ave, City', 'Sarah Anderson', '555-1018', '2023-01-22'),
('Linda', 'Taylor', '1975-05-07', 'F', '555-1019', 'linda.taylor@email.com', '741 Poplar St, City', 'David Taylor', '555-1020', '2023-03-01'),
('Christopher', 'Thomas', '2008-10-11', 'M', '555-1021', 'parent2@email.com', '852 Ash Ave, City', 'Nancy Thomas', '555-1022', '2023-02-25'),
('Barbara', 'Jackson', '1970-02-28', 'F', '555-1023', 'barbara.jackson@email.com', '963 Hickory St, City', 'William Jackson', '555-1024', '2023-01-18');

-- Insert Medications
INSERT INTO medications (medication_name, dosage, manufacturer, price, stock_quantity, expiry_date) VALUES
('Aspirin', '81mg', 'PharmaCorp', 12.50, 500, '2025-12-31'),
('Lisinopril', '10mg', 'MediTech', 25.75, 300, '2025-08-15'),
('Metformin', '500mg', 'HealthPharma', 18.90, 450, '2025-10-20'),
('Amoxicillin', '250mg', 'AntiBio Inc', 32.40, 200, '2024-11-30'),
('Ibuprofen', '200mg', 'PainRelief Co', 15.60, 600, '2025-09-12'),
('Atorvastatin', '20mg', 'CardioMed', 45.80, 250, '2025-07-08'),
('Omeprazole', '20mg', 'GastroHealth', 28.30, 350, '2025-06-25'),
('Hydrochlorothiazide', '25mg', 'DiureticPharma', 22.15, 180, '2025-05-18'),
('Acetaminophen', '500mg', 'FeverAway', 11.25, 750, '2025-11-22'),
('Prednisone', '5mg', 'SteroidMed', 38.70, 120, '2024-12-15');

-- Insert Appointments
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, reason, notes) VALUES
(1, 1, '2024-01-15', '09:00:00', 'completed', 'Chest pain evaluation', 'Patient reported mild chest discomfort'),
(2, 3, '2024-01-16', '10:30:00', 'completed', 'Annual checkup', 'Routine pediatric examination'),
(3, 2, '2024-01-17', '14:00:00', 'completed', 'Headache consultation', 'Chronic headaches for 2 weeks'),
(4, 8, '2024-01-18', '11:15:00', 'completed', 'Diabetes follow-up', 'Blood sugar monitoring'),
(5, 10, '2024-01-19', '15:30:00', 'completed', 'School physical', 'Required sports physical'),
(6, 1, '2024-01-22', '08:45:00', 'scheduled', 'Heart palpitations', 'Patient reports irregular heartbeat'),
(7, 5, '2024-01-23', '13:20:00', 'scheduled', 'Knee pain', 'Sports injury evaluation'),
(8, 4, '2024-01-24', '16:00:00', 'cancelled', 'Emergency visit', 'Patient cancelled due to improvement'),
(9, 6, '2024-01-25', '12:00:00', 'scheduled', 'X-ray results', 'Follow-up on chest X-ray'),
(10, 7, '2024-01-26', '09:30:00', 'scheduled', 'Pre-surgery consultation', 'Gallbladder surgery planning');

-- Insert Medical Records
INSERT INTO medical_records (patient_id, doctor_id, visit_date, diagnosis, treatment, prescription, notes) VALUES
(1, 1, '2024-01-15', 'Mild angina', 'Lifestyle modifications, medication', 'Aspirin 81mg daily', 'Patient advised to reduce stress and exercise regularly'),
(2, 3, '2024-01-16', 'Healthy child', 'Routine care', 'Multivitamin', 'Growth and development normal for age'),
(3, 2, '2024-01-17', 'Tension headache', 'Pain management', 'Ibuprofen 200mg as needed', 'Recommend stress reduction techniques'),
(4, 8, '2024-01-18', 'Type 2 Diabetes', 'Blood sugar control', 'Metformin 500mg twice daily', 'HbA1c levels improving'),
(5, 10, '2024-01-19', 'Healthy adolescent', 'Sports clearance', 'None', 'Cleared for all sports activities'),
(1, 1, '2023-12-10', 'Hypertension', 'Blood pressure management', 'Lisinopril 10mg daily', 'Blood pressure well controlled'),
(6, 1, '2023-11-15', 'Atrial fibrillation', 'Cardiac monitoring', 'Atorvastatin 20mg daily', 'Regular cardiology follow-up needed'),
(7, 5, '2023-10-20', 'Osteoarthritis', 'Joint pain management', 'Acetaminophen 500mg as needed', 'Physical therapy recommended'),
(8, 4, '2023-09-25', 'Acute bronchitis', 'Antibiotic treatment', 'Amoxicillin 250mg three times daily', 'Complete 7-day course'),
(9, 6, '2023-08-30', 'Pneumonia', 'Chest infection treatment', 'Amoxicillin 250mg, Prednisone 5mg', 'Chest X-ray shows improvement');

-- Insert Prescriptions
INSERT INTO prescriptions (patient_id, doctor_id, medication_id, dosage_instructions, quantity, prescribed_date, duration_days) VALUES
(1, 1, 1, 'Take 1 tablet daily with food', 30, '2024-01-15', 30),
(1, 1, 2, 'Take 1 tablet daily in morning', 30, '2023-12-10', 30),
(3, 2, 5, 'Take 1-2 tablets every 6 hours as needed for pain', 20, '2024-01-17', 7),
(4, 8, 3, 'Take 1 tablet twice daily with meals', 60, '2024-01-18', 30),
(6, 1, 6, 'Take 1 tablet daily at bedtime', 30, '2023-11-15', 30),
(7, 5, 9, 'Take 1-2 tablets every 4-6 hours as needed', 30, '2023-10-20', 14),
(8, 4, 4, 'Take 1 capsule three times daily', 21, '2023-09-25', 7),
(9, 6, 4, 'Take 1 capsule three times daily', 21, '2023-08-30', 7),
(9, 6, 10, 'Take 1 tablet daily for 5 days', 5, '2023-08-30', 5),
(2, 3, 9, 'Take 1 tablet as needed for fever', 10, '2024-01-16', 7);