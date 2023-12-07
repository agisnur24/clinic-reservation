from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class ReqReservation(BaseModel):
    patient_id:         int
    clinic_schedule_id: int

class Create_Patient(BaseModel):
    name:            str
    identity_number: int
    age:             int
    gender:          str
    contact:         str
    address:         str

class Patient(BaseModel):
    id:              int
    name:            str
    identity_number: int
    age:             int
    gender:          str
    contact:         str
    address:         str

class Update_Patient(BaseModel):
    age:     int
    contact: str
    address: int

class Create_Clinic_Schedule(BaseModel):
    day:      str
    date:     str
    time:     str
    max_slot: int

class Clinic_Schedule(BaseModel):
    id:       int
    day:      str
    date:     str
    time:     str
    max_slot: int

class Update_Clinic_Schedule(BaseModel):
    day:      str
    date:     str
    time:     str
    max_slot: int
    
class Reservation(BaseModel):
    id:           int
    patient:      Patient
    booked:       Clinic_Schedule
    queue_number: int

app = FastAPI()

# In-memory storage for simplicity (replace with a database in real project)
patients = []
clinic_schedules = []
reservations = []
reservation_counter = 0

# Make a reservation for a patient
@app.post("/reservation")
async def create_reservation(rsv: ReqReservation):
    global patients
    global clinic_schedules
    global reservations
    
    # Retrieve patient data from the patients list based on the Patient.id condition which is the
    # same as the patient_id from the reservation request
    patient = next((x for x in patients if x.id == rsv.patient_id), None)
    # If patient data is not found, return an error message
    if patient is None:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Patient not found", "Data": {}})
    
    # Retrieve Clinic_Schedule data from the list of clinic_schedules based on the same 
    # Clinic_Schedule.id conditions as the clinic_schedule_id from the reservation request
    schedule = next((x for x in clinic_schedules if x.id == rsv.clinic_schedule_id), None)
    # If clinic schedule data is not found, return an error message
    if schedule is None:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Schedule not found",
                                                     "Data": {}})

    # Create validation to ensure that the same patient does not make more than one reservation
    # on the same schedule
    filtered_patient_reservation = next((x for x in reservations 
                                    if x.patient.id == rsv.patient_id 
                                    and x.booked.id == rsv.clinic_schedule_id), None)
    if filtered_patient_reservation != None:
        raise HTTPException(status_code=400, detail={"Status": False, 
                                                     "Message": "You have made a reservation on that schedule"})
    
    # Insert clinic schedule data into variable book
    book = schedule
    
    # Retrieve all Reservation data from the list of reservations based on the same book.id condition
    # as the clinic_schedule_id from the request to calculate how many slots are left 
    filtered_reservation = [x for x in reservations if x.booked.id == rsv.clinic_schedule_id]
    # Create validation to take the remaining queue and reject reservation requests if the slot quota is full
    if len(filtered_reservation) == book.max_slot:
        raise HTTPException(status_code=400, detail={"Status": False, 
                                                     "Message": "the queue on this schedule is full", 
                                                     "Data": {}})
    else:
        reservation_counter = len(filtered_reservation) + 1
    
    # Insert data into Reservation from the results of previous data retrieval and providing a 
    # queue from the results of previous validation
    reservation = Reservation(
        # The ID is set like this because this project doesn't use a database yet. So that every 
        # time the Reservation data is increased, the ID becomes auto incremented
        id= len(reservations) + 1,
        patient= patient,
        booked= book,
        queue_number= reservation_counter
    )
    
    # Add Reservation data to the reservations list
    reservations.append(reservation)
    
    # Returns data to the user with server response status Created
    return HTTPException(status_code=201, detail={"Status": True, 
                                                  "Message": "Reservation success", 
                                                  "Data": reservation})

# Get reservations list based on schedule
@app.get("/reservations/{clinic_schedule_id}")
async def get_reservations_list_by_schedule(clinic_schedule_id: int):
    
    # Search for reservations based on the same clinic schedule ID as the clinic_schedule_id of the request
    filtered_reservations = [x for x in reservations if x.booked.id == clinic_schedule_id]
    
    # Returns data to the user from the filtered_reservations list
    return {"Status": True, "Message": "Get reservations list by schedule  success",
            "Data": filtered_reservations}

