const axios = require('axios').default;
var assert = require('assert');
var fs = require('fs');

const API_URL = "http://127.0.0.1:5000";
const FILE_NAME = "api_test.md"


async function clearAll(){
    try {
        let endpoint = `${API_URL}/admin/delete_all`
        return Promise.resolve(axios.post(endpoint)
            .then(function (response) {
                return(response.data.message);
            })).catch(error => {return("Can't access endpoint - POST "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function createSchool(values){
    try {
        let endpoint = `${API_URL}/auth/register/schools`
        return Promise.resolve(axios.post(endpoint, values)
            .then(function (response) {
                return response.data.school
            })).catch(error => {return("Can't access endpoint - POST "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function updateSchool(abbreviation, values){
    try {
        let endpoint = `${API_URL}/api/schools/${abbreviation}`
        return Promise.resolve(axios.put(endpoint, values)
            .then(function (response) {
                return response.data.school
            })).catch(error => {return("Can't access endpoint - PUT "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function getSchool(abbreviation){
    try {
        let endpoint = `${API_URL}/api/schools/${abbreviation}`
        return Promise.resolve(axios.get(endpoint)
            .then(function (response) {
                return response.data.school
            })).catch(error => {return("Can't access endpoint - GET "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function deleteSchool(abbreviation){
    try {
        let endpoint = `${API_URL}/api/schools/${abbreviation}`
        return Promise.resolve(axios.delete(endpoint)
            .then(function (response) {
                return response.data.message
            })).catch(error => {return("Can't access endpoint - DELETE "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

////////////////////////////////////     TEACHER     ////////////////////////////////////

async function createTeacher(school, values){
    try {
        let endpoint = `${API_URL}/auth/register/schools/${school}/teachers`
        return Promise.resolve(axios.post(endpoint, values)
            .then(function (response) {
                return response.data.teacher
            })).catch(error => {return("Can't access endpoint - POST "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function loginTeacher(school, values){
    try {
        let endpoint = `${API_URL}/auth/register/schools/${school}/teachers/login`
        return Promise.resolve(axios.post(endpoint, values)
            .then(function (response) {
                return response.data.teacher
            })).catch(error => {return("Can't access endpoint - POST "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function updateTeacher(teacher_id, values){
    try {
        let endpoint = `${API_URL}/api/teachers/${teacher_id}`
        return Promise.resolve(axios.put(endpoint, values)
            .then(function (response) {
                return response.data.teacher
            })).catch(error => {return("Can't access endpoint - PUT "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function updateTeacherPassword(teacher_id, values){
    try {
        let endpoint = `${API_URL}/auth/teachers/${teacher_id}`
        return Promise.resolve(axios.put(endpoint, values)
            .then(function (response) {
                return response.data.message
            })).catch(error => {return("Can't access endpoint - PUT "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function getTeacher(teacher_id){
    try {
        let endpoint = `${API_URL}/api/teachers/${teacher_id}`
        return Promise.resolve(axios.get(endpoint)
            .then(function (response) {
                return response.data.teacher
            })).catch(error => {return("Can't access endpoint - GET "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function getSchoolTeachers(abbreviation){
    try {
        let endpoint = `${API_URL}/api/school/${abbreviation}/teachers`
        return Promise.resolve(axios.get(endpoint)
            .then(function (response) {
                return response.data.teachers
            })).catch(error => {return("Can't access endpoint - GET "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}

async function deleteTeacher(teacher_id){
    try {
        let endpoint = `${API_URL}/api/teachers/${teacher_id}`
        return Promise.resolve(axios.delete(endpoint)
            .then(function (response) {
                return response.data.message
            })).catch(error => {return("Can't access endpoint - DELETE "+ endpoint + "\n " + error.response.data.message)});
    } catch (error) {
        return (error);
    }
}


////////////////////////////////////     TEST FUNCTIONS     ////////////////////////////////////

async function resetDatabase(){
    fs.appendFile(FILE_NAME,"### Attempting to reset database\n", function (err) {
        if (err){console.log(err);}});

    out = await clearAll()
    console.log(out)
    fs.appendFile(FILE_NAME,out, function (err) {
        if (err){console.log(err);}});
}


async function schoolTests(){
    create = {
        'name' : "Test School",
        'abbreviation' : "TA",
        'email' : "test@gmail.com",
        'domain' : "gmail.com",
        'signup_code' : "AB12",
        'state' : "MO",
        'city' : "STL",
        'address' : "20 N Grand Blvd"
    }
    update = {
        'name' : "Updated Test School",
        'abbreviation' : "UTA",
        'email' : "Updatedtest@gmail.com",
        'domain' : "Updatedgmail.com",
        'signup_code' : "UpdatedAB12",
        'state' : "UpdatedMO",
        'city' : "UpdatedSTL",
        'address' : "Updated20 N Grand Blvd"
    }
    id = 'TA'
    new_id = 'UTA'

    out = await createSchool(create)
    console.log(out)

    out = await updateSchool(id,update)
    console.log(out)

    out = await getSchool(new_id)
    console.log(out)

    out = await deleteSchool(new_id)
    console.log(out)

    out = await getSchool(new_id)
    console.log(out)
}


async function teacherTests(){
    school = {
        'name' : "Test School",
        'abbreviation' : "TA",
        'email' : "test@gmail.com",
        'signup_code' : "AB12",
        'domain' : "school.edu"
    };
    teacher = {
        "email" : "teacher@school.edu",
        "username" : "Teacher1",
        "password" : "pass",
        "code" : "AB12",
        "display_name" : "professor",
        "fname" : "First",
        "lname" : "Last"
    };
    update = {
        "email" : "teacherA@school.edu",
        "username" : "TeacherA",
        "display_name" : "Dr. T",
        "fname" : "FirstName",
        "lname" : "LastName"
    };

    out = await createSchool(school);
    console.log(out);
    school_id = out.abbreviation;

    console.log("Teacher1");
    out = await createTeacher(school_id, teacher);
    teacher_id = out.id;
    console.log(out);

    // Valid teacher
    teacher5 = teacher
    teacher5.email = 'teach@school.edu'
    teacher5.username = 'Teacher5'
    console.log("Teacher5");
    out = await createTeacher(school_id, teacher5);
    console.log(out);

    console.log("Teacher2");
    // Invalid email domain
    teacher2 = teacher
    teacher2.email = 'teach@slu.edu'
    teacher2.usernme = 'Teacher1'
    out = await createTeacher(school_id, teacher2);
    console.log(out);

    console.log("Teacher3");
    // Invalid code
    teacher3 = teacher
    teacher3.email = 'teach@school.edu'
    teacher3.usernme = 'Teacher2'
    teacher3.code = 'CD34'
    out = await createTeacher(school_id, teacher3);
    console.log(out);

    console.log("Teachers");
    out = await getSchoolTeachers(school_id);
    console.log(out);

    console.log("Teacher update");
    out = await updateTeacher(teacher_id, update);
    console.log(out);

    console.log("Teacher1");
    out = await getTeacher(teacher_id);
    console.log(out);

    console.log("Teacher del");
    out = await deleteTeacher(teacher_id);
    console.log(out);

    console.log("Teacher1");
    out = await getTeacher(teacher_id);
    console.log(out);
}


async function testRun(){
    fs.writeFile(FILE_NAME,"# Begin testing API\n", function (err) {
        if (err){console.log(err);}});

    await resetDatabase()
    // await schoolTests()
    // await teacherTests()
}

testRun()
// resetDatabase()