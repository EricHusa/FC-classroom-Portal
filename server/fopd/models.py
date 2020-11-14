from fopd import db

import datetime, uuid

### Many to Many association tables

teacher_devices = db.Table('teacher_devices',
    db.Column('teacher_id', db.String, db.ForeignKey('teacher.id'), nullable = False),
    db.Column('device_id', db.String, db.ForeignKey('device.id'), nullable = False)
)

student_courses = db.Table('student_courses',
    db.Column('student_id', db.String, db.ForeignKey('student.id'), nullable = False),
    db.Column('course_id', db.String, db.ForeignKey('course.id'), nullable = False)
)

student_assignments = db.Table('student_assignments',
    db.Column('assignment_id', db.String, db.ForeignKey('assignment.id'), nullable = False),
    db.Column('student_id', db.String, db.ForeignKey('student.id'), nullable = False)
)

student_experiments = db.Table('student_experiments',
    db.Column('experiment_id', db.String, db.ForeignKey('experiment.id'), nullable = False),
    db.Column('student_id', db.String, db.ForeignKey('student.id'), nullable = False)
)

student_observations = db.Table('student_observations',
    db.Column('observation_id', db.String, db.ForeignKey('observation.id'), nullable = False),
    db.Column('student_id', db.String, db.ForeignKey('student.id'), nullable = False)
)

student_measurements = db.Table('student_measurements',
    db.Column('observation_id', db.String, db.ForeignKey('measurement.id'), nullable = False),
    db.Column('student_id', db.String, db.ForeignKey('student.id'), nullable = False)
)

collaborators = db.Table('collaborators', 
    db.Column('observation_id', db.String, db.ForeignKey('observation.id'), nullable = False),
    db.Column('student_id', db.String, db.ForeignKey('student.id'), nullable = False)
)


class School(db.Model):
    __tablename__ = 'school'

    # keys and attributes
    abbreviation = db.Column(db.String(15), primary_key = True, unique = True)  # primary key
    name = db.Column(db.String(60), nullable = False, unique = True)
    signup_code = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(30), nullable = False)
    domain = db.Column(db.String(20))
    state = db.Column(db.String(20))
    city = db.Column(db.String(100))
    address = db.Column(db.String(100))

    # One to Many relationships
    teachers = db.relationship('Teacher', cascade = 'all, delete-orphan')  # uni
    students = db.relationship('Student', cascade = 'all, delete-orphan')  # uni
    devices = db.relationship('Device')  # uni

    def serialize(self):
        return {
            'name' : self.name,
            'abbreviation' : self.abbreviation
        }

    def serialize_full(self):
        return {
            'name' : self.name,
            'abbreviation' : self.abbreviation,
            'email' : self.email,
            'domain' : self.domain,
            'signup_code' : self.signup_code,
            'location' : {
                'state' : self.state,
                'city' : self.city,
                'address' : self.address
            },
            'devices' : self.serialized_devices()
        }
    
    def serialized_devices(self):
        return [ device.serialize() for device in self.devices]

    def serialized_students(self):
        return [ account.serialize() for account in self.students]


class Teacher(db.Model):
    __tablename__ = 'teacher'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    email = db.Column(db.String(30), nullable = False, unique = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(60), nullable = False)
    display_name = db.Column(db.String(50), nullable = False, default = username)
    fname = db.Column(db.String(25), default = 'Teacher')
    lname = db.Column(db.String(25))

    # foreign keys
    school = db.Column(db.String, db.ForeignKey('school.abbreviation'), nullable = False)  # uni

    # One to Many relationships
    courses = db.relationship('Course', cascade = 'all, delete-orphan')  # uni
    experiments = db.relationship('Experiment', cascade = 'all, delete-orphan')  # uni
    assignments = db.relationship('Assignment', cascade = 'all, delete-orphan')  # uni

    # Many to Many relationships
    devices = db.relationship("Device",secondary=teacher_devices,back_populates="teachers")  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'email' : self.email,
            'username' : self.username,
            'fname' : self.fname,
            'lname' : self.lname,
            'display_name' : self.display_name
        }
    
    def serialize_partial(self):
        return {
            'id' : self.id,
            'display_name' : self.display_name
        }

    def serialized_devices(self):
        return [ device.serialize() for device in self.devices]


