# API Clinic Reservation System

This API application is a simple clinic reservation system with endpoints for managing patients, clinic schedules, and reservations.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/agisnur24/clinic-reservation.git
   cd clinic-reservation
   ```

2. Use virtual environments (venv):

   ```bash
   & "your save location"/clinic-reservation/venv/Scripts/Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:

   ```bash
   uvicorn main:app --reload
   ```

The FastAPI application will start at `http://127.0.0.1:8000`.

## Endpoints

### Create Reservation

- **Endpoint:** `/reservation`
- **Method:** `POST`
- **Description:** Create a reservation for a patient on a specific clinic schedule.
- **Request Body:**
  - `patient_id` (int): Patient ID.
  - `clinic_schedule_id` (int): Clinic schedule ID.

### Get Reservations List by Schedule

- **Endpoint:** `/reservations/{clinic_schedule_id}`
- **Method:** `GET`
- **Description:** Get a list of reservations for a specific clinic schedule.
- **Path Parameter:**
  - `clinic_schedule_id` (int): Clinic schedule ID.

### Get Reservations List

- **Endpoint:** `/reservations`
- **Method:** `GET`
- **Description:** Get a list of all reservations.

### Update Reservation

- **Endpoint:** `/reservation/{reservation_id}`
- **Method:** `PATCH`
- **Description:** Update the clinic schedule of an existing reservation.
- **Path Parameter:**
  - `reservation_id` (int): Reservation ID.
- **Request Body:**
  - `clinic_schedule_id` (int): New clinic schedule ID.

### Delete Reservation

- **Endpoint:** `/reservation/{reservation_id}`
- **Method:** `DELETE`
- **Description:** Delete a reservation.
- **Path Parameter:**
  - `reservation_id` (int): Reservation ID.

### Create Clinic Schedule

- **Endpoint:** `/clinic_schedule`
- **Method:** `POST`
- **Description:** Create a new clinic schedule.
- **Request Body:**
  - `day` (str): Day of the week.
  - `date` (str): Date of the clinic schedule.
  - `time` (str): Time of the clinic schedule.
  - `max_slot` (int): Maximum slots available.

### Get Clinic Schedules List

- **Endpoint:** `/clinic_schedules`
- **Method:** `GET`
- **Description:** Get a list of all clinic schedules.

### Update Clinic Schedule

- **Endpoint:** `/clinic_schedule/{clinic_schedule_id}`
- **Method:** `PATCH`
- **Description:** Update an existing clinic schedule.
- **Path Parameter:**
  - `clinic_schedule_id` (int): Clinic schedule ID.
- **Request Body:**
  - `day` (str): New day of the week.
  - `date` (str): New date of the clinic schedule.
  - `time` (str): New time of the clinic schedule.
  - `max_slot` (int): New maximum slots available.

### Delete Clinic Schedule

- **Endpoint:** `/clinic_schedule/{clinic_schedule_id}`
- **Method:** `DELETE`
- **Description:** Delete a clinic schedule.
- **Path Parameter:**
  - `clinic_schedule_id` (int): Clinic schedule ID.

### Create Patient

- **Endpoint:** `/patient`
- **Method:** `POST`
- **Description:** Create a new patient.
- **Request Body:**
  - `name` (str): Patient's name.
  - `identity_number` (int): Patient's identity number("UNIQUE". such as an identity card number or driver's license).
  - `age` (int): Patient's age.
  - `gender` (str): Patient's gender.
  - `contact` (str): Patient's contact information.
  - `address` (str): Patient's address.

### Get Patients List

- **Endpoint:** `/patients`
- **Method:** `GET`
- **Description:** Get a list of all patients.

### Update Patient

- **Endpoint:** `/patient/{patient_id}`
- **Method:** `PATCH`
- **Description:** Update an existing patient's information.
- **Path Parameter:**
  - `patient_id` (int): Patient ID.
- **Request Body:**
  - `age` (int): New patient's age.
  - `contact` (str): New patient's contact information.
  - `address` (str): New patient's address.

### Delete Patient

- **Endpoint:** `/patient/{patient_id}`
- **Method:** `DELETE`
- **Description:** Delete a patient.
- **Path Parameter:**
  - `patient_id` (int): Patient ID.

## Note

This application uses in-memory storage for simplicity. In a real-world project, replace it with a proper database.