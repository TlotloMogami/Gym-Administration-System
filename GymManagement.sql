CREATE DATABASE IF NOT EXISTS GymManagement;
USE GymManagement;

CREATE TABLE Admin (
    AdminID INT PRIMARY KEY,
    FullName VARCHAR(100),
    EmailAddress VARCHAR(100),
    PhoneNumber VARCHAR(20)
);

INSERT INTO Admin (AdminID, FullName, EmailAddress, PhoneNumber) VALUES
(501101, 'John Baloyi', '501101@mynwu.ac.za', '0793754561'),
(501102, 'Simon Sithole', '501102@mynwu.ac.za', '0644564567'),
(501103, 'Katlego Tawana', '501103@mynwu.ac.za', '0826574783');

CREATE TABLE MembershipType (
    PlanID INT PRIMARY KEY,
    PlanName VARCHAR(50),
    Features TEXT,
    Price DECIMAL(10,2)
);

INSERT INTO MembershipType (PlanID, PlanName, Features, Price) VALUES
(601101, 'Basic', 'Gym access only', 279.99),
(601102, 'Standard', 'Gym + Group Classes', 399.99),
(601103, 'Premium', 'All access + Personal Trainer', 779.99);

CREATE TABLE Trainer (
    TrainerID INT PRIMARY KEY,
    ProgrameID INT,
    FullName VARCHAR(100),
    Email VARCHAR(100),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20)
);

INSERT INTO Trainer (TrainerID, ProgrameID, FullName, Email, Address, PhoneNumber) VALUES
(701101, 401101, 'Easy Manyike', '701101@mynwu.ac.za', '2790 Mmabatho', '0839644738'),
(701102, 401102, 'Lornel Kubayi', '701102@mynwu.ac.za', '2750 Bokone', '0736893657'),
(701103, 401103, 'Tshikani Masete', '701103@mynwu.ac.za', '2763 Signal Hill', '0658367463');

CREATE TABLE FitnessProgramme (
    ProgrameID INT PRIMARY KEY,
    MemberID INT,
    TrainerID INT,
    Name VARCHAR(100)
);

-- Insert sample Fitness Programmes
INSERT INTO FitnessProgramme (ProgrameID, MemberID, TrainerID, Name) VALUES
(401101, 100101, 701101, 'Weight Loss'),
(401102, 100102, 701102, 'Strength Training'),
(401103, 100103, 701103, 'Cardio Fit'),
(401104, 100104, 701101, 'HIIT'),
(401105, 100105, 701102, 'Yoga'),
(401106, 100106, 701103, 'CrossFit'),
(401107, 100107, 701101, 'Endurance'),
(401108, 100108, 701102, 'Pilates'),
(401109, 100109, 701103, 'Bodybuilding'),
(401110, 100110, 701101, 'Core Strength'),
(401111, 100111, 701102, 'Mobility Training'),
(401112, 100112, 701103, 'Functional Training'),
(401113, 100113, 701101, 'Marathon Prep'),
(401114, 100114, 701102, 'Dance Fitness'),
(401115, 100115, 701103, 'Balance Training'),
(401116, 100116, 701101, 'Cycling Power'),
(401117, 100117, 701102, 'Resistance Training'),
(401118, 100118, 701103, 'Aerobic Workout'),
(401119, 100119, 701101, 'Boxing Fit'),
(401120, 100120, 701102, 'Stretch & Tone');

CREATE TABLE Venue (
    VenueID INT PRIMARY KEY,
    SessionID INT,
    Capacity INT
);

INSERT INTO Venue (VenueID, SessionID, Capacity) VALUES
(801101, 901101, 30),
(801102, 901102, 25),
(801103, 901103, 20),
(801104, 901104, 35),
(801105, 901105, 40);

CREATE TABLE Session (
    SessionID INT PRIMARY KEY,
    AdminID INT,
    TrainerID INT,
    MemberID INT,
    VenueID INT,
    ProgrameID INT
);

INSERT INTO Session (SessionID, AdminID, TrainerID, MemberID, VenueID, ProgrameID) VALUES
(901101, 501101, 701101, 100101, 801101, 401101),
(901102, 501102, 701102, 100102, 801102, 401102),
(901103, 501103, 701103, 100103, 801103, 401103),
(901104, 501101, 701101, 100104, 801104, 401104),
(901105, 501102, 701102, 100105, 801105, 401105);

CREATE TABLE Payment (
    PaymentID INT PRIMARY KEY,
    MemberID INT,
    AdminID INT,
    PaymentDate DATE,
    Price DECIMAL(10,2),
    PaymentMethod VARCHAR(50)
);

