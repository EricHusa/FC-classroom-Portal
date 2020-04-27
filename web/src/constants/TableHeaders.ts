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
        { key: "action", label: "Action", sortable: false }
      ],
    observations: [
        { key: "title", label: "Title", sortable: true },
        { key: "updated", label: "Last Update", sortable: true },
        { key: "action", label: "Action", sortable: false }
    ],
    observationResponse: [
        { key: "number", label: "Number", sortable: true },
        { key: "submitted", label: "Updated on", sortable: true },
        { key: "response", label: "Observation", sortable: false },
        { key: "action", label: "Action", sortable: false }
    ],
    settingsButtons: [
        { key: "option", label: "Options", sortable: false }
    ],
    climate: [
        { key: "name", label: "Name", sortable: true },
        { key: "cycles", label: "Cycles", sortable: true },
        { key: "time_units", label: "Units", sortable: false },
        { key: "action", label: "Action", sortable: false }
    ],
    air_temp: [
        { key: "start_time", label: "Start Hour", sortable: false },
        { key: "end_time", label: "End Hour", sortable: false },
        { key: "value", label: "Degrees (Celsius)", sortable: false }
    ],
    light_intensity: [
        { key: "start_time", label: "Start Hour", sortable: false },
        { key: "end_time", label: "End Hour", sortable: false },
        { key: "value", label: "State", sortable: false }
    ],
    air_flush: [
        { key: "start_time", label: "Start Hour", sortable: false },
        { key: "end_time", label: "End Hour", sortable: false },
        { key: "interval", label: "Frequency (minutes)", sortable: false },
        { key: "duration", label: "Duration (minutes)", sortable: false }
    ]
}