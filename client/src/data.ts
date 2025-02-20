export const employees = [
  {
    id: 1,
    name: "Alice Johnson",
    title: "CEO",
    manager_id: null,
    direct_reports: [
      {
        id: 2,
        name: "Bob Smith",
        title: "Engineering Manager",
        manager_id: 1,
        direct_reports: [
          {
            id: 4,
            name: "David Brown",
            title: "Software Engineer",
            manager_id: 2,
            direct_reports: [],
          },
          {
            id: 5,
            name: "Ella Davis",
            title: "Software Engineer",
            manager_id: 2,
            direct_reports: [],
          },
        ],
      },
      {
        id: 3,
        name: "Catherine Lee",
        title: "Marketing Manager",
        manager_id: 1,
        direct_reports: [
          {
            id: 6,
            name: "Frank Wilson",
            title: "Marketing Specialist",
            manager_id: 3,
            direct_reports: [],
          },
          {
            id: 7,
            name: "Grace Miller",
            title: "Marketing Specialist",
            manager_id: 3,
            direct_reports: [],
          },
        ],
      },
      {
        id: 8,
        name: "Hank White",
        title: "HR Specialist",
        manager_id: 1,
        direct_reports: [],
      },
    ],
  },
];