INSERT INTO Payment (PaymentID, MemberID, AdminID, PaymentDate, Price, PaymentMethod) VALUES
(301101, 100101, 501101, '2024-01-15', 279.99, 'Cash'),
(301102, 100102, 501102, '2024-02-12', 399.99, 'Cash'),
(301103, 100103, 501103, '2024-03-01', 799.99, 'Cash'),
(301104, 100104, 501101, '2024-03-10', 279.99, 'Cash'),
(301105, 100105, 501102, '2024-03-15', 399.99, 'Cash');

CREATE TABLE Membership (
    MembershipID INT PRIMARY KEY,
    MemberID INT,
    PlanID INT,
    StartDate DATE,
    EndDate DATE,
    PaymentDay INT
);

INSERT INTO Membership (MembershipID, MemberID, PlanID, StartDate, EndDate, PaymentDay) VALUES
(201101, 100101, 601101, '2025-02-15', '2026-02-15', 15),
(201102, 100102, 601102, '2025-02-12', '2026-02-12', 12),
(201103, 100103, 601103, '2025-03-01', '2026-03-01', 1),
(201104, 100104, 601101, '2025-03-10', '2026-03-10', 10),
(201105, 100105, 601102, '2025-03-15', '2026-03-15', 15);

CREATE TABLE Member (
    MemberID INT PRIMARY KEY,
    MembershipID INT,
    PaymentID INT,
    ProgrameID INT,
    AdminID INT,
    FullName VARCHAR(100),
    Age INT,
    PhoneNumber VARCHAR(20),
    RegistrationDate DATE,
    Address VARCHAR(255)
);

INSERT INTO Member (MemberID, MembershipID, PaymentID, ProgrameID, AdminID, FullName, Age, PhoneNumber, RegistrationDate, Address) VALUES
(100101, 201101, 301101, 401101, 501101, 'Kagiso Lesetla', 22, '0792267465', '2024-01-15', '2745 University Drive'),
(100102, 201102, 301102, 401102, 501102, 'Marvin Nkosi', 23, '0735647893', '2024-02-12', '2752 Sekame St'),
(100103, 201103, 301103, 401103, 501103, 'Carol Baloyi', 26, '0797774563', '2024-03-01', '2767 Provident St'),
(100104, 201104, 301104, 401104, 501101, 'David Ntshing', 18, '0658735573', '2024-03-10', '2783 Bothlaping St'),
(100105, 201105, 301105, 401105, 501102, 'Eva Manganyi', 19, '0836574528', '2024-03-15', '2858 Mmabatho'),
(100106, 200106, 300106, 401106, 501103, 'Precious Mkharhi', 18, '0725678356', '2024-01-06', '2738 Rivera Park'),
(100107, 200107, 300107, 401107, 501101, 'Princess Meyer', 29, '0667456365', '2024-01-07', '2749 Golf View'),
(100108, 200108, 300108, 401108, 501102, 'Angel Valoi', 27, '0735674683', '2024-01-08', '2753 Lonely Park'),
(100109, 200109, 300109, 401109, 501103, 'Blessing Maladji', 25, '0824536746', '2024-01-09', '2768 Montlabeng'),
(100110, 200110, 300110, 401110, 501101, 'Koketso Mhlarhi', 21, '0631084756', '2024-01-10', '2784 Seweding'),
(100111, 200111, 300111, 401111, 501102, 'Junior Khoza', 25, '0661019786', '2024-01-11', '2866 Tloung'),
(100112, 200112, 300112, 401112, 501103, 'Mbuyelo Rikhotso', 29, '0725468354', '2024-01-12', '2744 Magogoe'),
(100113, 200113, 300113, 401113, 501101, 'Faith Ntshani', 22, '0662678465', '2024-01-13', '2750 Bokene'),
(100114, 200114, 300114, 401114, 501102, 'Hope Shai', 24, '0816625647', '2024-01-14', '2763 Signal Hill'),
(100115, 200115, 300115, 401115, 501103, 'Phillip Hlatswayo', 28, '0763046857', '2024-01-15', '2769 Dibate'),
(100116, 200116, 300116, 401116, 501101, 'Paul Ngobeni', 25, '0745385746', '2024-01-16', '2855 Danvile'),
(100117, 200117, 300117, 401117, 501102, 'Ofentse Kgosi', 27, '0724652579', '2024-01-17', '2751 Taung'),
(100118, 200118, 300118, 401118, 501103, 'Pholosho Phaahla', 21, '0817238957', '2024-01-18', '2766 Namakgale'),
(100119, 200119, 300119, 401119, 501101, 'Sharmaine Abrahamms', 19, '0785935786', '2024-01-19', '2782 Majeje'),
(100120, 200120, 300120, 401120, 501102, 'Sternan Van Niekerk ', 24, '0764148856', '2024-01-20', '2857 Thapang');
