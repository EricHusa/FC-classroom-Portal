from fopd import db

import datetime, uuid


class School(db.Model):
    __tablename__ = 'school'

    # keys
    abbreviation = db.Column(db.String(15), primary_key = True, unique = True)  # primary key
    name = db.Column(db.String(60), nullable = False, unique = True)
    state = db.Column(db.String(20), default = '')
    city = db.Column(db.String(100), default = '')
    code = db.Column(db.String(15), default = '')
    address = db.Column(db.String(100), default = '')

    # One to Many relationships
    teachers = db.relationship('Teacher', backref = 'school', lazy = True, cascade = 'all, delete-orphan')
    students = db.relationship('Student', backref = 'school', lazy = True, cascade = 'all, delete-orphan')
    devices = db.relationship('Device', backref = 'school', lazy = True, cascade = 'all, delete-orphan')


teacher_devices = db.Table('teacher_devices',
    db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), nullable = False),
    db.Column('device_id', db.Integer, db.ForeignKey('device.id'), nullable = False)
)

class Teacher(db.Model):
    __tablename__ = 'teacher'

    # keys
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    email = db.Column(db.String(30), nullable = False, unique = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(60), nullable = False)
    fname = db.Column(db.String(25), default = 'No Name')
    lname = db.Column(db.String(25), default = 'No Name')
    # public_id = db.Column(db.String(100), unique = True)

    # foreign keys
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable = False)

    # One to Many relationships
    students = db.relationship('Student', backref = 'teacher', lazy = True)
    courses = db.relationship('Course', backref = 'teacher', lazy = True, cascade = 'all, delete-orphan')
    experiments = db.relationship('Experiment', backref = 'teacher', lazy = True, cascade = 'all, delete-orphan')
    assigned_assignments = db.relationship('Assignment', backref = 'teacher', lazy = True, cascade = 'all, delete-orphan')
    # devices = db.relationship('Device', backref = 'teacher', lazy = True) # do not cascade

    #Many to Many relationships
    devices = relationship("Device",secondary=teacher_devices,back_populates="teachers")

    def __repr__(self):
        return f'<Teacher("{self.username}", "{self.public_id}")>'

    # def __eq__(self, other):
    #     return self._id == other._id and self.public_id == other.public_id

### Many to many

student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), nullable = False),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), nullable = False)
)

### Student assignments
student_assignments = db.Table('student_assignments',
    db.Column('assignment_id', db.Integer, db.ForeignKey('assignment.id'), nullable = False),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), nullable = False)
)

student_experiments = db.Table('student_experiments',
    db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id'), nullable = False),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), nullable = False)
)

student_observations = db.Table('student_observations',
    db.Column('observation_id', db.Integer, db.ForeignKey('observation.id'), nullable = False),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), nullable = False)
)

student_measurements = db.Table('student_observations',
    db.Column('observation_id', db.Integer, db.ForeignKey('observation.id'), nullable = False),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), nullable = False)
)

class Student(db.Model):
    __tablename__ = 'student'

    # keys
    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))  # primary key
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(60), nullable = False)
    fname = db.Column(db.String(25), default = 'No Name')
    lname = db.Column(db.String(25), default = '')
    created = db.Column(db.Date, nullable = False, default = datetime.date.today)

    # foreign keys
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable = False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable = False)

    # Many to Many relationships
    courses = relationship("Course",secondary=student_courses,back_populates="students")
    assignments = relationship("Assignment",secondary=student_assignments,back_populates="students")
    experiments = relationship("Experiment",secondary=student_experiments,back_populates="students")
    observations = relationship("Observation",secondary=student_observations,back_populates="collaborators")
    measurements = relationship("Measurement",secondary=student_measurements,back_populates="collaborators")
    
    # One to Many relationships
    assignment_responses = db.relationship('AssignmentResponse', backref = 'student', lazy = True, cascade = 'all, delete-orphan')
    observation_responses = db.relationship('ObservationResponse', backref = 'student', lazy = True, cascade = 'all, delete-orphan')
    measurement_responses = db.relationship('MeasurementResponse', backref = 'student', lazy = True, cascade = 'all, delete-orphan')

    def __repr__(self):
        return f'<Student("{self.username}", "{self.fname}", "{self.public_id}")>'

    def __eq__(self, other):
        return self._id == other._id

class Device(db.Model):
    __tablename__ = "device"

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable = False)
    # public_id = db.Column(db.String(100), unique = True, default = str(uuid.uuid4()))

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id')) # can be null
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable = False)

    experiments = db.relationship('Experiment', backref = 'device', lazy = True, cascade = 'all, delete-orphan')
    teachers = relationship("Teacher",secondary=teacher_devices,back_populates="devices")

    def __repr__(self):
        return f'<Device("{self.name}")>'

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable = False)
    # public_id = db.Column(db.String(100), unique = True, default = str(uuid.uuid4()))

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable = False)

    # students = db.relationship('Student', backref = 'course', lazy = True) #, cascade = 'all, delete-orphan') ask if cascade
    students = relationship("Student",secondary=student_classes,back_populates="courses")


    def __repr__(self):
        return f'<Course("{self.name}", "{self.public_id}", "{self.students[:4]}")>'


