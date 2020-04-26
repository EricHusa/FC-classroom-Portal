export default {
    assignmentOptions: {
        options: [
            {key: "title", label: "Title", required: true, type: "text"},
            {
                key: "description",
                label: "Description",
                required: false,
                type: "text"
            },
            {key: "due_date", label: "Due Date", required: true, type: "date"}
        ],
        types: [
            {text: "Written response", value: "text"},
            {text: "Numerical response", value: "number"}
        ]
    },
    observationOptions: {
        options: [
            {key: "title", label: "Title", required: true, type: "text"},
            {
                key: "description",
                label: "Description",
                required: false,
                type: "text"
            },
        ],
        types: [
            {text: "Written responses", value: "text"},
            {text: "Numerical responses", value: "number"}
        ]
    }
}