# Get reservations list
@app.get("/reservations")
async def get_reservation_list():
    
    # Check whether there is data in the reservations list or not.
    # If there is no data in the reservations list, it will be returned with the status Not Found
    if len(reservations) < 1:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Data not found", "Data": {}})
    
    # Returns data to the user from the reservations list
    return {"Status": True, "Message": "Get list reservations success", "Data": reservations}

# Update data reservation
@app.patch("/reservation/{reservation_id}")
async def update_reservation(reservation_id: int, clinic_schedule_id: int):
    
    # Search for reservations based on the same ID as the reservation_id of the request
    reservation = next((x for x in reservations if x.id == reservation_id), None)
    
    # Search for clinic_schedule based on the same ID as the clinic_schedule_id from the request
    clinic_schedule = next((x for x in clinic_schedules if x.id == clinic_schedule_id))
    
    # Calculate the queue to see if there are still any remaining slots.
    # If there are no slots remaining, the request will be rejected
    filtered_schedule = [x for x in reservations if x.booked.id == clinic_schedule_id]
    if len(filtered_schedule) == clinic_schedule.max_slot:
        raise HTTPException(status_code=400, detail={"Status": False, 
                                                     "Message": "the queue on this schedule is full", 
                                                     "Data": {}})
    
    # Retrieve queue data from selected reservations
    deleted_queue_number = reservation.queue_number
    
    # Validate so that every queue number that is more than the deleted queue number will be shifted
    # to fill the empty queue and adjust the queue number on the schedule
    filtered_reservations = [r for r in reservations if r.booked.id == reservation.booked.id]
    
    # Update remaining queue numbers
    for r in filtered_reservations:
        if r.queue_number > deleted_queue_number:
            r.queue_number -= 1
    
    # Update clinic_schedule data
    reservation.booked = clinic_schedule
    
    # Update queue number data
    reservation.queue_number = len(filtered_schedule) + 1
    
    # Returns updated data to the user
    return {"Status": True, "message": "Reservation updated successfully", "Data": reservation}

@app.delete("/reservation/{reservation_id}")
async def delete_reservation(reservation_id: int):
    
    # Search for reservations by ID
    reservation = next((x for x in reservations if x.id == reservation_id), None)
    
    # If the reservation is not found, returns an error message
    if reservation is None:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Reservation not found", "Data": {}})
    
    # Retrieve all reservation data based on clinic schedule ID from the reservations list
    filtered_reservations = [r for r in reservations if r.booked.id == reservation.booked.id]
    
    # Update the queue number for another reservation
    for r in filtered_reservations:
        if r.queue_number > reservation.queue_number:
            r.queue_number -= 1
    
    # Delete reservation data from reservations list
    reservations.remove(reservation)
    
    # Return the user a success message
    return {"Status": True, "Message": "Reservation deleted successfully"}

# Make a schedule for the clinic
@app.post("/clinic_schedule")
async def create_clinic_schedule(req: Create_Clinic_Schedule):
    
    # Create validation to ensure there will be no similar schedule data
    schedule = next((x for x in clinic_schedules if x.date == req.date and x.time == req.time), None)
    if schedule != None:
        raise HTTPException(status_code=400, detail={"Status": False, "Message": "Schedule already exist", 
                                                     "Data": {}})
    
    # Insert data into the Clinic_Schedule from the request
    clinic_schedule = Clinic_Schedule(
        id= len(clinic_schedules) + 1,
        day= req.day,
        date= req.date,
        time= req.time,
        max_slot= req.max_slot
    )
    
    # Add Clinic_Schedule data to the clinic_schedules list
    clinic_schedules.append(clinic_schedule)
    
    # Returns data to the user with server response status Created
    return HTTPException(status_code=201, detail={"Status": True, "Message": "Create schedule success",
                                                  "Data": clinic_schedule})