class Experiment(db.Model):
    __tablename__ = 'experiment'

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))
    title = db.Column(db.String(80), nullable = False)
    description = db.Column(db.Text, nullable = False)
    plant = db.Column(db.String(50), nullable = False)
    start_date = db.Column(db.Date, nullable = False, default = datetime.date.today)
    # public_id = db.Column(db.String(100), unique = True, default = str(uuid.uuid4()))

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable = False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable = False)

    # observations = db.relationship('Observation', backref = 'experiment', lazy = True, cascade = 'all, delete-orphan')
    # measurements = db.relationship('Measurement', backref = 'experiment', lazy = True, cascade = 'all, delete-orphan')
    # students = db.relationship('Student', backref = 'experiment', lazy = False)
    observations = db.relationship('Observation')
    measurements = db.relationship('Measurement')

    #Many to Many
    students = relationship("Student",secondary=student_measurements,back_populates="experiments")

    def __repr__(self):
        return f'<Experiment("{self.title}", "{self.start_date}", "{self.public_id}", "{self.students[:4]}")>'

# import enum
# class TypeOptions(enum.Enum):
    # written = 0
    # numerical = 1

    
class Assignment(db.Model):
    __tablename__ = 'assignment'

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = False)
    type = db.Column(db.String(50), nullable = False)
    due_date = db.Column(db.Date, nullable = False, default = datetime.date.today)
    # public_id = db.Column(db.String(100), unique = True, default = str(uuid.uuid4()))

    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable = False)

    #One to Many
    responses = db.relationship('AssignmentResponse', backref = 'assignment', lazy = True, cascade = 'all, delete-orphan')

    #Many to Many
    students = relationship("Student",secondary=student_measurements,back_populates="observations")
    
    # TODO: test many-to-many works
    def __repr__(self):
        return f'<Assignment("{self.title}", "{self.type}", "{self.public_id}", "{self.teacher.username}")>'

    # def __eq__(self, other):
    #     return self._id == other._id and self._title == other.title and self.public_id == other.public_id


class AssignmentResponse(db.Model):
    __tablename__ = 'assignment_responses'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)  #remove?
    response = db.Column(db.Text, default = '')
    submitted = db.Column(db.Date)
    comments = db.Column(db.Text, default = '')
    public_id = db.Column(db.String(100), unique = True, default = str(uuid.uuid4()))

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable = False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable = False)

    def __repr__(self):
        return f'<AssignmentResponse("{self.response}", "{self.student.username}", "{self.public_id}")>'


# observation_responses = db.Table('observation_responses', 
#     db.Column('experiment_id', db.Integer, db.ForeignKey('experiment.id'), nullable = False),
#     db.Column('observation_id', db.Integer, db.ForeignKey('observation.id'), nullable = False)
# )

collaborators = db.Table('collaborators', 
    db.Column('observation_id', db.Integer, db.ForeignKey('observation.id'), nullable = False),
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), nullable = False)
)

class Observation(db.Model):
    __tablename__ = 'observation'

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))
    title = db.Column(db.String(50), nullable = False)
    type = db.Column(db.String(30), nullable = False)
    description = db.Column(db.Text, nullable = False)
    units = db.Column(db.String(30), nullable = False)
    updated = db.Column(db.Date, nullable = False, default = datetime.date.today)
    # public_id = db.Column(db.String(100), unique = True, default = str(uuid.uuid4()))

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable = False)

    # student_collaborators = db.relationship('Student', secondary = collaborators, lazy = 'subquery', backref = db.backref('observations', lazy = True))
    responses = db.relationship('ObservationResponse')

    #Many to Many
    collaborators = relationship("Student",secondary=student_measurements,back_populates="observations")

class ObservationResponse(db.Model):
    __tablename__ = 'observation_response'

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))
    response = db.Column(db.Text)
    submitted = db.Column(db.Date, nullable = True)
    editable = db.Column(db.Boolean, nullable = False, default = True)
    # public_id = db.Column(db.String(100), unique = True, default = str(uuid.uuid4()))

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    observation_id = db.Column(db.Integer, db.ForeignKey('observation.id'), nullable = False)

class Measurement(db.Model):
    __tablename__ = 'measurement'

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'), nullable = False)

    collaborators = relationship("Student",secondary=student_measurements,back_populates="measurements")

    responses = db.relationship('MeasurementResponse')

class MeasurementResponse(db.Model):
    __tablename__ = 'measurement_response'

    id = db.Column(db.String(36), primary_key = True, unique = True, default = str(uuid.uuid4()))

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    observation_id = db.Column(db.Integer, db.ForeignKey('observation.id'), nullable = False)