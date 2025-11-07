Система Деканат 50 классов + 12 классов исключений
Кол-во полей: 162
Кол-во методов: 126
Кол-во ассоциаций: 63


Person 3 2 ->
Student 5 6 -> Group, Transcript, AcademicRecord, Payment, Exam
Teacher 4 5 -> Grade, Attendance, Research, Exam
Dean 1 3 -> Faculty, StudyPlan, Graduate
Accountant 0 5 -> Payment, Salary, Invoice, Scholarship
ForeignStudent 1 1 -> Visa
Applicant 1 3 -> Application
Graduate 1 2 -> Diploma
HeadOfDepartment 0 1 -> Department
Methodologist 0 3 -> Curriculum, Course, Exam
Secretary 0 3 -> TransferDocument, Credit, Exam

Faculty 3 2 -> Department
Department 4 2 -> Teacher
Group 3 3 ->
Course 4 4 -> Student, Grade
Curriculum 2 2 -> StudyPlan
Schedule 1 4 -> Course, Classroom
Exam 3 2 -> Student, Grade
Credit 2 3 -> Student
Grade 3 0 ->
AcademicRecord 2 2 -> Grade
Attendance 3 1 -> Student
Research 3 2 -> Teacher, Conference
Conference 3 1 -> Research
Semester 3 2 -> Course
AcademicEvent 3 3 ->
StudyPlan 2 2 -> Curriculum

Payment 5 6 -> Student
Scholarship 3 3 -> Student
Salary 3 2 -> Person
Invoice 3 2 -> Person
BankAccount 2 3 ->
MoneyTransfer 4 2 -> BankAccount
Budget 2 4 ->
FinancialReport 2 2 -> Budget

Building 4 3 -> Classroom, Room
Classroom 4 2 ->
Library 2 4 -> Book
Book 5 3 ->
Dormitory 3 2 -> Room
Room 5 2 -> Student
Cafeteria 3 3 ->

Document 4 2 -> Person
Transcript 1 1 -> Student
Diploma 3 4 -> Graduate
Certificate 3 2 -> Person
Visa 2 2 -> ForeignStudent
Application 3 2 -> Applicant
Contract 4 3 -> Person
TransferDocument 4 2 -> Student, Group

AcademicException 0 0 ->
InsufficientFundsException 0 0 ->
StudentNotFoundException 0 0 ->
CourseFullException 0 0 ->
InvalidGradeException 0 0 ->
DuplicateEnrollmentException 0 0 ->
PaymentProcessingException 0 0 ->
VisaExpiredException 0 0 ->
RoomCapacityException 0 0 ->
BookNotAvailableException 0 0 ->
InvalidScheduleException 0 0 ->
ScholarshipCriteriaException 0 0 ->