class Student(db.Model):
    __tablename__ = 'student'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    username = db.Column(db.String(50), nullable = False)  # Only unique on a per-school basis
    password = db.Column(db.String(60), nullable = False)
    created = db.Column(db.Date, nullable = False, default = datetime.date.today)
    display_name = db.Column(db.String(50), nullable = False, default = username)
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))

    # foreign keys
    school = db.Column(db.String, db.ForeignKey('school.abbreviation'), nullable = False)
    teacher_id = db.Column(db.String, db.ForeignKey('teacher.id'), nullable = False)

    # Many to Many relationships
    assignments = db.relationship("Assignment",secondary=student_assignments,back_populates="students")  # bi
    experiments = db.relationship("Experiment",secondary=student_experiments,back_populates="students")  # bi
    observations = db.relationship("Observation",secondary=student_observations,back_populates="collaborators")  # bi
    measurements = db.relationship("Measurement",secondary=student_measurements,back_populates="collaborators")  # bi
    
    # One to Many relationships
    assignment_responses = db.relationship('AssignmentResponse', back_populates = 'student', lazy = True, cascade = 'all, delete-orphan')  # bi
    # observation_responses = db.relationship('ObservationResponse', back_populates = 'student', lazy = True, cascade = 'all, delete-orphan')  # bi
    # measurement_responses = db.relationship('MeasurementResponse', back_populates = 'student', lazy = True, cascade = 'all, delete-orphan')  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'fname' : self.fname,
            'lname' : self.lname,
            'display_name' : self.display_name,
            'created' : self.created
        }


class Device(db.Model):
    __tablename__ = "device"

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    display_name = db.Column(db.String(50), nullable = False)
    name = db.Column(db.String(50))

    # foreign keys
    school = db.Column(db.String, db.ForeignKey('school.abbreviation'))

    # One to Many relationships
    experiments = db.relationship('Experiment', back_populates = 'device', lazy = True, cascade = 'all, delete-orphan')  # bi

    # Many to Many relationships
    teachers = db.relationship("Teacher",secondary=teacher_devices,back_populates="devices")  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'display_name': self.display_name
        }


class Course(db.Model):
    __tablename__ = 'course'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    name = db.Column(db.String(100), nullable = False)

    # foreign keys
    teacher_id = db.Column(db.String, db.ForeignKey('teacher.id'), nullable = False)

    # Many to Many relationships
    students = db.relationship("Student",secondary=student_courses)  # uni

    def serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'students' : self.serialized_students()
        }

    def serialized_students(self):
        return [ account.serialize() for account in self.students]


class Experiment(db.Model):
    __tablename__ = 'experiment'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    title = db.Column(db.String(80), nullable = False)
    description = db.Column(db.Text, nullable = False)
    plant = db.Column(db.String(50), nullable = False)
    start_date = db.Column(db.Date, nullable = False, default = datetime.date.today)

    # foreign keys
    teacher_id = db.Column(db.String, db.ForeignKey('teacher.id'), nullable = False)
    device_id = db.Column(db.String, db.ForeignKey('device.id'))

    # One to Many relationships
    observations = db.relationship('Observation')  # uni
    measurements = db.relationship('Measurement')  # uni

    # Many to One relationships
    device = db.relationship('Device', back_populates="experiments")  # bi

    # Many to Many relationships
    students = db.relationship("Student",secondary=student_experiments,back_populates="experiments")  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'plant' : self.plant,
            'start_date' : self.start_date,
            'teacher' : self.teacher_id,
            'device' : self.device,
            'students' : self.serialized_students()
        }

    def serialized_students(self):
        return [ account.serialize() for account in self.students]


class Assignment(db.Model):
    __tablename__ = 'assignment'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4())) # primary key
    title = db.Column(db.String(100), nullable = False)
    category = db.Column(db.String(20), nullable = False)
    due_date = db.Column(db.Date, nullable = False)
    units = db.Column(db.String(20))
    description = db.Column(db.Text)

    # foreign keys
    teacher_id = db.Column(db.String, db.ForeignKey('teacher.id'), nullable = False)

    #One to Many relationships
    responses = db.relationship('AssignmentResponse', back_populates = 'assignment', cascade = 'all, delete-orphan')  # bi

    #Many to Many relationships
    students = db.relationship("Student",secondary=student_assignments,back_populates="assignments")  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'description' : self.description,
            'category' : self.category,
            'due_date' : self.due_date,
            'units' : self.units,
            'teacher' : self.teacher_id,
            'students' : self.serialized_students()
        }


