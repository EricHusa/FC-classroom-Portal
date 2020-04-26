export default {
    experiments: [
        { name: "Name", type: "text", key: "title" },
        {name: "Description", type: "textarea-default", key: "description"},
        { name: "Plant", type: "text", key: "plant"},
        { name: "Start Date", type: "date", key: "start_date" }
      ],
    assignments: [
        { key: "title", label: "Title", sortable: true },
        { key: "due_date", label: "Due Date", sortable: true },
        { key: "action", label: "Action", sortable: false },
      ],
    observations: [
        { key: "title", label: "Title", sortable: true },
        { key: "updated", label: "Last Update", sortable: true },
        { key: "action", label: "Action", sortable: false },
    ],
    observationResponse: [
        { key: "number", label: "Number", sortable: true },
        { key: "submitted", label: "Updated on", sortable: true },
        { key: "response", label: "Observation", sortable: false },
        { key: "action", label: "Action", sortable: false },
    ]
}