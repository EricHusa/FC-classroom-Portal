export default {
    admin: [],
    teacher: [
        {name: "Home", path: "/"},
        {name: "School", path: "/school"},
        {name: "Settings", path: "/settings"},
        {name: "Help", path: "/help"},
        {name: "Sign Out", path: "/login"}
    ],
    student: [
        {name: "Sign Out", path: "/login"}
        ],
    guest: [
        {name: "Sign In", path: "/login"},
        {name: "Help", path: "/help"}
    ]
};