class AssignmentResponse(db.Model):
    __tablename__ = 'assignment_responses'
    __table_args__ = (
        db.PrimaryKeyConstraint('student_id', 'assignment_id'),
    )

    # keys and attributes
    response = db.Column(db.Text, default = '')
    submitted = db.Column(db.Date)
    comments = db.Column(db.Text, default = '')

    # foreign keys
    student_id = db.Column(db.String, db.ForeignKey('student.id'), nullable = False)  # makes up composite key
    assignment_id = db.Column(db.String, db.ForeignKey('assignment.id'), nullable = False)  # makes up composite key

    # Many to One relationships
    student = db.relationship("Student", back_populates='assignment_responses')  # bi
    assignment = db.relationship("Assignment", back_populates='responses')  # bi

    def serialize(self):
        assignee = self.student.serialize()
        return {
            'student' : assignee,
            'assignment' : self.assignment_id,
            'response' : self.response,
            'submitted' : self.submitted,
            'comments' : self.comments
        }


class Observation(db.Model):
    __tablename__ = 'observation'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4())) # primary key
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text)
    updated = db.Column(db.Date, nullable = False, default = datetime.date.today)

    # foreign keys
    experiment_id = db.Column(db.String, db.ForeignKey('experiment.id'), nullable = False)

    # One to Many relationships
    responses = db.relationship('ObservationResponse', back_populates='observation')  # bi

    # Many to Many relationships
    collaborators = db.relationship("Student",secondary=student_observations,back_populates="observations")  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'experiment' : self.experiment_id,
            'tile' : self.title,
            'description' : self.description,
            'updated' : self.updated,
            'collaborators' : self.serialized_collaborators()
        }

    def serialized_collaborators(self):
        return [ account.serialize() for account in self.collaborators]

    def serialized_responses(self):
        return [ resp.serialize() for resp in self.responses]


class ObservationResponse(db.Model):
    __tablename__ = 'observation_response'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    response = db.Column(db.Text)
    submitted = db.Column(db.Date, default = datetime.date.today)
    editable = db.Column(db.Boolean, nullable = False, default = True)
    position = db.Column(db.Integer, nullable = False, default = 0)
    recorded_by = db.Column(db.String(50))

    # foreign keys
    observation_id = db.Column(db.String, db.ForeignKey('observation.id'), nullable = False)
    # recorded_by = db.Column(db.String, db.ForeignKey('student.id'), nullable = True)

    # Many to One relationships
    observation = db.relationship("Observation", back_populates='responses')  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'observation' : self.observation_id,
            'recorder' : self.recorded_by,
            'submitted' : self.submitted,
            'response' : self.response,
            'editable' : self.editable,
            'position' : self.position
        }


class Measurement(db.Model):
    __tablename__ = 'measurement'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text)
    updated = db.Column(db.Date, nullable = False, default = datetime.date.today)
    units = db.Column(db.String(20, nullable = False))
    graphics = db.Column(db.Boolean, nullable = False, default = True)
    public = db.Column(db.Boolean, nullable = False, default = False)

    # foreign keys
    experiment_id = db.Column(db.String, db.ForeignKey('experiment.id'), nullable = False)

    # One to Many relationships
    responses = db.relationship('MeasurementResponse', back_populates='measurement')  # bi

    # Many to Many relationships
    collaborators = db.relationship("Student",secondary=student_measurements,back_populates="measurements")  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'tile' : self.title,
            'description' : self.description,
            'updated' : self.updated,
            'units' : self.units,
            'graphics' : self.graphics,
            'public' : self.public,
            'collaborators' : self.serialized_collaborators()
        }

    def serialized_collaborators(self):
        return [ account.serialize() for account in self.collaborators]

    def serialized_responses(self):
        return [ resp.serialize() for resp in self.responses]


class MeasurementResponse(db.Model):
    __tablename__ = 'measurement_response'

    # keys and attributes
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    response = db.Column(db.Float)
    submitted = db.Column(db.Date)
    editable = db.Column(db.Boolean, nullable = False, default = True)
    position = db.Column(db.Integer, nullable = False, default = 0)
    recorded_by = db.Column(db.String(50))

    # foreign keys
    measurement_id = db.Column(db.String, db.ForeignKey('measurement.id'), nullable = False)

    # Many to One relationships
    measurement = db.relationship("Measurement", back_populates='responses')  # bi

    def serialize(self):
        return {
            'id' : self.id,
            'measurement' : self.measurement.serialize(),
            'recorder' : self.recorded_by,
            'submitted' : self.submitted,
            'response' : self.response,
            'editable' : self.editable,
            'position' : self.position
        }
