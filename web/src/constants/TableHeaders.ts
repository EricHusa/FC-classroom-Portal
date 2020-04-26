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
        { key: "action", label: "Action" },
      ]
}