-- Create Hospital Database
CREATE DATABASE IF NOT EXISTS drqueryDB;
USE drqueryDB;

-- Patients Table
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('M', 'F', 'Other') NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    address TEXT,
    emergency_contact VARCHAR(100),
    emergency_phone VARCHAR(15),
    registration_date DATE DEFAULT (CURRENT_DATE)
);

-- Doctors Table
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    license_number VARCHAR(50) UNIQUE,
    department_id INT,
    hire_date DATE NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active'
);

-- Departments Table
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    head_doctor_id INT
);

-- Appointments Table
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status ENUM('scheduled', 'completed', 'cancelled', 'no_show') DEFAULT 'scheduled',
    reason VARCHAR(200),
    notes TEXT
);

-- Medical Records Table
CREATE TABLE medical_records (
    record_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    visit_date DATE NOT NULL,
    diagnosis TEXT,
    treatment TEXT,
    prescription TEXT,
    notes TEXT
);

-- Medications Table
CREATE TABLE medications (
    medication_id INT PRIMARY KEY AUTO_INCREMENT,
    medication_name VARCHAR(100) NOT NULL,
    dosage VARCHAR(50),
    manufacturer VARCHAR(100),
    price DECIMAL(8,2),
    stock_quantity INT DEFAULT 0,
    expiry_date DATE
);

-- Prescriptions Table
CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    medication_id INT NOT NULL,
    dosage_instructions TEXT,
    quantity INT NOT NULL,
    prescribed_date DATE NOT NULL,
    duration_days INT
);

-- Add Foreign Key Constraints
ALTER TABLE doctors ADD FOREIGN KEY (department_id) REFERENCES departments(department_id);
ALTER TABLE departments ADD FOREIGN KEY (head_doctor_id) REFERENCES doctors(doctor_id);
ALTER TABLE appointments ADD FOREIGN KEY (patient_id) REFERENCES patients(patient_id);
ALTER TABLE appointments ADD FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id);
ALTER TABLE medical_records ADD FOREIGN KEY (patient_id) REFERENCES patients(patient_id);
ALTER TABLE medical_records ADD FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id);
ALTER TABLE prescriptions ADD FOREIGN KEY (patient_id) REFERENCES patients(patient_id);
ALTER TABLE prescriptions ADD FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id);
ALTER TABLE prescriptions ADD FOREIGN KEY (medication_id) REFERENCES medications(medication_id);