# Get clinic schedules list
@app.get("/clinic_schedules")
async def get_clinic_schedule_list():
    
    # Check whether there is data in the clinic_schedules list or not
    # If there is no data in the clinic_schedule list, it will be returned with the status Not Found
    if len(clinic_schedules) < 1:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Data not found", "Data": {}})
    
    # Returns data to the user from the clinic_schedules list
    return {"Status": True, "Message": "Get list clinic schedules success", "Data": clinic_schedules}

@app.patch("/clinic_schedule/{clinic_schedule_id}")
async def update_clinic_schedule(clinic_schedule_id: int, req: Update_Clinic_Schedule):
    
    # Search for clinic schedule data based on ID
    clinic_schedule = next((x for x in clinic_schedules if x.id == clinic_schedule_id), None)
    # If clinic schedule data is not found, return an error message
    if clinic_schedule is None:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Clinic schedule not found",
                                                     "Data": {}})
    
    # Update clinic schedule data
    clinic_schedule.day = req.day
    clinic_schedule.date = req.date
    clinic_schedule.time = req.time
    clinic_schedule.max_slot = req.max_slot
    
    # Return updated clinic schedule data
    return {"Status": True, "Message": "Clinic schedule updated successfully", "Data": clinic_schedule}

@app.delete("/clinic_schedule/{clinic_schedule_id}")
async def delete_clinic_schedule(clinic_schedule_id: int):
    # Search for clinic schedule data based on ID
    clinic_schedule = next((x for x in clinic_schedules if x.id == clinic_schedule_id), None)
    
    # If clinic schedule data is not found, return an error message
    if clinic_schedule is None:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Clinic schedule not found",
                                                     "Data": {}})
    
    # Delete clinic schedule data from the clinic_schedules list
    clinic_schedules.remove(clinic_schedule)
    
    # Return a success message
    return {"Status": True, "Message": "Clinic schedule deleted successfully"}

# Make a new patient
@app.post("/patient")
async def create_patient(req: Create_Patient):
    
    # Create validation so that no patient has more than one data
    filtered_patient = [x for x in patients if x.identity_number == req.identity_number]
    if len(filtered_patient) > 0:
        raise HTTPException(status_code=400, detail={"Status": False, "Message": "The patient has registered", 
                                                     "Data": {}})
    
    # Insert data into Patient from request
    patient = Patient(
        id= len(patients) + 1,
        name= req.name,
        identity_number= req. identity_number,
        age= req.age,
        gender=  req.gender,
        contact= req.contact,
        address= req.address
    )
    
    # Add Patient data to the patients list
    patients.append(patient)
    
    # Returns data to the user with server response status Created
    return HTTPException(status_code=201, detail={"Status": True, "Message": "Create patient success",
                                                  "Data": patient})

# Get patients list
@app.get("/patients")
async def get_patients_list():
    
    # Check whether there is data in the patients list or not
    # If there is no data in the patients list, it will be returned with the status Not Found
    if len(patients) < 1:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Data not found", "Data": {}})
    
    # Returns data to the user from the patients list
    return {"Status": True, "Message": "Get list patients success", "Data": patients}

@app.patch("/patient/{patient_id}")
async def update_patient(patient_id: int, req: Update_Patient):
    
    # Search patient data by ID
    patient = next((x for x in patients if x.id == patient_id), None)
    
    # If patient data is not found, returns an error message
    if patient is None:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Patient not found", "Data": {}})
    
    # Update patient data
    patient.age = req.age
    patient.contact = req.contact
    patient.address = req.address
    
    # Return updated patient data to the user
    return {"Status": True, "Message": "Patient updated successfully", "Data": patient}

@app.delete("/patient/{patient_id}")
async def delete_patient(patient_id: int):
    
    # Search patient data by ID
    patient = next((x for x in patients if x.id == patient_id), None)
    
    # If patient data is not found, return an error message
    if patient is None:
        raise HTTPException(status_code=404, detail={"Status": False, "Message": "Patient not found", "Data": {}})
    
    # Delete patient data from the patients list
    patients.remove(patient)
    
    # Return a success message
    return {"Status": True, "Message": "Patient deleted successfully"}