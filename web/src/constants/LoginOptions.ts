export default {
    login: [
        { key: "teacher", label: "Teacher", required: true, type: "text" },
        { key: "username", label: "Username", required: true, type: "text" },
        { key: "password", label: "Password", required: true, type: "password" }
      ],
    register: [
        { key: "fopd_id", label: "Device ID", required: true, type: "text" },
        { key: "fname", label: "First Name", required: true, type: "text" },
        { key: "lname", label: "Last Name", required: true, type: "text" },
        { key: "password", label: "Password", required: true, type: "password" },
        { key: "repeatPassword", label: "Confirm Password", required: true, type: "password" }
      ]
}